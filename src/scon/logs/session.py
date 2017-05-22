"""
    Logging Session.
"""
import zipfile, logging, os, io
from .logfiles import CombatLogFile, GameLogFile, ChatLogFile
from scon.config.settings import settings

class LogSession(object):
    """
        A basic logsession.
        deal with data as it comes along, and output interpretable data for the outside world.
        
    """
    pass

class LogFileSession(LogSession):
    """
        The Log-File-Session is supposed to save one directory of logs.
        It can parse its logs, and should become able to build up its internal 
        structure into Battle Instances etc.
    """
    VALID_FILES = ['combat.log', 'game.log', 'chat.log' ] # extend this to other logs.
    
    def __init__(self, directory):
        ''' if directory is a file, it will be handled as a compressed folder '''
        self.battles = []
        self.user = None
        self.files_parsed = []
        
        # various logfiles used.
        self.combat_log = None
        self.game_log = None
        self.chat_log = None
        # self.net_log = None
        
        self.directory = directory
        self._zip_source = None
        self.idstr = None # id string to identify this log instance.
        self._error = False
    
    def clean(self, remove_log=True):
        if self.combat_log:
            self.combat_log.clean(remove_log)
        if self.game_log:
            self.game_log.clean(remove_log)
        if self.chat_log:
            self.chat_log.clean(remove_log)
        
    
    def validate(self, contents=False):
        """ 
          - validates if the logfiles are within this package.
          - sets the idstr of this object.
          @todo: in-depth validation of logs, on contents=True.
        """
        self._zip_source = os.path.isfile(self.directory) or False
        v = False
        try:
            if self._zip_source:
                v = self._unzip_validate()
                if v > 0:
                    self.idstr = os.path.split(self.directory)[1].replace('.zip', '').lower()
            else:
                v = self._validate_files_exist()                
                if v > 0:
                    self.idstr = os.path.split(self.directory)[1].lower()
        except Exception as e:
            logging.error("exception in logfilesession.validate %s" % e)
            return False
        return v            
    
    def parse_files(self, files=None):
        ''' parses the logfiles '''
        # perform simple validation.
        if self._zip_source is None:
            logging.error('_zip_source is None!')
            self.validate(False)
        if self._zip_source:
            self._unzip_logs(files)
        else:
            if files is None:
                files = self.VALID_FILES
            if 'combat.log' in files and not 'combat.log' in self.files_parsed:
                self.combat_log = CombatLogFile(os.path.join(self.directory, 'combat.log'))
                self.combat_log.read()
                self.combat_log.parse()
                self.files_parsed.append('combat.log')
            if 'game.log' in files and not 'game.log' in self.files_parsed:
                self.game_log = GameLogFile(os.path.join(self.directory, 'game.log'))
                self.game_log.read()
                self.game_log.parse()
                self.files_parsed.append('game.log')
            if 'chat.log' in files and not 'chat.log' in self.files_parsed:
                self.chat_log = ChatLogFile(os.path.join(self.directory, 'chat.log'))
                self.chat_log.read()
                self.chat_log.parse()
                self.files_parsed.append('chat.log')
    
    def determine_owner(self):
        ''' determines the user in the parsed gamelog '''
        pass
    
    def parse_battles(self):
        ''' parses the battles '''
        pass
    
    def _unzip_logs(self, files=None):
        z = zipfile.ZipFile(self.directory, "r")
        try:
            for filename in z.namelist():
                fn = os.path.split(filename)[1] or ''
                fn = fn.lower()
                if fn:
                    if fn == 'combat.log' and (not files or fn in files) and not 'combat.log' in self.files_parsed:
                        self.combat_log = CombatLogFile(fn)
                        self.combat_log.set_data(io.TextIOWrapper(io.BytesIO(z.read(filename)), encoding=settings.detect_encoding()).read())
                        self.combat_log.parse()
                        self.files_parsed.append('combat.log')
                    elif fn == 'game.log' and (not files or fn in files) and not 'game.log' in self.files_parsed:
                        self.game_log = GameLogFile(fn)
                        self.game_log.set_data(io.TextIOWrapper(io.BytesIO(z.read(filename)), encoding=settings.detect_encoding()).read())
                        self.game_log.parse()
                        self.files_parsed.append('game.log')
                    elif fn == 'chat.log' and (not files or fn in files) and not 'chat.log' in self.files_parsed:
                        self.chat_log = ChatLogFile(fn)
                        self.chat_log.set_data(io.TextIOWrapper(io.BytesIO(z.read(filename)), encoding=settings.detect_encoding()).read())
                        self.chat_log.parse()
                        self.files_parsed.append('chat.log')
        except Exception as e:
            self._error = True
            logging.error('_unzip logs encountered error %s' % e)
            raise
        finally:
            z.close()
    
    def _unzip_validate(self):
        z = zipfile.ZipFile(self.directory, "r")
        found = 0
        for filename in z.namelist():
            fn = os.path.split(filename)[1] or ''
            fn = fn.lower()
            if fn and fn in self.VALID_FILES:
                found += 1
        z.close()
        return found
    
    def _validate_files_exist(self):
        found = 0
        for f in self.VALID_FILES:
            if os.path.exists(os.path.join(self.directory, f)):
                found += 1
        return found

class LogSessionCollector(object):
    """
        finds sessions in a directory, a.k.a. you load the log directories
        of SC into sessions.
        
        - find_sessions: only find and instantiate sessions.
        - collect: validates each found session and returns them as list.
        - collect_unique: instead of a list, a dict is returned, where each
        session can be accessed via its idstr. does not parse/validate sessions.
    """
    def __init__(self, directory):
        self.initial_directory = directory
        self.sessions = []
        self.find_sessions()
    
    def find_sessions(self):
        for f in os.listdir(self.initial_directory):
            full_dir = os.path.join(self.initial_directory, f)
            if os.path.isdir(full_dir) or full_dir.lower().endswith('.zip'):
                self.sessions.append(LogFileSession(full_dir))
    
    def collect(self):
        sessions = []
        for session in self.sessions:
            try:
                if session.validate():
                    sessions.append(session)       
            except:
                continue
        return sessions
    
    def collect_unique(self):
        ''' collects all sessions into a dictionary ordered by their idstr.
            sessions without idstr, or already existing (first served) are omitted
            parsing is not done.
        '''
        # note this function resets sessions to the working ones.
        self.sessions = self.collect()
        sessions_dict = {}
        for session in self.sessions:
            if session.idstr and not session.idstr in list(sessions_dict.keys()):
                sessions_dict[session.idstr] = session
        return sessions_dict
    
    def clean(self, remove_log=True):
        for session in self.sessions:
            session.clean(remove_log)
        
        


if __name__ == '__main__':
    l_raw = LogFileSession('D:\\Users\\g4b\\Documents\\My Games\\sc\\2014.05.17 15.50.28')
    l_zip = LogFileSession('D:\\Users\\g4b\\Documents\\My Games\\sc\\2014.05.20 23.49.19.zip')
    
    l_zip.parse_files()
    print((l_zip.combat_log.lines))
    
    collector = LogSessionCollector('D:\\Users\\g4b\\Documents\\My Games\\sc\\')
    print((collector.collect_unique()))