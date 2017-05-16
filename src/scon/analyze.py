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
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    coll = LogSessionCollector(os.path.join(os.path.expanduser('~'),
                        'Documents', 'My Games', 'sc'))
    logging.info('Collecting Sessions...')
    coll.collect_unique()
    logging.info('collected %s sessions.' % (len(coll.sessions)))
    #f = open('output.txt', 'w')
    rex_combat = {}
    rex_game = {}
    rex_chat = {}
    LOG_GOOD = True # Log good packets.
    for logf in coll.sessions:
        logf.parse_files(['game.log', 'combat.log', 'chat.log'])
        
        print(("----- Log %s -----" % logf.idstr))
        if logf.combat_log:
            for l in logf.combat_log.lines:
                if isinstance(l, dict):
                    #print l
                    rex_combat['dict'] = rex_combat.get('dict', 0) + 1
                else:
                    if not l.unpack() or LOG_GOOD:
                        rex_combat[l.__class__.__name__] = rex_combat.get(l.__class__.__name__, 0) + 1
                        if not isinstance(l, combat.UserEvent):
                            if not LOG_GOOD:
                                print((l.values['log']))
        else:
            logging.debug('No combat log in %s' % logf.idstr)
        if logf.game_log:
            for l in logf.game_log.lines:
                if isinstance(l, dict):
                    rex_game['dict'] = rex_game.get('dict', 0) + 1 
                elif isinstance(l, str):
                    print(l)
                else:
                    if l.unpack() and not LOG_GOOD:
                        pass
                    else:
                        rex_game[l.__class__.__name__] = rex_game.get(l.__class__.__name__, 0) + 1
                        if not LOG_GOOD:
                            print((l.values['log']))
        else:
            logging.debug('No game log in %s' % logf.idstr)
        if logf.chat_log:
            for l in logf.chat_log.lines:
                if isinstance(l, dict):
                    rex_chat['dict'] = rex_chat.get('dict', 0) + 1 
                elif isinstance(l, str):
                    print(l)
                else:
                    if l.unpack() and not LOG_GOOD:
                        pass
                    else:
                        rex_chat[l.__class__.__name__] = rex_chat.get(l.__class__.__name__, 0) + 1
                        if not LOG_GOOD:
                            print((l.values['log']))
        else:
            logging.debug('No chat log in %s' % logf.idstr)
        logf.clean(True)
        # additional cleanup:
        if logf.chat_log:
            logf.chat_log.lines = []
        if logf.game_log:
            logf.game_log.lines = []
        if logf.combat_log:
            logf.combat_log.lines = []
    print('Analysis complete:')
    print(('#'*20+' RexCombat ' + '#' *20))
    print(rex_combat)
    print(('#'*20+' RexGame ' + '#' *20))
    print(rex_game)
    print(('#'*20+' RexChat ' + '#' *20))
    print(rex_chat)
