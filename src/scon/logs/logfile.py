#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Author: Gabor Guzmics, 2013-2014
    
    LogFile is an object capable to load SCon Logfiles and parse their ingredients
    It can be extended by overriding resolve to understand Logentries further.
    Each Logfile represents a physical file parsed, however theoretically, you can also parse arbitrary
    data by setting the LogFile<instance>._data yourself.
"""
from .logstream import LogStream
import io, logging

class LogFile(LogStream):
    def __init__(self, fname=None,
                       folder=None):
        super(LogFile, self).__init__()
        self.fname = fname
        self.folder = folder # only for custom tagging.
        self._data = None
    
    def read(self, fname=None):
        fname = fname or self.fname
        try:
            f = io.open(fname, 'r', encoding="iso8859-1")
            self.set_data(f.read())
        except Exception as e:
            logging.error("Error %s reading file %s " % (e, fname, ))
        finally:
            f.close()
        
    def filter(self, klasses):
        ret = []
        for line in self.lines:
            for k in klasses:
                if isinstance(line, k):
                    ret.append(line)
                    break
        return ret
    
    def parse(self):
        # parse _data if we still have no lines.
        lines = []
        if self.has_data():
            data_lines = self.get_data(
                        ).replace('\r', '\n'
                        ).replace('\n\n', '\n'
                        ).split('\n'
                        )
            for line in data_lines:
                line = self.pre_parse_line(line)
                if not line:
                    continue
                else:
                    lines.append(line)
        elif self.lines:
            lines = self.lines
        if lines:
            for line in lines:
                self._parse_line(line)


