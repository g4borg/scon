import os
import platform

class Settings(dict):
    def autodetect(self, path=None):
        # autodetect settings.
        d = path
        system = platform.system()
        if system == 'Windows' or system.startswith('CYGWIN_NT'):
            # try to find user folder:
            d = d or os.path.join(os.path.expanduser('~'),
                                     'Documents',
                                     'My Games',
                                     'StarConflict',)
        elif system == 'Linux':
            raise NotImplementedError, "Implement Linux!"
        elif system == 'Darwin':
            raise NotImplementedError, "Implement Mac!"
        else:
            raise NotImplementedError, "Unknown System! %s" % platform.system()
        if not os.path.exists(d) or not os.path.isdir(d):
            raise Exception, "Configuration Autodetection failed. "
        self['root_path'] = d
        
    def get_path(self):
        return self.get('root_path', None)
    
    def get_logs_path(self):
        return os.path.join(self.get_path, 'logs')

settings = Settings()
