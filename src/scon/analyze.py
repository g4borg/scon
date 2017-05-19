#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Tool to analyze Logs in general.
    
    This tool is built to discover unidentified packets.
    It is mainly used in development 
    (for the whole library, this is actually the most important script atm)
    
    It outputs a trash.log.bak and a scon.log.bak, and works itself through gigabytes of my backuped test data.
    
    This script therefore has following purposes:
        - a) find bugs, find unknown packets (so new type of log entries in combat.log)
        - b) see speed of parsing
        - c) test parsing for memory efficiency, because parsing lots of big files needs that.
"""
import os, sys, logging
from scon.logs.logfiles import LogFileResolver as LogFile
from scon.logs import combat, game, chat
from scon.logs.session import LogSessionCollector
from scon.logs.game import ClientInfo

# only analyze_path is used in this script. the others are for example.
settings = {'analyze_path': os.path.join(os.path.expanduser('~'),
                        'Documents', 'My Games', 'sc'),
            
            'root_path': os.path.join(os.path.expanduser('~'),
                                     'Documents',
                                     'My Games',
                                     'StarConflict',),            
            'logfiles': os.path.join(os.path.expanduser('~'),
                                     'Documents',
                                     'My Games',
                                     'StarConflict',
                                     'logs'
                                     ),}

def select_parsing_sessions(alist):
    # for micro controlling, which sessions to parse.
    # default: return alist
    return alist[-50:]

if __name__ == '__main__':
    # set this to your liking:
    COUNT_GOOD = True # count via rex good packets aswell. useful to see total encountered packets in summary.
    LOG_GOOD_ONLY = False # Log good packets only. if set to false, will log unknown packets to trash_log.
    LOG_BAD_CMBT = True # by default, the main logs of interest for unknown entries is combat logs. here you can finetune which logs to catch.
    LOG_BAD_CHAT = False
    LOG_BAD_GAME = False
    
    # set up our logging to do our task:
    FILE_MAIN_LOG = 'scon.log.bak'
    FILE_TRASH_LOG = 'trash.log.bak'
    if os.path.exists(FILE_MAIN_LOG) and os.path.isfile(FILE_MAIN_LOG):
        os.remove(FILE_MAIN_LOG)
    if os.path.exists(FILE_TRASH_LOG) and os.path.isfile(FILE_TRASH_LOG):
        os.remove(FILE_TRASH_LOG)
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logfile = logging.FileHandler(FILE_MAIN_LOG)
    logfile.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(logfile)
    
    trashfile = logging.FileHandler(FILE_TRASH_LOG)
    trashfile.setLevel(logging.INFO)
    trash_log = logging.getLogger('trash_log')
    
    trash_log.addHandler(trashfile)
    trash_log.propagate = False # only log to file.
    
    ###################################
    
    # collect all sessions, as in, get all log directories:
    coll = LogSessionCollector(settings.get('analyze_path'))
    logging.info('Collecting Sessions...')
    coll.collect_unique()
    logging.info('collected %s sessions.' % (len(coll.sessions)))
    
    # now do in depth parsing per session:
    
    #f = open('output.txt', 'w')
    rex_combat = {}
    rex_game = {}
    rex_chat = {}
    
    selected = select_parsing_sessions(coll.sessions)
    logging.info("Start In Depth parsing for %s sessions. %s" % (len(selected),'Counting good packets' if COUNT_GOOD else 'Counting only bad packets.'))
    if LOG_GOOD_ONLY:
        logging.info("Only logging unknown variants of known packet types")
    else:
        logging.info("Logging unknown packets aswell, CMBT: %s, GAME: %s, CHAT %s" % (LOG_BAD_CMBT, LOG_BAD_GAME, LOG_BAD_CHAT))
    for logf in selected:
        logf.parse_files(['game.log', 'combat.log', 'chat.log'])
        
        logging.info(("## Processing Log %s" % logf.idstr))
        if logf.combat_log:
            for l in logf.combat_log.lines:
                if isinstance(l, dict):
                    #print l
                    rex_combat['dict'] = rex_combat.get('dict', 0) + 1
                    if not LOG_GOOD_ONLY and LOG_BAD_CMBT:
                        x = l.get('log', None)
                        if x:
                            trash_log.info(x)
                        else:
                            logging.warning('Unknown dictionary: %s' % l)
                else:
                    if not l.unpack() or COUNT_GOOD:
                        rex_combat[l.__class__.__name__] = rex_combat.get(l.__class__.__name__, 0) + 1
                    if not isinstance(l, combat.CombatLog):
                        if not LOG_GOOD_ONLY and LOG_BAD_CMBT:
                            trash_log.info((l.values['log']))
        else:
            logging.warning('No combat log in %s' % logf.idstr)
        if logf.game_log:
            for l in logf.game_log.lines:
                if isinstance(l, dict):
                    rex_game['dict'] = rex_game.get('dict', 0) + 1
                    if not LOG_GOOD_ONLY and LOG_BAD_GAME:
                        x = l.get('log', None)
                        if x:
                            trash_log.info(x)
                        else:
                            logging.warning('Unknown dictionary: %s' % l)
                elif isinstance(l, str):
                    print(l)
                else:
                    if not l.unpack() or COUNT_GOOD:
                        rex_game[l.__class__.__name__] = rex_game.get(l.__class__.__name__, 0) + 1
                    if not LOG_GOOD_ONLY and LOG_BAD_GAME and not isinstance(l, game.GameLog):
                        trash_log.info((l.values['log']))
        else:
            logging.warning('No game log in %s' % logf.idstr)
        if logf.chat_log:
            for l in logf.chat_log.lines:
                if isinstance(l, dict):
                    rex_chat['dict'] = rex_chat.get('dict', 0) + 1 
                elif isinstance(l, str):
                    print(l)
                else:
                    if not l.unpack() or COUNT_GOOD:
                        rex_chat[l.__class__.__name__] = rex_chat.get(l.__class__.__name__, 0) + 1
                    if not LOG_GOOD_ONLY and LOG_BAD_CHAT and not isinstance(l, chat.ChatLog):
                        trash_log.info((l.values['log']))
        else:
            logging.warning('No chat log in %s' % logf.idstr)
        
        # Okay, parsing done.
        # default cleanup: will remove all dictionaries, trash logs, etc.
        logf.clean(True)
        # additional cleanup
        # we remove actually ALL log lines, as we are not interested in the data anymore.
        # this allows us to parse a lot more files
        if logf.chat_log:
            logf.chat_log.lines = []
        if logf.game_log:
            logf.game_log.lines = []
        if logf.combat_log:
            logf.combat_log.lines = []
    
    # Summary:
    logging.info('Analysis complete:')
    logging.info(('#'*20+' RexCombat ' + '#' *20))
    logging.info(rex_combat)
    logging.info(('#'*20+' RexGame ' + '#' *20))
    logging.info(rex_game)
    logging.info(('#'*20+' RexChat ' + '#' *20))
    logging.info(rex_chat)
