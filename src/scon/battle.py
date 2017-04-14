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
    for logf in coll.sessions:
        logf.parse_files(['game.log', 'combat.log'])
        logf.clean()
        if logf.combat_log:
            print 'length combat log ', len(logf.combat_log.lines)
        if logf.game_log:
            print 'length game log ', len(logf.game_log.lines)