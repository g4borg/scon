"""
    Represents a battle instance.
    
    todo: finding battles. factory for missions, skirmishes?
"""

class Battle(object):
    def __init__(self, parent=None):
        # parent is a log-session usually
        self.players = []
        self.teams = []
        self.time_start = None
        self.time_end = None
        self.owner = None
    

def battle_factory(logs):
    ''' takes a log session and returns the battles in it 
        makes a preliminary scan for information
    '''
    
    if logs.combat_log and logs.game_log:
        # without these it does not make sense
        # check combat_log
        
        pass
    return []
    
        