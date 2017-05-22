"""
    Represents a battle instance.
    
    todo: finding battles. factory for missions, skirmishes?
"""
from scon.logs import game, combat

# basic battle: responsible for managing, recognizing and parsing a single battle instance.
class Battle(object):
    _game_type_strings = []
    
    @classmethod
    def is_my_gametype(cls, gametype=None, level=None):
        if gametype:
            if gametype in cls._game_type_strings:
                return True
    
    def __init__(self, parent=None, gametype=None, level=None):
        # parent is a log-session
        self.parent = parent
        self.players = []
        self.teams = []
        self.time_start = None
        self.time_end = None
        self.owner = None
        self.live = False # whether this is a streamed object.
        self.level = level or ''
        self.gametype = gametype or ''
    
    def parse_details(self):
        # fast parse strategy: fill in all details about this battle.
        pass
    
    def parse_statistics(self):
        # parse battle statistics.
        pass
    
class PvPBattle(Battle):
    _game_type_strings = ['BombTheBase', 'Control', 'KingOfTheHill', 'CaptureTheBase', 'TeamDeathMatch', 'GreedyTeamDeathMatch', 'Sentinel']

class PvPTDM(PvPBattle):
    _game_type_strings = ['TeamDeathMatch', 'GreedyTeamDeathMatch' ]

class PvPDomination(PvPBattle):
    _game_type_strings = ['Control']

class PvPCombatRecon(PvPBattle):
    _game_type_strings = ['Sentinel']

class PvPCtB(PvPBattle):
    _game_type_strings = ['CaptureTheBase']

class PvPDetonation(PvPBattle):
    _game_type_strings = ['BombTheBase']

class PvPBeaconHunt(PvPBattle):
    _game_type_strings = ['KingOfTheHill']

# Dreads
class DreadnoughtBattle(Battle):
    _game_type_strings = ['ClanShip']

### PvE Stuff: low prio.
class PvEBattle(Battle):
    _game_type_strings = ['PVE_Mission',]

class PvERaidBattle(PvEBattle):
    pass

# Openspace time.
class Openspace(Battle):
    _game_type_strings = ['FreeSpace']
    pass

class UnknownBattle(Battle):
    @classmethod
    def is_my_gametype(cls, gametype=None, level=None):
        if gametype:
            return True

BATTLE_TYPES = [
    # here the more detailed ones
    PvPTDM, PvPDomination, PvPCombatRecon,
    PvPCtB, PvPDetonation, PvPBeaconHunt, 
    DreadnoughtBattle,
    PvEBattle, PvERaidBattle,
    # freespace, general pvp battle
    Openspace,
    PvPBattle,
    # unknowns:
    UnknownBattle          
    ]

###
def battle_factory(logs):
    ''' takes a log session and returns the battles in it 
        makes a preliminary scan for information
    '''
    battles = []
    battle = None
    if logs.game_log:
        # check game log
        for line in logs.game_log.lines:
            if isinstance(line, game.StartingLevel):
                if not line.unpack():
                    print('Encountered broken packet: ', line.values)
                    continue
                if not line.is_mainmenu():
                    # this is the beginning of a new battle.
                    if battle:
                        battles.append(battle)
                    
                    bklass = Battle
                    for klass in BATTLE_TYPES:
                        if klass.is_my_gametype(line.values.get('gametype', None), line.values.get('level', None)):
                            bklass = klass
                            break
                    if bklass:
                        battle = bklass(logs, line.values.get('gametype', None), line.values.get('level', None))
                    else:
                        battle = None
                else:
                    if battle:
                        battles.append(battle)
                        battle = None    
                
    return battles
    
        