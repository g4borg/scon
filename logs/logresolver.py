"""
    Resolves Logs.
"""

from logfile import LogFile
from combat import COMBAT_LOGS

class LogFileResolver(LogFile):
    resolution_classes = COMBAT_LOGS
    
    def __init__(self, *args, **kwargs):
        super(LogFileResolver, self).__init__(*args, **kwargs)
        self.resolution_classes = self.resolution_classes or []
    
    def resolve(self, line):
        for klass in self.resolution_classes:
            if klass.is_handler(line):
                return klass(line)
        return line
