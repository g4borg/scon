
L_CMBT = 'CMBT'
L_WARNING = 'WARNING'
L_NET = 'NET'
L_CHAT = 'CHAT'

class Log(object):
    matcher = None
    trash = False
    
    @classmethod
    def is_handler(cls, log):
        return False
    
    def unpack(self):
        pass
