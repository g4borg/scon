import logging
"""
    Base Class for a Logentry is Log. Stacktrace is an exception, which gets injected if a stacktrace 
    is assumed, and swallows all following unrecognized logs.
    
    -> It gets parsed by a Logstream, like the Logfile, but might also be used to be feeded 
       by live-streams of currently open log files.
    
    -> Logfiles is responsible to read whole packs of files, and 
    -> Sessions are responsible for reading whole directories.
    
    A Log object usually will expand itself containing "values", and is responsible to retain all dynamic data needed to describe it in unpack()
    The classmethod is_handler should pre-scan a log, which is usually a dict containing the actual log in log['log']
    but it could be a string aswell.
    
    clean is called to make a log object independent of its source information, and delete all incoming data, so it becomes sleek.
    reviewed is an internal boolean, which supposed to be saved on successful unpack, unpack should ignore already unpacked logs.
    matcher is a regex object to match, or a list of them.
    trash is a boolean flag to indicate, this log is possibly unknown information or unneeded, and should be removed or ignored.
    
    -> Note for anyone creating new subclasses for parsing: 
        All classes are to be __slot__-ed so they can be created more efficiently by python. 
        A class without __slot__ will slow down parsing exponentially in CPython. 
        __slots__ hinder you to add new properties on the fly in the code, but having this immutable class optimizes memory allocation.
        
        This is the reason, the base layout of the log object is explained here.
"""

import datetime

L_CMBT = 'CMBT'
L_WARNING = 'WARNING'
L_NET = 'NET' # Not supported in near future.
L_CHAT = 'CHAT'

class Log(object):
    __slots__ = ['trash', 'reviewed', '_match_id', 'values', '_timestamp']
    matcher = None
    
    def __init__(self):
        self.trash = False
        self.reviewed = False
        self.values = None
        self._match_id = None
        self._timestamp = None
    
    @classmethod
    def is_handler(cls, log):
        return False
    
    @property
    def timestamp(self):
        if self._timestamp:
            return self._timestamp
        # build timestamp:
        # datetime.time(hour[, minute[, second[, microsecond[, tzinfo]]]])
        _time = datetime.time( int(self.values.get('hh')),
                               int(self.values.get('mm')),
                               int(self.values.get('ss', 0)),
                               int(self.values.get('ns', 0)) )
        self._timestamp = _time
        return _time
    
    def unpack(self, force=False):
        ''' unpacks this log from its data and saves values '''
        pass
    
    def explain(self):
        ''' returns a String readable by humans explaining this Log '''
        return ''
    
    def clean(self):
        ''' tell the log to forget all non-essential data '''
        pass
    
    def append(self, something):
        ''' returns true if this logfile wants an unrecognized log appended to it. '''
        return False

class Stacktrace(Log):
    ''' Special Log to catch error reports 
        -> holds data in message not in values.
        -> makes use of append
    '''
    __slots__ = ['trash', 'reviewed', 'message', '_match_id', 'values']
    
    def __init__(self, values=None):
        super(Stacktrace, self).__init__()
        self.message = values or ''
        if isinstance(self.message, dict):
            self.message = self.message.get('log', '')
        #self.trash = True
    
    @classmethod
    def is_handler(cls, log):
        # do i have a system crash report beginning here?
        if isinstance(log, str):
            l = log.strip()
        elif isinstance(log, dict):
            l = log.get('log', '').strip()
        else:
            return False
        if l.startswith('Stack trace:') or l.startswith('BitStream::DbgLog'):
            return True
    
    def clean(self):
        self.message = ''
    
    def append(self, something):
        ''' I take anything! '''
        logging.debug( "EXC: %s" % something )
        self.message = '%s\n%s' % (self.message, something)
        return True