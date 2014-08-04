#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Resolves Logs.
"""

from logfile import LogFile
from combat import COMBAT_LOGS
from game import GAME_LOGS

class LogFileResolver(LogFile):
    ''' dynamic logfile resolver '''
    resolution_classes = COMBAT_LOGS
    
    def __init__(self, *args, **kwargs):
        super(LogFileResolver, self).__init__(*args, **kwargs)
        self.resolution_classes = self.resolution_classes or []
    
    def resolve(self, line):
        for klass in self.resolution_classes:
            if klass.is_handler(line):
                return klass(line)
        return line

class CombatLogFile(LogFile):
    ''' Combat Log '''
    def resolve(self, line):
        for klass in COMBAT_LOGS:
            if klass.is_handler(line):
                return klass(line)
        return line

class GameLogFile(LogFile):
    ''' Game Log '''
    def resolve(self, line):
        for klass in GAME_LOGS:
            if klass.is_handler(line):
                return klass(line)
        return line

