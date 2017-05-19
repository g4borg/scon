# -*- coding: utf-8 -*-
"""
    Primary Packets for Combat.Log Files.
    
    This is the most important part for dealing with actual statistics, since every action taken
    in a combat instance gets logged here.
    
    
    ------------------------------------
    Note:
    All logs start with something like
    23:53:29.137        | LOGDATA 
    
    LOGDATA can be quite different depending on the logfile.
    
    other forms encountered:
    23:54:00.600 WARNING| 
    
    combat logs:
    01:04:38.805 CMBT   | 
"""
import re
from .base import Log, L_CMBT, Stacktrace
import logging
trash_log = logging.getLogger('trash_log')

class CombatLog(Log):
    __slots__ = Log.__slots__
    @classmethod
    def _log_handler(cls, log):
        if log.startswith(cls.__name__):
            return True
        return False
    
    @classmethod
    def is_handler(cls, log):
        if log.get('logtype', None) == L_CMBT:
            return cls._log_handler(log.get('log', '').strip())
        return False
    
    def __init__(self, values=None):
        super(CombatLog, self).__init__()
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
        if not isinstance(self, UserEvent):
            trash_log.info('%s\t\t%s' % (self.__class__.__name__, self.values.get('log', '')))
        # trash if unknown or no matcher.
        self.trash = True
    
    def explain(self):
        ''' returns a String readable by humans explaining this Log '''
        return self.values.get('log', 'Unknown Combat Log')
    
    def clean(self):
        if 'log' in list(self.values.keys()):
            del self.values['log']

                
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
    matcher = re.compile(r"^Spawn\sSpaceShip\sfor\splayer(?P<player>-*\d+)\s\((?P<name>[^,]*),\s+(?P<hash>#\w+)\)\.\s+'(?P<ship_class>\w+)'")

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
    matcher = [
        # more complex version:       
        re.compile(r"^\s+Participant\s+(?P<source_name>[^\s]+)(?:\s+(?P<ship_class>\w+)|\s{30,})\s+(?:totalDamage\s(?P<total_damage>(?:\d+|\d+\.\d+));\s+|\s+)(?:mostDamageWith\s'(?P<module_class>[^']+)';\s*(?P<additional>.*)|<(?P<other>\w+)>)"),
        # simple version (new):
        re.compile(r"^\s+Participant\s+(?P<source_name>[^\s]+)\s+(?P<ship_class>\w+)"),
        re.compile(r"^\s+Participant\s+(?P<source_name>[^\s]+)"),
        ]

class Rocket(CombatLog):
    __slots__ = CombatLog.__slots__
    # keys = [ 'event', 'name', 'def', 'target', 'reason', 'direct_hit', 'rocket_id' ]
    # changed 'missile_type' to 'def'
    
    matcher = [
        # old version: Rocket detonation. owner...
        re.compile(r"^Rocket\s(?P<event>launch|detonation)\.\sowner\s'(?P<name>[^']+)'(?:,\s(?:def\s'(?P<def>[^']+)'|target\s'(?P<target>[^']+)'|reason\s'(?P<reason>[^']+)'|directHit\s'(?P<direct_hit>[^']+)'))+"),
        # new version: Rocket detonation rocket ID (is that range? it can be -1), owner ...
        re.compile(r"^Rocket\s(?P<event>launch|detonation)\s+(?P<rocket_id>-*\d+),\sowner\s'(?P<name>[^']+)'(?:,\s(?:def\s'(?P<def>[^']+)'|target\s'(?P<target>[^']+)'|reason\s'(?P<reason>[^']+)'|directHit\s'(?P<direct_hit>[^']+)'))+"),
        ]

class Heal(CombatLog):
    __slots__ = CombatLog.__slots__
    matcher = [
        # heal by module
        re.compile(r"^Heal\s+(?P<source_name>[^\s]+)\s\->\s+(?P<target_name>[^\s]+)\s+(?P<amount>(?:\d+|\d+\.\d+))\s(?P<module_class>[^\s]+)"),
        # direct heal by source or n/a (global buff)
        re.compile(r"^Heal\s+(?:n/a|(?P<source_name>\w+))\s+\->\s+(?P<target_name>[^\s]+)\s+(?P<amount>(?:\d+\.\d+|\d+))"),
        # new heal with microtid
        re.compile(r"^Heal\s+(?:n/a|(?P<source_name>[^\|]+)\|(?P<source_tid>\d+))\s+\->\s+(?P<target_name>[^\|]+)\|(?P<target_tid>\d+)\s+(?P<amount>(?:\d+\.\d+|\d+))")
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

class Uncaptured(CombatLog):
    """
        Variables:
        - objective (which was uncaptured (most likely something like VitalPointXY))
        - team (number)
        - attackers (split by space, names of the attackers, contains bots)
    """
    __slots__ = CombatLog.__slots__
    matcher = re.compile(r"^Uncaptured\s'(?P<objective>[^']+)'\(team\s(?P<team>\d+)\)\.(?:\sAttackers\:\s(?P<attackers>.*)|)")
    
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
        if log.startswith('======='):
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
        if 'log' in list(self.values.keys()):
            del self.values['log']

class PVE_Mission(CombatLog):
    """
     - mission: contains the mission id.
     - message: contains the pve mission message, like starting rounds, waves, etc.
    """
    __slots__ = CombatLog.__slots__
    matcher = re.compile("^PVE_Mission:\s'(?P<mission>[^']+)'.\s(?P<message>.*)") # this is very general, but we dont care for pve now.

class Looted(CombatLog):
    """
    called on looting in openspace.
    - loot contains the loot id.
    - container contains the container looted from.
    """
    __slots__ = CombatLog.__slots__
    matcher = re.compile("^Looted\s'(?P<loot>[^']+)'\sfrom\s'(?P<container>[^']+)'")

class Dropped(CombatLog):
    """
    called on dropping in openspace.
     - loot contains the loot id. it can be '<all>'
    """
    __slots__ = CombatLog.__slots__
    matcher = re.compile("^Dropped\sloot\s'(?P<loot>[^']+)'")

class Set(CombatLog):
    """
    called on setting "relationship" / OpenSpace
    Variables in values:
     - what (relationship)
     
    Optionals:
     - name (who do i set?)
     - value (to what value?)
     - def: spell usually in combination with level and deftype.
    """
    __slots__ = CombatLog.__slots__
    matcher = [
        # what: usually reputation.
        re.compile("^Set\s(?P<what>\w+)\s(?P<name>[^\s]+)\sto\s(?P<value>\w+)"),
        # what: 'stage', +level +deftype (aura), def (aura spell name), index is weird array lookup always 0, id is the id of the aura. 
        re.compile("^Set\s(?P<what>\w+)\s(?P<level>\d+)\s+for\s+(?P<deftype>\w+)\s+'(?P<def>[^']+)'\[(?P<index>\d+)\]\s+id\s(?P<id>-*\d+)"),
        ]

class SqIdChange(CombatLog):
    """ - number: player number
        - name: player name
        - old_sqid: sqid of player before
        - sqid: new player sqid
    """
    __slots__ = CombatLog.__slots__
    matcher = re.compile("^Player\s(?P<number>\d+)\((?P<name>[^\)]+)\)\schanged\ssqid\sfrom\s(?P<old_sqid>\d+)\sto\s(?P<sqid>\d+)")
    
    @classmethod
    def _log_handler(cls, log):
        if log.startswith('Player'):
            return True
        return False

class Mailed(CombatLog):
    """ has no information. only that loot has been mailed """
    __slots__ = CombatLog.__slots__
    matcher = re.compile("Mailed\sloot")

class UserEvent(CombatLog):
    """ special class for combat logs that might be associated with the playing player """
    __slots__ = CombatLog.__slots__
    @classmethod
    def _log_handler(cls, log):
        if log and 'earned medal' in log:
            return True
        elif log:
            logging.debug('UserEvent saw unknown line:\n%s' % log)
        return False

# Action?
COMBAT_LOGS = [ Apply, Damage, Spawn, Spell, Reward, Participant, Rocket, Heal, 
               Gameplay, #?
               Scores,
               Killed, Captured, AddStack, Cancel, Uncaptured,
               # undone openspace:
               PVE_Mission, Looted, Set, Dropped,
               SqIdChange, Mailed, # unknown if these are important...
               # always last:
               GameEvent, UserEvent,
               Stacktrace,
               ]

