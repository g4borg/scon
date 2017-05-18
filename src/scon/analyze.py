#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Tool to analyze Logs in general.
"""
import os, sys, logging
from scon.logs.logfiles import LogFileResolver as LogFile
from scon.logs import combat, game, chat
from scon.logs.session import LogSessionCollector
from scon.logs.game import ClientInfo

# for windows its kinda this:
# note, this isnt used in this script. yeah i know right, defined up here, but not used down there.
# it's because i want to unify this to be on one configurable place ;)
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
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logfile = logging.FileHandler('scon.log.bak')
    logfile.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(logfile)
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
        
        logging.info(("## Processing Log %s" % logf.idstr))
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
                                logging.debug((l.values['log']))
        else:
            logging.warning('No combat log in %s' % logf.idstr)
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
                            logging.debug((l.values['log']))
        else:
            logging.warning('No game log in %s' % logf.idstr)
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
                            logging.debug((l.values['log']))
        else:
            logging.warning('No chat log in %s' % logf.idstr)
        logf.clean(True)
        # additional cleanup:
        if logf.chat_log:
            logf.chat_log.lines = []
        if logf.game_log:
            logf.game_log.lines = []
        if logf.combat_log:
            logf.combat_log.lines = []
    logging.info('Analysis complete:')
    logging.info(('#'*20+' RexCombat ' + '#' *20))
    logging.info(rex_combat)
    logging.info(('#'*20+' RexGame ' + '#' *20))
    logging.info(rex_game)
    logging.info(('#'*20+' RexChat ' + '#' *20))
    logging.info(rex_chat)
