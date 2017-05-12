"""
    Generate Fixtures for Crafting.
    Simple generator, does not integrate well into existing stuff, so please use
    only for bootstrapping.
"""
import os, json
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DIR = os.path.join(BASE_DIR, 'scon', 'fixtures')

def write_fixture(data):
    f = open(os.path.join(DIR, 'generated.json'), 'w')
    f.write(json.dumps(data))
    f.close()

def build_pk_cache(data, models=None):
    pk_cache = {}
    # fill cache from existing
    for d in data:
        if 'pk' in list(d.keys()):
            # has pk
            pk_cache[d['model']] = max(pk_cache.get('model', 0), d['pk'])
    for d in data:
        m = d['model']
        if models:
            if m not in models:
                continue
        if 'pk' in list(d.keys()):
            #print "PK was already in there! %s" % d
            pass
        else:
            if m not in list(pk_cache.keys()):
                pk_cache[m] = 1
                i = 1
            else:
                i = pk_cache[m] + 1
                pk_cache[m] = i
            d['pk'] = i        
    return data

def lookup_pk(data, name, mdl='scon.item', kwargs=None):
    for d in data:
        if d['model'] == mdl:
            if d['fields'].get('name', '').lower() == name.lower():
                found = True
                if kwargs is not None:
                    for key, val in list(kwargs.items()):
                        if not d['fields'].get(key, None) == val:
                            found = False
                if found:
                    return d['pk']

def generate_fixtures():
    data = []
    
    ORES = [
            {'name': 'Impure tungsten', 'sell_price': 6600, 'icon': 'resource_tungsten_ore'},
            {'name': 'Impure osmium', 'sell_price': 4500, 'icon': 'resource_osmium_ore'},
            {'name': 'Impure silicon', 'sell_price': 600, 'icon': 'resource_silicon_ore'},
            {'name': 'Vanadium', 'sell_price': 500, 'icon': 'resource_vanadium'},
            {'name': 'Crystal shard', 'sell_price': 3500, 'icon': 'resource_crystal_shard'},
            ]
    MATERIALS = [
            {'name': 'Tungsten plate', 
             'description': 'Durable tungsten plate', 
             'sell_price': 20000,
             'icon': 'component_tungsten_plate'},
            {'name': 'Screened battery', 'sell_price': 42000, 
             'icon': 'component_screened_battery'},
            {'name': 'Osmium crystals', 'sell_price': 5500, 
             'icon': 'component_osmium_crystals'},
            {'name': 'Pure Silicon', 'sell_price': 2500, 
             'icon': 'component_pure_silicon'},
            {'name': 'Processing block', 'sell_price': 22000, 
             'icon': 'component_processing_block'},
            {'name': 'Metal blank', 'sell_price': 1600, 
             'icon': 'component_metal_blank'},
            {'name': 'Alien Monocrystal', 'sell_price': 25000, 
             'icon': 'component_alien_monocrystal'},
            {'name': 'Computing chip', 'sell_price': 4500, 
             'icon': 'component_computing_chip'},
            ]
    AMMOS = [
            {'name': 'Explosive Shells',
             'quality': 4,
             'sell_price': 1000,
             'icon': 'ammo_explosive_shells_mk4',
             },
            {'name': 'Double Deflector',
             'quality': 4,
             'sell_price': 1000,
             'icon': 'ammo_double_deflector_mk4',
             },
            {'name': 'Xenon Lamp',
             'quality': 4,
             'sell_price': 1000,
             'icon': 'ammo_xenon_lamp_mk4',
             },
            {'name': 'Attack Drone',
             'quality': 10,
             'sell_price': 1092,
             'icon': 'ammo_attack_drone',
             },
             {'name': 'Focusing Lens',
              'quality': 4,
              'sell_price': 1000,
              'icon': 'ammo_focusing_lens',
              },
             {'name': 'Iridium Slugs',
              'quality': 4,
              'sell_price': 1000,
              'icon': 'ammo_iridium_slugs',
              },
             {'name': 'Supercooled Charges',
              'quality': 4,
              'sell_price': 1000,
              'icon': 'ammo_supercooled_charges',
              },
             {'name': 'Doomsday Missile',
              'quality': 1,
              'sell_price': 1000,
              #'tech': 5,
              'icon': 'ammo_doomsday_missile',
              }
             ]
    
    ITEMS_NON_CRAFTING = [
             {'name': 'Target Tracking Coprocessor III',
              'typ': 5, # cpu
              'tech': 3,
              'sell_price': 20188,
              'description': 'Increases Critical Damage',
              'icon': 'cpu_target_tracking_coprocessor',
              },
            {'name': 'Plasma Gun III',
              'typ': 7, # weap
              'quality': 4,
              'tech': 3,
              'icon': 'weapon_plasma_gun',
              },
            {'name': 'Plasma Gun IV',
              'typ': 7, # weap
              'quality': 4,
              'tech': 4,
              'icon': 'weapon_plasma_gun',
              },
            {'name': 'Plasma Gun V',
              'typ': 7, # weap
              'quality': 4,
              'tech': 5,
              'icon': 'weapon_plasma_gun',
              },
            # assault rails:
            {'name': 'Assault Railgun III',
              'typ': 7, # weap
              'quality': 4,
              'tech': 3,
              'icon': 'weapon_assault_railgun',
              },
            {'name': 'Assault Railgun IV',
              'typ': 7, # weap
              'quality': 4,
              'tech': 4,
              'icon': 'weapon_assault_railgun',
              },
            {'name': 'Assault Railgun V',
              'typ': 7, # weap
              'quality': 4,
              'tech': 5,
              'icon': 'weapon_assault_railgun',
              },
            # beam cannon:
            {'name': 'Beam Cannon III',
              'typ': 7, # weap
              'quality': 4,
              'tech': 3,
              'icon': 'weapon_beam_cannon',
              },
            {'name': 'Beam Cannon IV',
              'typ': 7, # weap
              'quality': 4,
              'tech': 4,
              'icon': 'weapon_beam_cannon',
              },
            {'name': 'Beam Cannon V',
              'typ': 7, # weap
              'quality': 4,
              'tech': 5,
              'icon': 'weapon_beam_cannon',
              },
            ]
    
    ITEMS = [
             {'name': 'Duplicator',
              'typ': 0,
              'sell_price': 8000,
              'buy_price_premium': 200,
              'description': 'Revives in Invasion with Cargo once.',
              'icon': 'duplicator',
              },
             {'name': 'A1MA IV',
              'quality': 1,
              'tech': 4,
              'typ': 8, # active.
              'role': 0, # multipurp.
              'sell_price': 26910,
              'icon': 'active_a1ma',
              },
             {'name': 'Pirate "Orion" Targeting Complex V',
              'quality': 14,
              'tech': 5,
              'typ': 8, # active.
              'role': 3, # covops
              'icon': 'active_t5_orion_targeting_complex_pirate', 
              },
             {'name': 'Pirate Engine Overcharge V',
              'quality': 14,
              'tech': 5,
              'typ': 8, # active.
              'role': 6, # gunship
              'icon': 'active_t5_engine_overcharge_pirate', 
              },
             {'name': 'Pirate Mass Shield Generator V',
              'quality': 14,
              'tech': 5,
              'typ': 8, # active.
              'role': 7, # engi 
              'icon': 'active_t5_mass_shield_generator_pirate',
              },
             {'name': 'Reverse Thruster III',
              'quality': 1,
              'tech': 3,
              'typ': 8, # active.
              'role': 9, # LRF 
              'icon': 'active_reverse_thruster',
              },
             {'name': 'Reverse Thruster IV',
              'quality': 1,
              'tech': 4,
              'typ': 8, # active.
              'role': 9, # LRF
              'icon': 'active_reverse_thruster', 
              },
             {'name': 'Reverse Thruster V',
              'quality': 1,
              'tech': 5,
              'typ': 8, # active.
              'role': 9, # LRF 
              'icon': 'active_reverse_thruster',
              },
             {'name': 'Plasma Gun III',
              'quality': 5,
              'tech': 3,
              'typ': 7, # weap 
              'icon': 'weapon_plasma_gun_mk5',
              },
             {'name': 'Plasma Gun IV',
              'quality': 5,
              'tech': 4,
              'typ': 7, # weap
              'icon': 'weapon_plasma_gun_mk5', 
              },
             {'name': 'Plasma Gun V',
              'quality': 5,
              'tech': 5,
              'typ': 7, # weap 
              'icon': 'weapon_plasma_gun_mk5',
              },
             {'name': 'Assault Railgun III',
              'quality': 5,
              'tech': 3,
              'typ': 7, # weap 
              'icon': 'weapon_assault_rail_mk5',
              },
             {'name': 'Assault Railgun IV',
              'quality': 5,
              'tech': 4,
              'typ': 7, # weap
              'icon': 'weapon_assault_rail_mk5', 
              },
             {'name': 'Assault Railgun V',
              'quality': 5,
              'tech': 5,
              'typ': 7, # weap 
              'icon': 'weapon_assault_rail_mk5',
              },
             {'name': 'Beam Cannon III',
              'quality': 5,
              'tech': 3,
              'typ': 7, # weap 
              'icon': 'weapon_beam_cannon_mk5',
              },
             {'name': 'Beam Cannon IV',
              'quality': 5,
              'tech': 4,
              'typ': 7, # weap
              'icon': 'weapon_beam_cannon_mk5', 
              },
             {'name': 'Beam Cannon V',
              'quality': 5,
              'tech': 5,
              'typ': 7, # weap 
              'icon': 'weapon_beam_cannon_mk5',
              },
             ]
    BLUEPRINTS = [
            {'name': 'Focusing Lens Blueprint'},
            {'name': 'Iridium Slugs Blueprint'},
            {'name': 'Supercooled Charges Blueprint'},
            {'name': 'A1MA T4 Blueprint'},
            {'name': 'Orion-2 Targeting Complex Blueprint',
             'description': 'Module works twice as long but much weaker.'},
            {'name': 'Engine Warp Overcharge Blueprint'},
            {'name': 'Mass Shield Energizer Blueprint'},
            {'name': 'Reverse Thruster T3 Blueprint'},
            {'name': 'Reverse Thruster T4 Blueprint'},
            {'name': 'Reverse Thruster T5 Blueprint'},
            {'name': 'Beam Cannon Prototype T3 Blueprint'},
            {'name': 'Beam Cannon Prototype T4 Blueprint'},
            {'name': 'Beam Cannon Prototype T5 Blueprint'},
            {'name': 'Assault Railgun Prototype T3 Blueprint'},
            {'name': 'Assault Railgun Prototype T4 Blueprint'},
            {'name': 'Assault Railgun Prototype T5 Blueprint'},
            {'name': 'Plasma Gun Prototype T3 Blueprint'},
            {'name': 'Plasma Gun Prototype T4 Blueprint'},
            {'name': 'Plasma Gun Prototype T5 Blueprint'},
            {'name': 'Doomsday Missile Blueprint'},
            ]
    CRAFTING = [
            {'item': 'Duplicator',
             'recipee': [(1, 'Processing Block'), (2,'Computing chip'), (2, 'Metal blank')]},
            {'item': 'Tungsten plate',
             'recipee': [(2, 'Impure tungsten'),]},
            {'item': 'Screened battery',
             'recipee': [(1, 'Tungsten plate'), (2, 'Computing chip')]},
            {'item': 'Osmium crystals',
             'recipee': [(1, 'Impure osmium'),]},
            {'item': 'Pure Silicon',
             'recipee': [(1, 'Impure silicon'),]},
            {'item': 'Computing chip',
             'recipee': [(1, 'Crystal shard'),]},
            {'item': 'Processing block',
             'recipee': [(4, 'Pure Silicon'), (2, 'Computing chip')]},
            {'item': 'Metal blank',
             'recipee': [(2, 'Vanadium'),]},
            {'item': 'Target Tracking Coprocessor III',
             'recipee': [(1, 'Screened battery'), (7, 'Metal blank'), (5, 'Pure silicon')]},
            {'item': 'Explosive Shells',
             'amount': 2,
             'recipee': [(1, 'Metal blank'),(2, 'Pure Silicon')]},
            {'item': 'Attack drone',
             'recipee': [(1, 'Alien Monocrystal'), (1,'Computing chip')]},
            {'item': 'Double Deflector',
             'amount': 2,
             'recipee': [(1, 'Osmium crystals'),]},
            {'item': 'Xenon Lamp',
             'amount': 2,
             'recipee': [(1, 'Computing chip'), (1, 'Pure Silicon')]},
            
            {'item': 'Focusing Lens',
             'amount': 2,
             'recipee': [(1, 'Focusing Lens Blueprint'), (1, 'Osmium crystals')]},
            {'item': 'Supercooled Charges',
             'amount': 2,
             'recipee': [(1, 'Supercooled Charges Blueprint'), (1, 'Computing chip')]},
            {'item': 'Iridium Slugs',
             'amount': 2,
             'recipee': [(1, 'Iridium Slugs Blueprint'), (1, 'Metal blank')]},
            {'item': 'A1MA IV',
             'recipee': [(1, 'A1MA T4 Blueprint'), (2, 'Processing block'),
                         (14, 'Metal blank'), (2, 'Screened battery'),
                         (20, 'Alien Monocrystal')]},
            {'item': 'Pirate "Orion" Targeting Complex V',
             'recipee': [(1, 'Orion-2 Targeting Complex Blueprint'), 
                         (3, 'Tungsten plate'),
                         (4, 'Computing chip'), 
                         (2, 'Processing block'),
                         (30, 'Alien Monocrystal')
                         ]},
            {'item': 'Pirate Engine Overcharge V',
             'recipee': [(1, 'Engine Warp Overcharge Blueprint'), 
                         (3, 'Tungsten plate'),
                         (2, 'Osmium crystals'), 
                         (2, 'Processing block'),
                         (30, 'Alien Monocrystal')
                         ]},
            {'item': 'Pirate Mass Shield Generator V',
             'recipee': [(1, 'Mass Shield Energizer Blueprint'), 
                         (10, 'Metal blank'),
                         (3, 'Computing chip'), 
                         (3, 'Processing block'),
                         (30, 'Alien Monocrystal')
                         ]},
            # lrf reverse blink:
            {'item': 'Reverse Thruster III',
             'recipee': [(1, 'Reverse Thruster T3 Blueprint'), 
                         (7, 'Metal blank'),
                         (1, 'Screened battery'),
                         (4, 'Computing chip'), 
                         (15, 'Alien Monocrystal')
                         ]},
            {'item': 'Reverse Thruster IV',
             'recipee': [(1, 'Reverse Thruster T4 Blueprint'), 
                         (12, 'Metal blank'),
                         (2, 'Screened battery'),
                         (5, 'Computing chip'), 
                         (20, 'Alien Monocrystal')
                         ]},
            {'item': 'Reverse Thruster V',
             'recipee': [(1, 'Reverse Thruster T5 Blueprint'), 
                         (7, 'Tungsten plate'),
                         (3, 'Screened battery'),
                         (6, 'Computing chip'), 
                         (30, 'Alien Monocrystal')
                         ]},
            
            # plasma
            {'item': ('Plasma Gun III', {'quality': 5}),
             'recipee': [(1, 'Plasma Gun Prototype T3 Blueprint'), 
                         (1, ('Plasma Gun III', {'quality': 4})),
                         (6, 'Metal blank'),
                         (3, 'Screened battery'),
                         (30, 'Alien Monocrystal')
                         ]},
            {'item': ('Plasma Gun IV', {'quality': 5}),
             'recipee': [(1, 'Plasma Gun Prototype T4 Blueprint'), 
                         (1, ('Plasma Gun IV', {'quality': 4})),
                         (1, 'Tungsten plate'),
                         (4, 'Screened battery'),
                         (50, 'Alien Monocrystal')
                         ]},
            {'item': ('Plasma Gun V', {'quality': 5}),
             'recipee': [(1, 'Plasma Gun Prototype T5 Blueprint'), 
                         (1, ('Plasma Gun V', {'quality': 4})),
                         (3, 'Tungsten plate'),
                         (5, 'Screened battery'),
                         (70, 'Alien Monocrystal')
                         ]},
            # assault
            {'item': ('Assault Railgun III', {'quality': 5}),
             'recipee': [(1, 'Assault Railgun Prototype T3 Blueprint'), 
                         (1, ('Assault Railgun III', {'quality': 4})),
                         (6, 'Metal blank'),
                         (3, 'Screened battery'),
                         (30, 'Alien Monocrystal')
                         ]},
            {'item': ('Assault Railgun IV', {'quality': 5}),
             'recipee': [(1, 'Assault Railgun Prototype T4 Blueprint'), 
                         (1, ('Assault Railgun IV', {'quality': 4})),
                         (1, 'Tungsten plate'),
                         (4, 'Screened battery'),
                         (50, 'Alien Monocrystal')
                         ]},
            {'item': ('Assault Railgun V', {'quality': 5}),
             'recipee': [(1, 'Assault Railgun Prototype T5 Blueprint'), 
                         (1, ('Assault Railgun V', {'quality': 4})),
                         (3, 'Tungsten plate'),
                         (5, 'Screened battery'),
                         (70, 'Alien Monocrystal')
                         ]},
            # beam
             {'item': ('Beam Cannon III', {'quality': 5}),
             'recipee': [(1, 'Beam Cannon Prototype T3 Blueprint'), 
                         (1, ('Beam Cannon III', {'quality': 4})),
                         (6, 'Metal blank'),
                         (3, 'Screened battery'),
                         (30, 'Alien Monocrystal')
                         ]},
            {'item': ('Beam Cannon IV', {'quality': 5}),
             'recipee': [(1, 'Beam Cannon Prototype T4 Blueprint'), 
                         (1, ('Beam Cannon IV', {'quality': 4})),
                         (1, 'Tungsten plate'),
                         (4, 'Screened battery'),
                         (50, 'Alien Monocrystal')
                         ]},
            {'item': ('Beam Cannon V', {'quality': 5}),
             'recipee': [(1, 'Beam Cannon Prototype T5 Blueprint'), 
                         (1, ('Beam Cannon V', {'quality': 4})),
                         (3, 'Tungsten plate'),
                         (5, 'Screened battery'),
                         (70, 'Alien Monocrystal')
                         ]},
            # missiles
            {'item': 'Doomsday Missile',
             'recipee': [(1, 'Doomsday Missile Blueprint'), 
                         (2, 'Osmium crystals'),
                         (1, 'Computing chip'), 
                         (1, 'Metal blank'),
                         ]},
            ]
    
    for ore in ORES:
        fields = {'typ': 12,
                  'tech': 0,
                  'craftable': True,
                     }
        fields.update(ore)
        data.append({'model': 'scon.item', 'fields': fields})
    for mat in MATERIALS:
        fields = {'typ': 13,
                  'tech': 0,
                  'craftable': True,
                     }
        fields.update(mat)
        data.append({'model': 'scon.item', 'fields': fields})
    
    for ammo in AMMOS:
        fields = {'typ': 8,
                  'tech': 0,
                  'craftable': True,
                     }
        fields.update(ammo)
        data.append({'model': 'scon.item', 'fields': fields})
    
    for item in ITEMS:
        fields = {
                  # items define typ and tech!
                  'craftable': True,
                     }
        fields.update(item)
        data.append({'model': 'scon.item', 'fields': fields})
    
    for item in ITEMS_NON_CRAFTING:
        fields = {
                  # items define typ and tech!
                  'craftable': False,
                     }
        fields.update(item)
        data.append({'model': 'scon.item', 'fields': fields})
        
    for bluep in BLUEPRINTS:
        fields = {
                  'typ': 11, # blueprint
                  'tech': 0,
                  'craftable': True,
                  'icon': 'blueprint',
                     }
        fields.update(bluep)
        data.append({'model': 'scon.item', 'fields': fields})
        
    
    build_pk_cache(data)
    # now to the crafting recipees:
    i = 1 # counter for crafting
    j = 1 # counter for input
    for craft in CRAFTING:
        try:
            item = craft['item']
            kwargs = None
            if isinstance(item, tuple) or isinstance(item, list):
                kwargs = item[1]
                item = item[0]
            crafting = {'model': 'scon.crafting',
                        'pk': i,
                        'fields': { 'output': lookup_pk(data, item, kwargs=kwargs ),
                                    'amount': craft.get('amount', 1) }}
            data.append(crafting)
            primary = True
            for amount, recipee in craft['recipee']:
                item = recipee
                kwargs = None
                if isinstance(item, tuple) or isinstance(item, list):
                    print(item)
                    kwargs = item[1]
                    item = item[0]
                    
                crafting_input = {'model': 'scon.craftinginput',
                                  'pk': j,
                                  'fields': {'crafting': i,
                                             'item': lookup_pk(data, item, kwargs=kwargs),
                                             'amount': amount,
                                             'primary': primary}
                                  }
                primary = False
                j = j + 1
                data.append(crafting_input)
            i = i + 1
        except:
            raise
    
    build_pk_cache(data)
    return data
    
if __name__ == "__main__":
    fixes = generate_fixtures()
    from pprint import pprint
    pprint( fixes )
    # check pks:
    for d in fixes:
        if d.get('pk', None) is None:
            print(("%s is fail." % d))
    
    write_fixture(fixes)