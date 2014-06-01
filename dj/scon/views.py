
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import logic

def config(request):
    t = loader.get_template('scon/config.html')
    c = RequestContext(request, logic.config({'title': 'Configure your Client'}))
    return HttpResponse(t.render(c))
