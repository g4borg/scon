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
        
        
        battles = battle_factory(logf)
        
        if len(battles) < 1:
            # skip this
            continue
        
        for battle in battles:
            print(battle.level)
        
        combat_log_lines, game_log_lines = (0, 0)
        
        if logf.combat_log:
            combat_log_lines = len(logf.combat_log.lines)
        if logf.game_log:
            game_log_lines = len(logf.game_log.lines)
        
        logf.clean()
        
        if logf.combat_log:
            print('combat.log: %s lines were eliminated during cleaning (%s -> %s)' % ( combat_log_lines - len(logf.combat_log.lines),
                          combat_log_lines,
                          len(logf.combat_log.lines),
                          ) )
        if logf.game_log:
            print('game.log: %s lines were eliminated during cleaning (%s -> %s)' % ( game_log_lines - len(logf.game_log.lines),
                          game_log_lines,
                          len(logf.game_log.lines),
                          ) )
        