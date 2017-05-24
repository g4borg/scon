import random

class ShipModule(object):
    """ A generic ship module equippable on a ship """
    name = 'Module' # class based variable. all ShipModule's share this one string.
    def __init__(self):
        self.ship = None # instance based variable. every instance has its own ship.
        
    def update(self):
        """ This function is called by the ship every gamestep """
        pass

class DefensiveLayer(ShipModule):
    """ some kind of defensive layer. a ship will use its defensive layers against incoming damage """
    name = 'Armor'
    
    def __init__(self, maximal, 
                 resistances=None, 
                 current=None):
        super(DefensiveLayer, self).__init__() # === ShipModule.__init__(self)
        self.maximal = maximal
        self.resistances = resistances or {}
        self.current = current or maximal
    
    def reduce_damage(self, damage, damage_type=None):
        # reduces incoming damage by absorbing it somehow.
        if self.current > 0:
            # only resist if i have still current.
            if damage_type:
                # if there was a damage type, we look up in our resistances:
                res = self.resistances.get(damage_type, 0)
                if res:
                    damage -= damage * res
            # we call get_damage to absorb damage, and it returns the rest of the damage.
            return self.get_damage(damage)
        else:
            # we have no life, damage passes through.
            return damage
    
    def get_damage(self, damage):
        # the module itself gets an amount of damage.
        self.current -= damage
        if self.current <= 0:
            rest_damage = 0 - self.current
            self.current = 0
            return rest_damage
        return 0

class Shields(DefensiveLayer):
    """ Shields can recharge after a delay. """
    name = 'Shields'
    RECHARGE_DELAY = 5
    
    def __init__(self, maximal, 
                 resistances=None, current=None, recharge=0):
        super(Shields, self).__init__(maximal, resistances, current)
        self.recharge = recharge
        # we save this little integer, which if bigger than zero, indicates there was a hit not long ago.
        self._last_hit = 0
    
    def get_damage(self, damage):
        # we override get_damage to remember we got hit.
        self._last_hit = self.RECHARGE_DELAY
        return super(Shields, self).get_damage(damage)
    
    def update(self):
        # we override update function to implement a recharge, and slowly reset the _last_hit.
        if self._last_hit > 0:
            self._last_hit -= 1
        else:
            if self.current < self.maximal:
                self.current += self.recharge
                self.current = min(self.current, self.maximal)

class Evasion(DefensiveLayer):
    """ Evasion is a special module, which has a chance to evade damage alltogether """
    default_cooldown = 32 * 60
    def __init__(self, evasion=None, default_cooldown=None):
        super(Evasion, self).__init__(1, {}, 1)
        self.evasion = evasion or 0.1
        self.cooldown = 0
        if default_cooldown:
            # if default cooldown is given, override class variable with instance variable:
            self.default_cooldown = default_cooldown
        
    def get_damage(self, damage):
        if damage == 0:
            # dont try to evade no damage.
            return 0
        if self.cooldown == 0 and random.random()<self.evasion:
            self.cooldown = self.default_cooldown
            print(f'{self.ship.name} superbly evades!')
            return 0
        else: return damage
    
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        

class Weapon(ShipModule):
    """ Weapons can fire 
        On this class we save some class variables, which act as default values.
            - we can subclass different weapons overriding those values for all weapons of that kind.
            - we can still make individual weapons with different stats.
    """
    name = 'Weapon'
    DEFAULT_DAMAGE = 10
    DEFAULT_COOLDOWN = 10
    DEFAULT_DAMAGE_TYPE = None
    
    def __init__(self,  ammo,
                        damage=None, 
                        cooldown=None, 
                        damage_type=None):
        super(Weapon, self).__init__()
        self.damage = damage or self.DEFAULT_DAMAGE
        self.cooldown = cooldown or self.DEFAULT_COOLDOWN
        self.damage_type = damage_type or self.DEFAULT_DAMAGE_TYPE
        self._heat = 0
        self.ammo = ammo
        
    
    def fire(self, other_ship, me=None):
        if not other_ship:
            return
        if self.ammo == 0:
            # no ammo
            return
        elif self.ammo < 0:
            # infinite ammo
            pass
        else:
            # reduce ammo
            self.ammo -= 1
        if self._heat == 0:
            other_ship.on_hit(self.damage, self.damage_type, me or self.ship)
            self._heat = self.cooldown
    
    def update(self):
        if self._heat > 0:
            self._heat -= 1

##########################################################################
class Spaceship(object):
    
    def __init__(self, name, modules=None):
        self.name = name
        self.modules = modules or []
        self.alive = True
        # we define an additional automatically called function
        self.equip_default()
    
    def equip_default(self):
        # you can use this to equip stuff by default in a subclass, without the need to override __init__.
        pass
    
    # we define some methods, that get called by the game itself:
    def on_spawn(self):
        print(f"{self.name} appears in space.")
        # bind my modules.
        for mod in self.modules:
            mod.ship = self
    
    def on_hit(self, damage, damage_type, source):
        for mod in self.modules:
            if isinstance(mod, DefensiveLayer):
                damage = mod.reduce_damage(damage, damage_type)
                if damage == 0:
                    return
        if damage > 0:
            # i am dead.
            self.alive = False
    
    def health_status(self):
        for mod in self.modules:
            if isinstance(mod, DefensiveLayer):
                if mod.current < mod.maximal:
                    print (f'{mod.name} has sustained {mod.maximal-mod.current} damage')
    
    def fire(self, target):
        for mod in self.modules:
            if isinstance(mod, Weapon):
                mod.fire(target, self)
    
    def update(self):
        for mod in self.modules:
            if isinstance(mod, ShipModule):
                mod.update()

class ShipBattle(object):
    # this is what one calls an abstract class or interface, basicly only defining methods.
    def add_ship(self, team, ship):
        pass
    def run(self):
        pass

class FreeForAll(ShipBattle):
    def __init__(self):
        # no need to call parent init since it has no init.
        self.ships = []
        self.running = False
    
    def add_ship(self, team, ship):
        self.ships.append(ship)
        
    def run(self):
        for ship in self.ships:
            ship.on_spawn()
        all_dead = False
        while not all_dead:
            all_dead = True
            for ship in self.ships:
                if ship.alive:
                    all_dead = False
                # even dead ships get the chance to fire a last time:
                targets = list(set(self.ships))
                targets.remove(ship)
                if len(targets) > 0:
                    target = random.choice(targets)
                    print(f'{ship.name} fires at {target.name}!')
                    ship.fire(target)
                else:
                    print (f'{ship.name} has won!')
                    return
                if ship.alive:
                    ship.update()
            # check should remove all dead ships.
            self.check()
    
    def check(self):
        if len(self.ships) == 0:
            print("There are no ships left.")
            self.running = False
            return
        remove_ships = []
        for ship in self.ships:
            if not ship.alive:
                print(f'The ship {ship.name} is destroyed.')
                remove_ships.append(ship)
        for ship in remove_ships:
            self.ships.remove(ship)

class TeamDeathMatch(ShipBattle):
    def __init__(self):
        self.teams = {}
        
    def add_ship(self, team, ship):
        ships = self.teams.get(team, [])
        ships.append(ship)
        self.teams[team] = ships
    
    def run(self):
        for team in self.teams.keys():
            print(f'Spawning team {team}')
            for ship in self.teams[team]:
                ship.on_spawn()
        all_dead = False
        while not all_dead:
            all_dead = True
            for team in self.teams.keys():
                other_teams = list(set(self.teams.keys()))
                other_teams.remove(team)
                if len(other_teams) == 0:
                    print(f'Team {team} is victorious!')
                    return
                for ship in self.teams[team]:
                    if ship.alive:
                        all_dead = False
                        ship.update()
                    atarget=random.choice(self.teams[random.choice(other_teams)])
                    print(f'{ship.name} fires at {atarget.name}!')
                    ship.fire(atarget)
            if not self.check():
                return
    
    
    def check(self):
        if len(self.teams.keys()) == 0:
            print("There are no ships left.")
            self.running = False
            return
        remove_ships = []
        for team in self.teams.keys():
            for ship in self.teams[team]:
                if not ship.alive:
                    print(f'The ship {ship.name} is destroyed.')
                    remove_ships.append((team, ship))
            
        for team, ship in remove_ships:
            self.teams[team].remove(ship)
        remove_teams = []
        for team in self.teams.keys():
            if len(self.teams[team]) == 0:
                print(f'Team {team} was eliminated.')
                remove_teams.append(team)
        for team in remove_teams:
            del self.teams[team]
        return True            
    
def main():
    game = TeamDeathMatch()
    
    
    game.add_ship('Holdens Crew', Spaceship('Rocinante', modules=[  Evasion(0.5, default_cooldown=30), # awesome evasive roci! 
                                                    DefensiveLayer(450, resistances={'kinetic': 0.2, 'phase': 0.45, None: 0.1}), 
                                                    Weapon(ammo=3200, damage=8, cooldown=1, damage_type='kinetic'), 
                                                    Weapon(ammo=1200, damage=12, cooldown=2, damage_type='kinetic'),
                                                    Weapon(ammo=3200, damage=8, cooldown=1, damage_type='kinetic'),
                                                    Weapon(ammo=1200, damage=12, cooldown=2, damage_type='kinetic'),
                                                    ]
                            ))
    
    game.add_ship('Protoss', Spaceship('Protoss Carrier', modules=[Shields(1000, resistances={None: 0.2, 'kinetic': 0.4, 'phase': 0.01}, recharge=4), 
                                                        DefensiveLayer(100, resistances={None: -0.1, 'kinetic': 0.0, 'phase': 0.2}), 
                                                        Weapon(-1, damage=15, cooldown=5, damage_type='phase'), 
                                                        Weapon(-1, damage=15, cooldown=5, damage_type='phase'),
                                                        Weapon(-1, damage=140, cooldown=60, damage_type='phase'),
                                                        ]))
    
    # add small ships in 2 teams.
    for x in range(1, 8):
        game.add_ship(1, Spaceship(f'Raptor {x}', modules=[Shields(100, recharge=0.2, resistances={'kinetic': 0.2}),
                                                        Evasion(0.05), # evade once shields are down! 
                                                        DefensiveLayer(50, resistances={'phase': 0.25}), 
                                                        Weapon(ammo=1200,damage=10, cooldown=5, damage_type='kinetic'), 
                                                        Weapon(ammo=120,damage=10, cooldown=5, damage_type='kinetic'),
                                                        Weapon(ammo=50, damage=40, cooldown=1000, damage_type='phase')]))
    for x in range(1, 8):
        game.add_ship(2, Spaceship(f'Barracuda {x}', modules=[Shields(100, recharge=0.2, resistances={'kinetic': 0.2}),
                                                        Evasion(0.05), # evade once shields are down! 
                                                        DefensiveLayer(50, resistances={'phase': 0.25}), 
                                                        Weapon(ammo=1200,damage=10, cooldown=5, damage_type='kinetic'), 
                                                        Weapon(ammo=120,damage=10, cooldown=5, damage_type='kinetic'),
                                                        Weapon(ammo=50, damage=40, cooldown=1000, damage_type='phase')]))
    game.run()

if __name__ == '__main__':
    main()
    