import logging

L_CMBT = 'CMBT'
L_WARNING = 'WARNING'
L_NET = 'NET'
L_CHAT = 'CHAT'

class Log(object):
    __slots__ = ['matcher', 'trash', 'reviewed']
    matcher = None
    trash = False
    reviewed = False
    
    @classmethod
    def is_handler(cls, log):
        return False
    
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
    ''' Special Log to catch error reports '''
    def __init__(self, values=None):
        super(Stacktrace, self).__init__()
        self.message = values or ''
        if isinstance(self.message, dict):
            self.message = self.message.get('log', '')
        #self.trash = True
    
    @classmethod
    def is_handler(cls, log):
        # do i have a system crash report beginning here?
        if isinstance(log, basestring):
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