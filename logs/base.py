
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
