#
#
#
"""
    Screener Module.
    
    Upon receiving a logfile, the screener module tries a first pass to retrieve the informations:
     - who am i? am i in steam? 
     - which os do i use? whats the date? other specifics?
     - battles, when did they begin, when did they end, which players were in it, which teams (game.log)
    
    It should act as a factory for a second, more in depth parsing mechanism, which can retrieve and
    manage the rest of the details.
     
"""
class Information:
    def __init__(self):
        self.steam_id = None # steam id
        self.steam_username = None # optional steam username.
        self.username = None # ingame username.
        self.uid = None # does not change.
        self.pid = None # changes per battle. needed once to identify pilot.
        
        
        
class Screener(object):
    def __init__(self):
        pass