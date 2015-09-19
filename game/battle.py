"""
    Represents a battle instance.
    
    todo: finding battles. factory for missions, skirmishes?
"""

# basic battle: responsible for managing, recognizing and parsing a single battle instance.
class Battle(object):
    def __init__(self, parent=None):
        # parent is a log-session usually
        self.players = []
        self.teams = []
        self.time_start = None
        self.time_end = None
        self.owner = None
        self.live = False # whether this is a streamed object.
        self.map = None
    
    def parse_details(self):
        # fast parse strategy: fill in all details about this battle.
        pass
    
    def parse_statistics(self):
        # parse battle statistics.
        pass
    
class PvPBattle(Battle):
    pass

class PvPTDM(PvPBattle):
    pass

class PvPDomination(PvPBattle):
    pass

class PvPCombatRecon(PvPBattle):
    pass

class PvPCtB(PvPBattle):
    pass

class PvPDetonation(PvPBattle):
    pass

class PvPBeaconHunt(PvPBattle):
    pass

# Dreads
class DreadnoughtBattle(Battle):
    pass

### PvE Stuff: low prio.
class PvEBattle(Battle):
    pass

class PvERaidBattle(PvEBattle):
    pass

# Openspace time.
class Openspace(Battle):
    pass


###
def battle_factory(logs):
    ''' takes a log session and returns the battles in it 
        makes a preliminary scan for information
    '''
    
    if logs.combat_log and logs.game_log:
        # without these it does not make sense
        # check combat_log
        
        pass
    return []
    
        