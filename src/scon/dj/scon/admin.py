from django.contrib import admin
from . import models 
# Register your models here.
admin.site.register(models.Crafting)
admin.site.register(models.CraftingInput)
admin.site.register(models.Item)
