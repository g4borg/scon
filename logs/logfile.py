#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Author: Gabor Guzmics, 2013-2014
    
    LogFile is an object capable to load SCon Logfiles and parse their ingredients
    It can be extended by overriding resolve to understand Logentries further.
    Each Logfile represents a physical file parsed, however theoretically, you can also parse arbitrary
    data by setting the LogFile<instance>._data yourself.
"""
import re
RE_SCLOG = r'^(?P<hh>\d{2,2})\:(?P<mm>\d{2,2})\:(?P<ss>\d{2,2})\.(?P<ns>\d{3,3})\s(?P<logtype>\s*[^\|\s]+\s*|\s+)\|\s(?P<log>.*)'
R_SCLOG = re.compile(RE_SCLOG) 

class LogFile(object):
    def __init__(self, fname=None,
                       folder=None):
        self.fname = fname
        self.folder = folder # only for custom tagging.
        self.lines = []
        self._data = None
    
    def read(self, fname=None):
        fname = fname or self.fname
        try:
            f = open(fname, 'r')
            self._data = f.read()
        finally:
            f.close()
        
    def set_data(self, data):
        self._data = data
    
    def _unset_data(self):
        self._data = None
    
    def parse(self):
        # parse _data if we still have no lines.
        if self._data:
            data_lines = self._data.replace('\r', '\n').replace('\n\n', '\n').split('\n')
            lines = []
            for line in data_lines:
                if not line:
                    continue
                elif not isinstance(line, basestring):
                    lines.append(line)
                    continue
                elif line.startswith('---'):
                    continue
                else:
                    # get the timecode & logtype
                    m = R_SCLOG.match(line)
                    if m:
                        g = m.groupdict()
                        if 'logtype' in g.keys():
                            g['logtype'] = g['logtype'].strip()
                        lines.append(g)
                    else:
                        lines.append(line)
            self.lines = lines
        # try to identify (resolve) lines.
        if self.lines:
            lines = []
            for line in self.lines:
                l = line
                if isinstance(line, basestring):
                    # Unknown Log?
                    pass
                elif isinstance(line, dict):
                    # Unresolved Log.
                    l = self.resolve(line)
                elif line is None:
                    # dafuq?
                    pass
                else:
                    # might be an object?
                    pass
                lines.append(l)
                
            self.lines = lines
    
    def resolve(self, line):
        # line is a dict.
        # try to find a class that is responsible for this log.
        return line

