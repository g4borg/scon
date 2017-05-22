import os
import platform

class Settings(dict): 
    # note that settings is a dict.
    def autodetect(self, path=None):
        """ autodetects config_path, returns True on success.
            if a path is given, it is set to it, as far as it exists.
        """
        # this code is mostly in here to remember how to check Operation Systems,
        # if the project ever needs releasable binaries.
        # following code tries autodetecting star conflict user file folder
        # 
        d = path
        system = platform.system()
        if system == 'Windows' or system.startswith('CYGWIN_NT'):
            # try to find user folder:
            d = d or os.path.join(os.path.expanduser('~'),
                                     'Documents',
                                     'My Games',
                                     'StarConflict',)
        elif system == 'Linux':
            d = d or os.path.join(os.path.expanduser('~'), '.local', 'share', 'starconflict')
        elif system == 'Darwin':
            if not d:
                raise NotImplementedError("Implement Mac!")
        else:
            if not d:
                raise NotImplementedError("Unknown System! %s" % platform.system())
        if not os.path.exists(d) or not os.path.isdir(d):
            return False
        self['config_path'] = os.path.abspath(d)
        return True
        
    def get_config_path(self):
        """ gets the config_path if set, otherwise None. """
        return self.get('config_path', None)
    
    def get_logs_path(self):
        """ gets the logfolder in the config_path or None. """
        p = self.get_config_path()
        if p:
            return os.path.join(p, 'logs')
        return None

settings = Settings()
