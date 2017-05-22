
import os, sys, codecs, locale
import platform
import logging
FALLBACK = 'iso8859-1'

class Settings(dict): 
    # note that settings is a dict.
    def autodetect(self, path=None):
        """ autodetects config_path and default_encoding, returns True on success.
            if a path is given, it is set to it, as far as it exists.
        """
        # default encoding for text files, however even at cp1252 used at some chats, iso8859-1 seems working best.
        #self['default_encoding'] = locale.getpreferredencoding()
        self['default_encoding'] = FALLBACK
        
        
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
            logging.error('Autodetection: log path %s does not exist.' % d)
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
    
    def detect_encoding(self, filename=None, ):
        """ Detecting the encoding of a file, or generally """
        # given atm this is called by every file once, for speed reasons, this has to be refactored later.
        if filename is None or not self.get('use_chardet', False):
            # default if filename is none: return self['default_encoding'] or iso8859-1
            return self.get('default_encoding', FALLBACK)
        else:
            # if a filename is given, we could use chardet.
            # atm we only use it to debug this process if use_chardet is true
            if not self.get('use_chardet', False):
                return self.get('default_encoding', FALLBACK)
            try:
                cde = self.detect_encoding_chardet(filename, quick=True)
                default_encoding = self.get('default_encoding', FALLBACK)
                if cde == default_encoding:
                    logging.info('Logfile %s has encoding %s' % (filename, cde))
                else:
                    logging.warning('Logfile %s has a different encoding than %s, being %s' % (filename, default_encoding, cde))
                return cde
            except:
                import traceback
                traceback.print_exc()
                return self.get('default_encoding', FALLBACK)
    
    def detect_encoding_chardet(self, filename, detector=None, quick=False):
        """ Detect file encoding with chardet.
            This is an experimental utility function.
            Returns iso8859-1 if even chardet fails, as i assume its the standard encoding used in log engine.
            Returns default_encoding entry if chardet is not installed, or else, yet again iso8859-1
        """
        try:
            from chardet.universaldetector import UniversalDetector
        except ImportError:
            logging.error('Chardet is not installed.')
            return self.get('default_encoding', FALLBACK)
        detector = detector or UniversalDetector()
        detector.reset()
        det_tresh = 0
        with open(filename, 'rb') as file:
            for line in file:
                detector.feed(line)
                if detector.done:
                    break
                else:
                    det_tresh +=1
                if det_tresh > 100 and quick:
                    break
                elif det_tresh > 10000:
                    logging.error("Detector is too hungry")
                    break
        detector.close()
        try:
            return codecs.lookup( detector.result.get('encoding', FALLBACK) ).name
        except LookupError:
            return detector.result.get('encoding', FALLBACK)

# this acts as a singleton. modify it from here.
settings = Settings()

if __name__ == '__main__':
    # test this.
    if settings.autodetect():
        print("Settings was autodetected.")
        print("Config Path is %s" % settings.get_config_path())
    else:
        print("Settings was not autodetected :(")
        sys.exit(1)
    
    try:
        import chardet
        settings['use_chardet'] = True
    except ImportError:
        pass
    
    # http://www.i18nqa.com/debug/table-iso8859-1-vs-windows-1252.html
    # This makes it sound easy.
    
    # it may  be that its by default cp1252, which is the locale preferred encoding given by locale on my system.
    # on the other hand, python uses charmap for that, which fails on some bytes, iso8859-1 can handle.
    # no wonder, the detector detects iso8859-1 for most log files i scanned, except a few chats in cp1252
    # it may be, that this is also related to windows updates and my habit of scanning old data aswell, it may also be that sc uses a hardcoded encoding
    
    # now some tests for encoding detection
    print('Locale Get Preferred Encoding is ', locale.getpreferredencoding())
    print('File System Encoding is ', sys.getfilesystemencoding())
    
    print('The UserConfig xml is saved as ', settings.detect_encoding(os.path.join(settings.get_config_path(),
                                               'user_config.xml')))
    
    
    print('Found Log file saved as ', settings.detect_encoding(os.path.join(settings.get_logs_path(),
    # note: you need to add a logfile here.
    '2017.03.17 12.02.13',
                                               'combat.log')))
    