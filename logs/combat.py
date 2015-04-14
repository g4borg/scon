# -*- coding: utf-8 -*-

"""
    todo:
    - English implementation first.
    - parsing combat.log
    
    Prosa.
    All logs start with something like
    23:53:29.137        | LOGDATA 
    
    LOGDATA can be quite different depending on the logfile.
    
    other forms encountered:
    23:54:00.600 WARNING| 
    
    combat logs:
    01:04:38.805 CMBT   | 
    
    
    The typical log entry
"""
import re
from base import Log, L_CMBT, Stacktrace

class CombatLog(Log):
    __slots__ = Log.__slots__ + [ '_match_id', 'values']
    @classmethod
    def _log_handler(cls, log):
        if log.get('log', '').strip().startswith(cls.__name__):
            return True
        return False
    
    @classmethod
    def is_handler(cls, log):
        if log.get('logtype', None) == L_CMBT:
            return cls._log_handler(log)
        return False
    
    def __init__(self, values=None):
        self.values = values or {}
        self.reviewed = False
    
    def unpack(self, force=False):
        if self.reviewed and not force:
            return True
        self._match_id = None
        # unpacks the data from the values.
        if hasattr(self, 'matcher') and self.matcher:
            matchers = self.matcher
            if not isinstance(matchers, list):
                matchers = [matchers,]
            for i, matcher in enumerate(matchers):
                m = matcher.match(self.values.get('log', ''))
                if m:
                    self.values.update(m.groupdict())
                    self._match_id = i
                    self.reviewed = True
                    return True
        # unknown?
        self.trash = True
    
    def explain(self):
        ''' returns a String readable by humans explaining this Log '''
        return self.values.get('log', 'Unknown Combat Log')

                
# @todo: where does this come from?
class Action(CombatLog):
    __slots__ = CombatLog.__slots__
    pass

class Gameplay(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = [
        # usual: team(reason). explained reason.
        re.compile(r"^Gameplay\sfinished\.\sWinner\steam\:\s+(?P<winner_team>\d+)\((?P<winner_reason>\w+)\)\.\sFinish\sreason\:\s'(?P<reason_verbose>[^']+)'\.\sActual\sgame\stime\s+(?P<game_time>\d+|\d+\.\d+)\ssec"),
        # team, unexplained reason (unknown, Timeout)
        re.compile(r"^Gameplay\sfinished\.\sWinner\steam\:\s+(?P<winner_team>\d+).\sFinish\sreason\:\s'(?P<winner_reason>[^']+)'\.\sActual\sgame\stime\s+(?P<game_time>\d+|\d+\.\d+)\ssec"),
        ]

class Apply(CombatLog): # Apply Aura.
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^Apply\saura\s'(?P<aura_name>\w+)'\sid\s(?P<id>\d+)\stype\s(?P<aura_type>\w+)\sto\s'(?P<target_name>[^\']+)'")

class Damage(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^Damage\s+(?P<source_name>[^\s]+)\s\->\s+(?P<target_name>[^\s]+)\s+(?P<amount>(?:\d+|\d+\.\d+))(?:\s(?P<module_class>[^\s]+)\s|\s{2,2})(?P<flags>(?:\w|\|)+)")

class Spawn(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^Spawn\sSpaceShip\sfor\splayer(?P<player>\d+)\s\((?P<name>[^,]+),\s+(?P<hash>#\w+)\)\.\s+'(?P<ship_class>\w+)'")

class Spell(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^Spell\s'(?P<spell_name>\w+)'\sby\s+(?P<source_name>.*)(?:\((?P<module_name>\w+)\)|)\stargets\((?P<target_num>\d+)\)\:(?:\s(?P<targets>.+)|\s*)")

class Reward(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = [
        # ordinary reward:
        re.compile(r"^Reward\s+(?P<name>[^\s]+)(?:\s(?P<ship_class>\w+)\s+|\s+)(?P<amount>\d+)\s(?P<reward_type>.*)\s+for\s(?P<reward_reason>.*)"),
        # openspace reward (karma):
        re.compile(r"^Reward\s+(?P<name>[^\s]+)(?:\s(?P<ship_class>\w+)\s+|\s+)\s+(?P<karma>[\+\-]\d+)\skarma\spoints\s+for\s(?P<reward_reason>.*)"),
        ]

class Participant(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^\s+Participant\s+(?P<source_name>[^\s]+)(?:\s{2}(?P<ship_class>\w+)|\s{30,})\s+(?:totalDamage\s(?P<total_damage>(?:\d+|\d+\.\d+));\smostDamageWith\s'(?P<module_class>[^']+)';(?P<additional>.*)|<(?P<other>\w+)>)")

class Rocket(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^Rocket\s(?P<event>launch|detonation)\.\sowner\s'(?P<name>[^']+)'(?:,\s(?:def\s'(?P<missile_type>\w+)'|target\s'(?P<target>[^']+)'|reason\s'(?P<reason>\w+)'|directHit\s'(?P<direct_hit>[^']+)'))+")

class Heal(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = [
        # heal by module
        re.compile(r"^Heal\s+(?P<source_name>[^\s]+)\s\->\s+(?P<target_name>[^\s]+)\s+(?P<amount>(?:\d+|\d+\.\d+))\s(?P<module_class>[^\s]+)"),
        # direct heal by source or n/a (global buff)
        re.compile(r"^Heal\s+(?:n/a|(?P<source_name>\w+))\s+\->\s+(?P<target_name>[^\s]+)\s+(?P<amount>(?:\d+|\d+\.\d+))"),
        ]

class Killed(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = [
        re.compile(r"^Killed\s(?P<target_name>[^\s]+)\s+(?P<ship_class>\w+);\s+killer\s(?P<source_name>[^\s]+)\s*"),
        re.compile(r"^Killed\s(?P<object>[^\(]+)\((?P<target_name>\w+)\);\s+killer\s(?P<source_name>[^\s]+)\s*"),
        re.compile(r"^Killed\s(?P<object>[^\;]+);\s+killer\s(?P<source_name>[^\s]+)\s+.*"),
        ]

class Captured(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^Captured\s'(?P<objective>[^']+)'\(team\s(?P<team>\d+)\)\.(?:\sAttackers\:(?P<attackers>.*)|.*)")

class AddStack(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^AddStack\saura\s'(?P<spell_name>\w+)'\sid\s(?P<id>\d+)\stype\s(?P<type>\w+)\.\snew\sstacks\scount\s(?P<stack_count>\d+)")

class Cancel(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^Cancel\saura\s'(?P<spell_name>\w+)'\sid\s(?P<id>\d+)\stype\s(?P<type>\w+)\sfrom\s'(?P<source_name>[^']*)'")

class Scores(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^Scores\s+-\sTeam1\((?P<team1_score>(?:\d+|\d+\.\d+))\)\sTeam2\((?P<team2_score>(?:\d+|\d+\.\d+))\)")
    
# Special classes
class GameEvent(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = [
        # game session identifier.
        re.compile(r"^Connect\sto\sgame\ssession\s+(?P<game_session>\d+)"),
        # start gameplay identifier.
        re.compile(r"^Start\sgameplay\s'(?P<gameplay_name>\w+)'\smap\s+'(?P<map_id>\w+)',\slocal\sclient\steam\s(?P<local_team>\d+)"),
        # pve mission identifier.
        re.compile(r"^Start\sPVE\smission\s'(?P<pve_name>\w+)'\smap\s+'(?P<map_id>\w+)'"),
       ]
    
    @classmethod
    def _log_handler(cls, log):
        if log.get('log', '').strip().startswith('======='):
            return True
        return False
    
    def unpack(self, force=False):
        if self.reviewed and not force:
            return True
        self._match_id = None
        # unpacks the data from the values.
        # small override to remove trailing "="s in the matching.
        if hasattr(self, 'matcher') and self.matcher:
            matchers = self.matcher
            if not isinstance(matchers, list):
                matchers = [matchers,]
            for i, matcher in enumerate(matchers):
                m = matcher.match(self.values.get('log', '').strip('=').strip())
                if m:
                    self.values.update(m.groupdict())
                    self._match_id = i
                    self.reviewed = True
                    return True
        # unknown?
        self.trash = True
    
    def clean(self):
        if 'log' in self.values.keys():
            del self.values['log']

class PVE_Mission(CombatLog):
    """
    PVE_Mission: 'bigship_building_normal'. start round 1/3
    PVE_Mission: 'bigship_building_normal'. round 1/3. start wave 1/3
    PVE_Mission: 'bigship_building_normal'. round 1/3. start wave 2/3
    PVE_Mission: 'bigship_building_normal'. round 1/3. start wave 3/3
    """
    __slots__ = CombatLog.__slots__
    matcher = [] # @TODO: do this.

class Looted(CombatLog):
    """
    Looted 'ow_Mineral_Info_T3_1' from 'LootCrate_Crystal1'
    Looted 'Junk_Fuel7' from 'LootCrate_Fuel_Dynamic'
    Looted 'ow_Afterburner_catalyst' from 'LootCrate_T3_Junk'
    """
    __slots__ = CombatLog.__slots__
    matcher = [] # @TODO: do this.

class UserEvent(CombatLog):
    """ special class for combat logs that might be associated with the playing player """
    __slots__ = CombatLog.__slots__
    @classmethod
    def _log_handler(cls, log):
        line =  log.get('log', '').strip()
        if line and 'earned medal' in line:
            return True
        elif line:
            print line
        return False

# Action?
COMBAT_LOGS = [ Apply, Damage, Spawn, Spell, Reward, Participant, Rocket, Heal, 
               Gameplay, #?
               Scores,
               Killed, Captured, AddStack, Cancel,
               PVE_Mission, Looted,
               GameEvent, UserEvent,
               Stacktrace,
               ]

