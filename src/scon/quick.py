#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Script to quickly test recent logs
    
"""
import os, sys, logging
from scon.logs.logfiles import LogFileResolver as LogFile
from scon.logs import combat, game, chat
from scon.logs.session import LogSessionCollector
from scon.logs.game import ClientInfo
from scon.game.battle import battle_factory
from scon.config.settings import settings

settings.autodetect()

if __name__ == '__main__':
    coll = LogSessionCollector(settings.get_logs_path())
    coll.collect_unique()
    for logf in coll.sessions:
        print (logf.idstr)
        logf.parse_files(['game.log', 'combat.log'])
        
        if logf.combat_log:
            print(('length combat log ', len(logf.combat_log.lines)))
        if logf.game_log:
            print(('length game log ', len(logf.game_log.lines)))
        print(battle_factory(logf))
        
        print ("Cleaning.")
        logf.clean()
        if logf.combat_log:
            print(('length combat log ', len(logf.combat_log.lines)))
        if logf.game_log:
            print(('length game log ', len(logf.game_log.lines)))
        