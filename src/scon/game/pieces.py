
def res_to_red(res):
    ''' calculates reduction % of damage from base resistance
        incoming damage is assumed to be 100.0 to get percentages.
    '''
    if res >= 0:
        fd = 100 / (1.0+res/100.0)
    else:
        fd = 100 / (1.0-res/100.0)
    return 100.0 - fd

def dam_res(dam, res):
    ''' calculates damage modified by resistance.
    '''
    if res >= 0:
        fd = dam / (1.0+res/100.0)
    else:
        fd = dam / (1.0-res/100.0)
    return fd

class ShipInstance(object):
    # just testin something.
    def __init__(self,
                    shields=None,
                    hulls=None, 
                    shield_resis=None, 
                    hull_resis=None ):
        self.shield_max = shields or 5000
        self.hull_max = hulls or 5000
        shield_resis = shield_resis or (100,100,100)
        hull_resis = hull_resis or (100,100,100)
        self.set_shield_res(*shield_resis)
        self.set_hull_res(*hull_resis)
        
    
    def set_shield_res(self, kn, em, th):
        self.shield_res_kn = kn
        self.shield_res_em = em
        self.shield_res_th = th
    
    def set_hull_res(self, kn, em, th):
        self.hull_res_kn = kn
        self.hull_res_em = em
        self.hull_res_th = th
        
    def survivability(self):
        # i have no clue how they calc this.
        # multiple attempts shows, they are using base pts as measure, but how exactly the calc is?
        krs = (self.shield_max/100.0 * self.shield_res_kn)
        ers = (self.shield_max/100.0 * self.shield_res_em)
        trs = (self.shield_max/100.0 * self.shield_res_th)
        print(("Shield.", krs, ers, trs))
        
        krh = (self.hull_max/100.0 * self.hull_res_kn)
        erh = (self.hull_max/100.0 * self.hull_res_em)
        trh = (self.hull_max/100.0 * self.hull_res_th)
        print(("Hull.", krh, erh, trh))
        
        #print "?1", ((krs+ers+trs+krh+erh+trh)/6.0)+self.shield_max + self.hull_max
        print(("?2", ((krs+ers+trs+3*self.shield_max)/3.0)+((krh+erh+trh+3*self.hull_max)/3.0)))
        
        
        # another try:
        """
            lets assume survivability is really measured through applying 1000 dps for 10 secs.
            
        """
        print("Assuming dps...")
        shield = self.shield_max
        hull = self.hull_max
        r1s = shield / (1.0*dam_res(1000, self.shield_res_kn))
        r2s = shield / (1.0*dam_res(1000, self.shield_res_em))
        r3s = shield / (1.0*dam_res(1000, self.shield_res_th))
        print((r1s, r2s, r3s))
        rXs = (r1s+r2s+r3s) / 3.0
        print(("Shield survival time at 1kdps", rXs))

        r1h = hull / (1.0*dam_res(1000, self.hull_res_kn))
        r2h = hull / (1.0*dam_res(1000, self.hull_res_em))
        r3h = hull / (1.0*dam_res(1000, self.hull_res_th))
        print((r1h, r2h, r3h))
        rXh = (r1h+r2h+r3h) / 3.0
        print(("Hull survival time at 1kdps", rXh))
        
        print(("Total survival time ", rXs + rXh, " sec"))
        print(("Surv should be ", int(round((rXs+rXh) * 1000))))
        
        
        
        return ((krs+ers+trs)/3.0)+self.shield_max + self.hull_max + ((krh+erh+trh)/3.0)
    
    

ship = ShipInstance()
print((ship.survivability()))

print(("#" * 80))
mykatanas=ShipInstance(7664, 4296, (70,61,100), (20,80,50))
print("We know its 19736... but own calcs say...")
print((mykatanas.survivability()))