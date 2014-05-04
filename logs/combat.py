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

class Log(object):
    matcher = None
    
    @classmethod
    def is_handler(cls, log):
        return False
    
class CombatLog(Log):
    @classmethod
    def _log_handler(cls, log):
        if log.get('log', '').strip().startswith(cls.__name__):
            return True
        return False
    
    @classmethod
    def is_handler(cls, log):
        if log.get('logtype', None) == 'CMBT':
            return cls._log_handler(log)
        return False
    
    def __init__(self, values=None):
        self.values = values
    
    def unpack(self):
        # unpacks the data from the values.
        if hasattr(self, 'matcher') and self.matcher:
            matchers = self.matcher
            if not isinstance(matchers, list):
                matchers = [matchers,]
            for matcher in matchers:
                m = matcher.match(self.values.get('log', ''))
                if m:
                    self.values.update(m.groupdict())
                    return True
                
# @todo: where does this come from?
class Action(CombatLog):
    pass

class Gameplay(CombatLog):
    matcher = [
        # usual: team(reason). explained reason.
        re.compile(r"^Gameplay\sfinished\.\sWinner\steam\:\s+(?P<winner_team>\d+)\((?P<winner_reason>\w+)\)\.\sFinish\sreason\:\s'(?P<reason_verbose>[^']+)'\.\sActual\sgame\stime\s+(?P<game_time>\d+|\d+\.\d+)\ssec"),
        # team, unexplained reason (unknown, Timeout)
        re.compile(r"^Gameplay\sfinished\.\sWinner\steam\:\s+(?P<winner_team>\d+).\sFinish\sreason\:\s'(?P<winner_reason>[^']+)'\.\sActual\sgame\stime\s+(?P<game_time>\d+|\d+\.\d+)\ssec"),
        ]

class Apply(CombatLog): # Apply Aura.
    matcher = re.compile(r"^Apply\saura\s'(?P<aura_name>\w+)'\sid\s(?P<id>\d+)\stype\s(?P<aura_type>\w+)\sto\s'(?P<target_name>[^\']+)'")

class Damage(CombatLog):
    matcher = re.compile(r"^Damage\s+(?P<source_name>[^\s]+)\s\->\s+(?P<target_name>[^\s]+)\s+(?P<amount>(?:\d+|\d+\.\d+))(?:\s(?P<module_class>[^\s]+)\s|\s{2,2})(?P<flags>(?:\w|\|)+)")

class Spawn(CombatLog):
    matcher = re.compile(r"^Spawn\sSpaceShip\sfor\splayer(?P<player>\d+)\s\((?P<name>[^,]+),\s+(?P<hash>#\w+)\)\.\s+'(?P<ship_class>\w+)'")

class Spell(CombatLog):
    matcher = re.compile(r"^Spell\s'(?P<spell_name>\w+)'\sby\s+(?P<source_name>.*)(?:\((?P<module_name>\w+)\)|)\stargets\((?P<target_num>\d+)\)\:(?:$|\s(?P<targets>.+))")

class Reward(CombatLog):
    matcher = re.compile(r"^Reward\s+(?P<name>[^\s]+)(?:\s(?P<ship_class>\w+)\s+|\s+)(?P<amount>\d+)\s(?P<reward_type>.*)\s+for\s(?P<reward_reason>.*)")

class Participant(CombatLog):
    matcher = re.compile(r"^\s+Participant\s+(?P<source_name>[^\s]+)(?:\s{2}(?P<ship_class>\w+)|\s{30,})\s+(?:totalDamage\s(?P<total_damage>(?:\d+|\d+\.\d+));\smostDamageWith\s'(?P<module_class>[^']+)';(?P<additional>.*)|<(?P<other>\w+)>)")

class Rocket(CombatLog):
    matcher = re.compile(r"^Rocket\s(?P<event>launch|detonation)\.\sowner\s'(?P<name>[^']+)'(?:,\s(?:def\s'(?P<missile_type>\w+)'|target\s'(?P<target>[^']+)'|reason\s'(?P<reason>\w+)'|directHit\s'(?P<direct_hit>[^']+)'))+")

class Heal(CombatLog):
    matcher = [
        # heal by module
        re.compile(r"^Heal\s+(?P<source_name>[^\s]+)\s\->\s+(?P<target_name>[^\s]+)\s+(?P<amount>(?:\d+|\d+\.\d+))\s(?P<module_class>[^\s]+)"),
        # direct heal by source or n/a (global buff)
        re.compile(r"^Heal\s+(?:n/a|(?P<source_name>\w+))\s+\->\s+(?P<target_name>[^\s]+)\s+(?P<amount>(?:\d+|\d+\.\d+))"),
        ]

class Killed(CombatLog):
    matcher = [
        re.compile(r"^Killed\s(?P<target_name>[^\s]+)\s+(?P<ship_class>\w+);\s+killer\s(?P<source_name>[^\s]+)\s*"),
        re.compile(r"^Killed\s(?P<object>[^\(]+)\((?P<target_name>\w+)\);\s+killer\s(?P<source_name>[^\s]+)\s*"),
        re.compile(r"^Killed\s(?P<object>[^\;]+);\s+killer\s(?P<source_name>[^\s]+)\s+.*"),
        ]

class Captured(CombatLog):
    matcher = re.compile(r"^Captured\s'(?P<objective>[^']+)'\(team\s(?P<team>\d+)\)\.(?:\sAttackers\:(?P<attackers>.*)|.*)")

class AddStack(CombatLog):
    matcher = re.compile(r"^AddStack\saura\s'(?P<spell_name>\w+)'\sid\s(?P<id>\d+)\stype\s(?P<type>\w+)\.\snew\sstacks\scount\s(?P<stack_count>\d+)")

class Cancel(CombatLog):
    matcher = re.compile(r"^Cancel\saura\s'(?P<spell_name>\w+)'\sid\s(?P<id>\d+)\stype\s(?P<type>\w+)\sfrom\s'(?P<source_name>[^']+)'")

class Scores(CombatLog):
    matcher = re.compile(r"^Scores\s+-\sTeam1\((?P<team1_score>(?:\d+|\d+\.\d+))\)\sTeam2\((?P<team2_score>(?:\d+|\d+\.\d+))\)")
    
# Special classes
class GameEvent(CombatLog):
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
    
    def unpack(self):
        # unpacks the data from the values.
        if hasattr(self, 'matcher') and self.matcher:
            matchers = self.matcher
            if not isinstance(matchers, list):
                matchers = [matchers,]
            for matcher in matchers:
                m = matcher.match(self.values.get('log', '').strip('=').strip())
                if m:
                    self.values.update(m.groupdict())
                    return True

class UserEvent(CombatLog):
    """ special class for combat logs that might be associated with the playing player """
    @classmethod
    def _log_handler(cls, log):
        if log.get('log', '').strip():
            return True
        return False

# Action?
COMBAT_LOGS = [ Apply, Damage, Spawn, Spell, Reward, Participant, Rocket, Heal, 
               Gameplay, #?
               Scores,
               Killed, Captured, AddStack, Cancel,
               GameEvent, UserEvent
               ]

