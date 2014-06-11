from django.db import models
from django.utils.text import slugify

ITEM_TYPES = (
  (0, 'Misc'),
  (1, 'Engine'),
  (2, 'Capacitor'),
  (3, 'Shield'),
  (4, 'Hull'),
  (5, 'Cpu'),
  (6, 'Active'),
  (7, 'Weapon'),
  (8, 'Ammo'),
  (9, 'Missile'),
  (10, 'Class'),
  (11, 'Blueprint'),
  (12, 'Resource'),
  (13, 'Component'),            
  )

QUALITY_TYPES = (
  (0, '-'),
  (1, 'Mk1'),
  (2, 'Mk2'),
  (3, 'Mk3'),
  (4, 'Mk4'),
  (5, 'Mk5'),
  (10, 'Universal'),
  (14, 'Pirate Mk4'),
  )
D_QUALITY = dict(QUALITY_TYPES)

TECH_TYPES = (
  (0, ''),
  (1, 'I'),
  (2, 'II'),
  (3, 'III'),
  (4, 'IV'),
  (5, 'V'),
  )

ROLE_TYPES = (
  (-1, ''),
  (0, 'Multipurpose'),
  (1, 'Recon'),
  (2, 'ECM'),
  (3, 'Covert Ops'),
  (4, 'Tackler'),
  (5, 'Command'),
  (6, 'Gunship'),
  (7, 'Engineer'),
  (8, 'Guard'),
  (9, 'Longrange')    
  )
# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    tech = models.IntegerField(default=0, blank=True)
    quality = models.IntegerField(default=0, blank=True, choices=QUALITY_TYPES)
    icon = models.CharField(max_length=128, blank=True, null=True)
    typ = models.IntegerField(default=0, choices=ITEM_TYPES)
    craftable = models.BooleanField(default=False, blank=True)
    sell_price = models.IntegerField(default=0, blank=True)
    buy_price = models.IntegerField(default=0, blank=True)
    buy_price_premium = models.IntegerField(default=0, blank=True)
    
    role = models.IntegerField(default=-1, blank=True)
    
    def save(self, *args, **kwargs):
        if self.icon is None or self.icon == '':
            if self.typ>0:
                item_types = dict(ITEM_TYPES)
                try:
                    s = item_types[self.typ]
                    s = s.lower()
                except:
                    s = 'unknown'
                self.icon = '%s_t%s_%s' % (s, self.tech, slugify(self.name))
            else:
                self.icon = 't%s_%s' % (self.tech, slugify(self.name))
        return super(Item, self).save(*args, **kwargs)
    
    def primary_recipee(self):
        f=CraftingInput.objects.filter(primary=True, item=self)
        if len(f) == 1:
            return f[0].crafting
    
    def crafting_used_in(self):
        return CraftingInput.objects.filter(item=self)
    
    def __unicode__(self):
        if self.quality:
            return '%s (%s)' % (self.name, D_QUALITY.get(self.quality, ''))
        return '%s' % (self.name,)

    
class Crafting(models.Model):
    output = models.ForeignKey(Item, related_name='crafting')
    amount = models.IntegerField(default=1, blank=True)
    input = models.ManyToManyField(Item, related_name='recipees', through='CraftingInput')
    
    def ingredients(self):
        return CraftingInput.objects.filter(crafting=self)
    
    def __unicode__(self):
        return 'Recipee for %s' % (self.output.name,)

class CraftingInput(models.Model):
    crafting = models.ForeignKey(Crafting)
    item = models.ForeignKey(Item)
    amount = models.IntegerField(default=1)
    primary = models.BooleanField(default=False, blank=True)
    
    def __unicode__(self):
        return 'Part of Recipee for %s (x%s): %s (x%s)' % (self.crafting.output, self.crafting.amount, self.item, self.amount)

