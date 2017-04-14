"""
    A LogStream is supposed to:
     - parse data feeded into it.
     - yield new objects
     - remember errors
    
    LogStream.Initialize:
     - initialize the logstream in some way.
    
    LogStream.Next:
     - once initialized, read your stream until you can yield a new class
     the next function reads the read-stream ahead.
     empty lines are omitted
     it tries to match the data into a new class and yields it
     if it runs into trouble, it just outputs the line for now.
    
    InitializeString:
     - init with a data blob
     - nice for trying it on files
    
    @TODO: look at how file streams in python are implemented and find a good generic solution
    combine it with the lookup for "watching files being changed", to create a program which listens to the logs live
    @see: monitor.py
    @see: watchdog https://pypi.python.org/pypi/watchdog
"""
from .base import Log
import re
from logs.base import Stacktrace
import logging
RE_SCLOG = r'^(?P<hh>\d{2,2})\:(?P<mm>\d{2,2})\:(?P<ss>\d{2,2})\.(?P<ns>\d{3,3})\s(?P<logtype>\s*[^\|\s]+\s*|\s+)\|\s(?P<log>.*)'
R_SCLOG = re.compile(RE_SCLOG) 

class LogStream(object):
    def __init__(self):
        self.lines = []
        self._data = None
        self._last_object = None
    
    def add_to_queue(self, line):
        # adds a line to the queue
        pass
    
    def new_packets(self, finish=False):
        # yields new packets.
        # processes the queue a bit.
        # yields new packets, once they are done.
        # watch out not to process the last packet until it has a follow up!
        # finish: override and yield all packets to finish.
        pass
    
    #####################################################################
    def has_data(self):
        if self._data:
            return True
    
    def set_data(self, data):
        self._data = data
    
    def get_data(self):
        return self._data
    
    def clean(self, remove_log=True):
        # cleans the logs by removing all non parsed packets.
        # remove_log: should i remove the raw log entry?
        lines = []
        for l in self.lines:
            if isinstance(l, Log):
                if l.unpack():
                    if not getattr(l, 'trash', False):
                        if remove_log:
                            l.clean()
                        lines.append(l)
                    else:
                        print type(l)
                        print l
        self.lines = lines
        self._unset_data()

    data = property(set_data, get_data)
    
    def _unset_data(self):
        self._data = None
        
    def pre_parse_line(self, line):
        if not isinstance(line, basestring):
            return line
        elif line.startswith('---'):
            return None
        elif line == '' or line == '\n':
            if line == '\n':
                logging.debug('Empty Newline detected.')
            return None
        else:
            # get the timecode & logtype
            m = R_SCLOG.match(line)
            if m:
                g = m.groupdict()
                if 'logtype' in g.keys():
                    g['logtype'] = g['logtype'].strip()
                return g
            else:
                return line
        return None
    
    def _parse_line(self, line):
        # add the line to my lines.
        if line is not None:
            o = line
            if isinstance(line, basestring):
                # Unknown Log?
                if not line:
                    return
                # It might be a stacktrace. inject it./
                if Stacktrace.is_handler(o):
                    o = Stacktrace(o)
                    self._last_object = o
                else:
                    #if isinstance(self._last_object, Stacktrace) and line.startswith('\t'):
                    #    logging.debug('Workaround: %s, worked: %s' % (line, self._last_object.append(line)))
                    #    return                        
                    if self._last_object is not None:
                        self._last_object.unpack()
                        if self._last_object.append(line):
                            return
                    logging.debug('#: %s' % line)
                    o = None
            elif isinstance(line, dict):
                # Unresolved Log.
                o = self.resolve(line)
                self._last_object = o
            else:
                self._last_object = o
            if o is None:
                self._last_object = None
                return
            self.lines.append(o)
    
    def parse_line(self, line):
        return self._parse_line(self.pre_parse_line(line))
    
    def resolve(self, gd):
        # gd is a dict.
        # try to find a class that is responsible for this log.
        return gd
