

"""
    Each Line has to be separated first into timecode and kind of log.
    
    
    
"""

import re
Lines = [
    "23:53:29.239        | Steam initialized appId 212070, userSteamID 1|1|4c5a01, userName 'G4bOrg'",
    "23:53:29.841 WARNING| ^1UiResourceManager::LoadStrings(): empty string \"gameplay_map_pve_gate\" for default language",
    "01:05:08.735 CMBT   | Spawn SpaceShip for player0 (OregyenDuero, #00039C86). 'Ship_Race3_L_T3'",
    "03:43:29.796 CMBT   | AddStack aura 'Spell_Cold_Ray' id 3492 type AURA_SLOW_MOVEMENT. new stacks count 5",
         ]

RE_TIME = r'\d{2,2}\:\d{2,2}\:\d{2,2}\.\d{3,3}\s\w+'
RE_SCLOG = r'^(?P<hh>\d{2,2})\:(?P<mm>\d{2,2})\:(?P<ss>\d{2,2})\.(?P<ns>\d{3,3})\s(?P<logtype>\s*[^\|\s]+\s*|\s+)\|\s(?P<log>.*)'
R_SCLOG = re.compile(RE_SCLOG) 

for line in Lines:
    m = R_SCLOG.match(line)
    if m:
        print((m.groups()))
