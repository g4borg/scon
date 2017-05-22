#!/usr/bin/python
# -*- coding: utf-8 -*-

from logs.base import Log, L_WARNING, Stacktrace
import re
"""
    This deals with the Game.Log file
    This file records lots of junk, but is needed to establish actions taken  between combat sessions,
    or retrieve more detailed information about running instances.
    It is also the typical place for a Stacktrace to happen.


--------------------------------------
Interesting Lines:

23:16:27.427        | Steam initialized appId 212070, userSteamID 1|1|4c5a01, userName 'G4bOrg'
23:16:36.214        | ====== starting level: 'levels/mainmenu/mainmenu'  ======
23:16:38.822        | ====== level started:  'levels/mainmenu/mainmenu' success ======
23:16:44.251        | ====== starting level: 'levels\mainmenu\mm_empire'  ======
23:16:46.464        | ====== level started:  'levels\mainmenu\mm_empire' success ======

--- Date: 2014-07-18 (Fri Jul 2014) Mitteleuropäische Sommerzeit UTC+01:00

23:55:55.517        | MasterServerSession: connect to dedicated server, session 6777304, at addr 159.253.138.162|35005
23:55:55.543        | client: start connecting to 159.253.138.162|35005...
23:55:55.683        | client: connected to 159.253.138.162|35005, setting up session...
23:55:55.886        | client: ADD_PLAYER 0 (OregyenDuero [OWL], 00039C86) status 6 team 1 group 1178422
23:55:55.886        | client: ADD_PLAYER 1 (R0gue, 0012768A) status 6 team 2 group 1178451
23:55:55.886        | client: ADD_PLAYER 2 (g4borg [OWL], 0003A848) status 1 team 1 group 1178422
23:55:55.886        | client: ADD_PLAYER 3 (WladTepes, 001210D8) status 6 team 1
23:55:55.886        | client: ADD_PLAYER 4 (oberus [], 000FE9B2) status 6 team 2
23:55:55.886        | client: ADD_PLAYER 5 (TheGuns58, 00121C58) status 6 team 1
23:55:55.886        | client: ADD_PLAYER 6 (Belleraphon, 0004C744) status 2 team 2
23:55:55.886        | client: ADD_PLAYER 7 (TopoL, 00007E1F) status 6 team 1
23:55:55.886        | client: ADD_PLAYER 8 (unicoimbraPT, 000C4FAC) status 6 team 2
23:55:55.886        | client: ADD_PLAYER 9 (AeroBobik [], 00082047) status 6 team 1
23:55:55.886        | client: ADD_PLAYER 10 (Samson4321 [], 000B93AF) status 6 team 2
23:55:55.886        | client: ADD_PLAYER 11 (nol [], 00069165) status 6 team 1
23:55:55.886        | client: ADD_PLAYER 12 (Pudwoppa, 000334A4) status 2 team 2
23:55:55.886        | client: ADD_PLAYER 13 (IgorMad [], 000D2AF3) status 6 team 1
23:55:55.886        | client: ADD_PLAYER 14 (YokaI, 000F1CC9) status 6 team 2
23:55:55.886        | client: ADD_PLAYER 15 (MrAnyKey [], 0012246C) status 6 team 2 group 1178451
23:55:55.886        | client: ADD_PLAYER 30 ((bot)David, 00000000) status 4 team 1
23:55:55.886        | client: ADD_PLAYER 31 ((bot)George, 00000000) status 4 team 2
23:55:55.886        | client: server assigned id 2
23:55:55.886        | client: got level load message 's1340_thar_aliendebris13'
23:55:55.889        | reset d3d device
23:55:56.487        | ReplayManager: stopping activity due to map change
23:55:56.576        | ====== starting level: 'levels\area2\s1340_thar_aliendebris13' KingOfTheHill client ======


"""

class GameLog(Log):
    __slots__ = Log.__slots__
    @classmethod
    def is_handler(cls, log):
        if log.get('logtype', None) == '': # we handle only logs with empty logtype.
            return cls._is_handler(log)
        return False
    
    @classmethod
    def _is_handler(cls, log):
        return False
    
    def __init__(self, values=None):
        super(GameLog, self).__init__()
        self.values = values
        self.reviewed = False
    
    def clean(self):
        if 'log' in list(self.values.keys()):
            del self.values['log']
    
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
                    self.trash = False
                    return True
        # unknown?
        self.trash = True
    
    def explain(self):
        ''' returns a String readable by humans explaining this Log '''
        return self.values.get('log', 'Unknown Game Log')

class WarningLog(Log):
    # has no slots, always trash.
    trash = True
    
    @classmethod
    def is_handler(cls, log):
        if log.get('logtype', None) == L_WARNING:
            return True
        return False
    
    def __init__(self, values=None):
        self.trash = True

########################################################################################################
# Individual logs.

class SteamInitialization(GameLog):
    __slots__ = GameLog.__slots__
    matcher = [
        re.compile(r"^Steam\sinitialized\sappId\s(?P<steam_app_id>\d+),\suserSteamID\s(?P<steam_id_universe>\d+)\|(?P<steam_id_type>\d+)\|(?P<steam_id_account_hex>\w+),\suserName\s'(?P<steam_username>[^']+)'"),
        ]

class MasterServerSession(GameLog):
    __slots__ = GameLog.__slots__
    matcher = [
        re.compile(r"^MasterServerSession\:\sconnect\sto\sdedicated\sserver(?:,\s|session\s(?P<session_id>\d+)|at addr (?P<addr>\d+\.\d+\.\d+\.\d+)\|(?P<port>\d+))+"),
        re.compile(r"^MasterServerSession:\sconnect\sto\sZoneInstance,\ssession\s(?P<session_id>\d+),\sat\saddr\s(?P<addr>\d+\.\d+\.\d+\.\d+)\|(?P<port>\d+),\szoneId\s(?P<zone_id>\d+)"),
        ]
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').startswith('MasterServerSession'):
            return True
        return False
    
    
class ClientInfo(GameLog):
    __slots__ = GameLog.__slots__
    # Note: clinfo holds the subtype of this packet.
    matcher = [
        # connecting; addr, port
        re.compile(r"^client\:\sstart\s(?P<clinfo>connecting)\sto\s(?P<addr>\d+\.\d+\.\d+\.\d+)\|(?P<port>\d+)\.\.\."),
        # connected; addr, port
        re.compile(r"^client\:\s(?P<clinfo>connected)\sto\s(?P<addr>\d+\.\d+\.\d+\.\d+)\|(?P<port>\d+).*"),
        # ADD_PLAYER; pnr, player, clantag, player_id, status, team, group
        re.compile(r"^client\:\s(?P<clinfo>ADD_PLAYER)\s+(?P<pnr>\d+)\s+\((?P<player>[^\s\,]+)(?:\s\[(?P<clantag>\w+)\],|\s\[\],|,)\s(?P<player_id>\w+)\)(?:\s|status\s(?P<status>\d+)|team\s(?P<team>\d+)|group\s(?P<group>\d+))+"),
        # assigned; myid
        re.compile(r"^client\:\sserver\s(?P<clinfo>assigned)\sid\s(?P<myid>\d+)"),
        # level; level
        re.compile(r"^client\:\sgot\s(?P<clinfo>level)\sload\smessage\s'(?P<level>[^']+)'"),
        # leave; pnr
        re.compile(r"^client\:\splayer\s(?P<pnr>\d+)\s(?P<clinfo>leave)\sgame"),
        # avgPing; avg_ping, avg_packet_loss, avg_snapshot_loss
        re.compile(r"^client\:\s(?P<clinfo>avgPing)\s(?P<avg_ping>[^;]+)(?:\;|\s|avgPacketLoss\s(?P<avg_packet_loss>[^;]+)|avgSnapshotLoss\s(?P<avg_snapshot_loss>[^;$]+))+"),
        # closed; dr
        re.compile(r"^client\:\sconnection\s(?P<clinfo>closed)\.(?:\s|(?P<dr>.*))+"),
        # disconnect; addr, port, dr
        re.compile(r"^client\:\s(?P<clinfo>disconnect)\sfrom\sserver\s(?P<addr>\d+\.\d+\.\d+\.\d+)\|(?P<port>\d+)\.(?:\s|(?P<dr>\w+))+"),
        # ready;
        re.compile(r"^client\:\ssend\s(?P<clinfo>ready)\smessage"),
        # init; ping
        re.compile(r"^client\:\sgot\s(?P<clinfo>init)\smessage\s+\(and\s1st\ssnapshot\)\.\sping\s(?P<ping>\d+)"),
        ]
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').startswith('client:'):
            return True
        return False
    

class StartingLevel(GameLog):
    __slots__ = GameLog.__slots__
    # level, gametype, unknown_gametype
    matcher = [
    re.compile(r"^======\sstarting\slevel\:\s'(?P<level>[^']+)'\s(?P<gametype>[^\s]+)\sclient\s(?P<some_id>\d+)\s======"),
    re.compile(r"^======\sstarting\slevel\:\s'(?P<level>[^']+)'\s(?P<gametype>[^\s]+)\sclient\s======"),
    re.compile(r"^======\sstarting\slevel\:\s'(?P<level>[^']+)'\s(?P<gametype>[^\s]+)\s======"),
    re.compile(r"^======\sstarting\slevel\:\s'(?P<level>[^']+)'\s+======"),
    ]
    
    def is_mainmenu(self):
        if self.reviewed and self.values:
            if 'mainmenu' in self.values.get('level', ''):
                return True
            return False
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').startswith('====== starting'):
            return True
        return False
    
    
class LevelStarted(GameLog):
    __slots__ = GameLog.__slots__
    matcher = []
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').startswith('====== level'):
            return True
        return False
    



GAME_LOGS = [#SteamInitialization,
             MasterServerSession,
             ClientInfo,
             StartingLevel,
             #LevelStarted,
             Stacktrace,
             ]