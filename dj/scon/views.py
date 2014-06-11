
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import logic
import models

def config(request):
    t = loader.get_template('scon/config.html')
    c = RequestContext(request, logic.config({'title': 'Configure your Client'}))
    return HttpResponse(t.render(c))

def crafting(request):
    t = loader.get_template('scon/crafting/overview.html')
    items = models.Item.objects.filter(craftable=True)
    tree = None
    c = RequestContext(request, {'tree': tree,
                                 'items': items})
    return HttpResponse(t.render(c))