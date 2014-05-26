"""
    Brainstorm File for Star Conflict Log Parsing
    
    Needed
     - find steam/scon folder on windows
     - find steam/scon folder on mac
     - find steam/scon folder on linux
     - what about steamless installs?
    
    Elaborate
     - which GUI to use? wx? PyQt4? PySide?
     - take over the database stuff from weltenfall.starconflict?
    
    Investigate
     - language based log files?
"""
#from win32com.shell import shell, shellcon
import os, sys, logging
from logs.logresolver import LogFileResolver as LogFile
from logs import combat

# for windows its kinda this:
settings = {'logfiles': os.path.join(os.path.expanduser('~'),
                                     'Documents',
                                     'My Games',
                                     'StarConflict',
                                     'logs'
                                     )}

def find_log_files(logpath):
    ''' returns a list of 4-tuples representing
       (combat.log, game.log, chat.log, game.net.log)
       for each directory in the logpath
    '''
    ret = []
    for directory in os.listdir(logpath):
        full_dir = os.path.join(logpath, directory)
        if os.path.isdir(full_dir):
            if  os.path.exists(os.path.join(full_dir, 'combat.log'))\
            and os.path.exists(os.path.join(full_dir, 'game.log'))\
            and os.path.exists(os.path.join(full_dir, 'chat.log'))\
            and os.path.exists(os.path.join(full_dir, 'game.net.log')):
                ret.append((
                        os.path.join(full_dir, 'combat.log'),
                        os.path.join(full_dir, 'game.log'),
                        os.path.join(full_dir, 'chat.log'),
                        os.path.join(full_dir, 'game.net.log')
                        ))
    return ret

def parse_games(logfiles):
    _logfiles = []
    for logpack in logfiles:
        combatlog, gamelog, chatlog, gamenetlog = logpack
        _logfiles.append(LogFile(combatlog))
        #_logfiles.append(LogFile(gamelog))
        #_logfiles.append(LogFile(chatlog))
        #_logfiles.append(LogFile(gamenetlog))
    return _logfiles

if __name__ == '__main__':
    logfiles = find_log_files(settings['logfiles'])
    logfiles = parse_games(logfiles)
    #f = open('output.txt', 'w')
    rex = {}
    for logf in logfiles:
        logf.read()
        logf.parse()
        for l in logf.lines:
            if isinstance(l, dict):
                #print l
                pass
            else:
                if not l.unpack():
                    rex[l.__class__.__name__] = rex.get(l.__class__.__name__, 0) + 1
                    if not isinstance(l, combat.UserEvent):
                        print l.values['log']
                #f.write(l.values['log'] + '\n')
    #f.close()
            #print type(l)
    print rex