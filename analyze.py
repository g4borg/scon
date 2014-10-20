#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Tool to analyze Logs in general.
"""
import os, sys, logging
from logs.logfiles import LogFileResolver as LogFile
from logs import combat, game, chat
from logs.session import LogSessionCollector
from logs.game import ClientInfo

# for windows its kinda this:
settings = {'root_path': os.path.join(os.path.expanduser('~'),
                                     'Documents',
                                     'My Games',
                                     'StarConflict',),            
            'logfiles': os.path.join(os.path.expanduser('~'),
                                     'Documents',
                                     'My Games',
                                     'StarConflict',
                                     'logs'
                                     )}


if __name__ == '__main__':
    coll = LogSessionCollector(os.path.join(os.path.expanduser('~'),
                        'Documents', 'My Games', 'sc'))
    coll.collect_unique()
    #f = open('output.txt', 'w')
    rex_combat = {}
    rex_game = {}
    for logf in coll.sessions:
        logf.parse_files(['game.log', 'combat.log'])
        print "----- Log %s -----" % logf.idstr
        if logf.combat_log:
            for l in logf.combat_log.lines:
                if isinstance(l, dict):
                    #print l
                    rex_combat['dict'] = rex_combat.get('dict', 0) + 1
                else:
                    if not l.unpack():
                        rex_combat[l.__class__.__name__] = rex_combat.get(l.__class__.__name__, 0) + 1
                        if not isinstance(l, combat.UserEvent):
                            print l.values['log']
        if logf.game_log:
            for l in logf.game_log.lines:
                if isinstance(l, dict):
                    rex_game['dict'] = rex_game.get('dict', 0) + 1 
                elif isinstance(l, str):
                    print l
                else:
                    if l.unpack():
                        pass
                    else:
                        rex_game[l.__class__.__name__] = rex_game.get(l.__class__.__name__, 0) + 1
                        print l.values['log']
                    # ClientInfo introspection for ping
                    #if isinstance(l, ClientInfo) and l.values.get('clinfo', '') == 'avgPing':
                    #    print l.values
                    #    # fix avgPing parsing!
    print 'Analysis complete:'
    print '#'*20+' RexCombat ' + '#' *20
    print rex_combat
    print '#'*20+' RexGame ' + '#' *20
    print rex_game
