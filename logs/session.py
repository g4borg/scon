"""
    Logging Session.
"""
import zipfile, logging, os
from logfiles import CombatLogFile, GameLogFile

class LogSession(object):
    """
        The Log-Session is supposed to save one directory of logs.
        It can parse its logs, and build up its internal structure into Battle Instances etc.
    """
    
    def __init__(self, directory):
        ''' if directory is a file, it will be handled as a compressed folder '''
        self.battles = []
        self.user = None
        
        # various logfiles used.
        self.combat_log = None
        self.game_log = None
        self.chat_log = None
        # self.net_log = None
        
        self.directory = directory
        self._zip_source = False
    
    def parse_files(self):
        ''' parses the logfiles '''
        # check if directory is a file
        self._zip_source = os.path.isfile(self.directory) or False
        if self._zip_source:
            self._unzip_logs()
        else:
            self.combat_log = CombatLogFile(os.path.join(self.directory, 'combat.log'))
            self.combat_log.read()
            self.game_log = GameLogFile(os.path.join(self.directory, 'game.log'))
            self.game_log.read()
        # parse all files
        self.combat_log.parse()
        self.game_log.parse()
    
    def determine_owner(self):
        ''' determines the user in the parsed gamelog '''
        pass
    
    def parse_battles(self):
        ''' parses the battles '''
        pass
    
    def _unzip_logs(self):
        z = zipfile.ZipFile(self.directory, "r")
        for filename in z.namelist():
            fn = os.path.split(filename)[1] or ''
            fn = fn.lower()
            if fn:
                if fn == 'combat.log':
                    self.combat_log = CombatLogFile(fn)
                    self.combat_log.set_data(z.read(filename))
                elif fn == 'game.log':
                    self.game_log = GameLogFile(fn)
                    self.game_log.set_data(z.read(filename))
                


if __name__ == '__main__':
    l_raw = LogSession('D:\\Users\\g4b\\Documents\\My Games\\sc\\2014.05.17 15.50.28')
    l_zip = LogSession('D:\\Users\\g4b\\Documents\\My Games\\sc\\2014.05.20 23.49.19.zip')
    
    l_zip.parse_files()
    print l_zip.combat_log.lines