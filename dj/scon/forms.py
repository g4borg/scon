'''
Created on 27.05.2014

@author: g4b
'''
from django import forms

class ConfigForm(forms.Form):
    def __init__(self, *args, **kwargs):
        