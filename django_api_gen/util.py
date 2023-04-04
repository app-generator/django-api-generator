# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, importlib, shutil
from django.conf import settings

def valid_models():

    retVal = []

    API_GENERATOR = getattr(settings, 'API_GENERATOR')

    for val in API_GENERATOR.values():

        app_name      = val.split('.')[0]
        model_name    = val.split('.')[-1]
        model_import  = val.replace('.'+model_name, '')             

        models = importlib.import_module( model_import )

        try:
            model = getattr(models, model_name)
        except:
            #print(f' > Warn: [' + model_name + '] model NOT_FOUND for [' + app_name + '] APP' )
            #print(f'   Hint: Add [' + model_name + '] model definition in [' + app_name + ']')
            continue 

        try:
            model.objects.last()
        except:
            #print(f' > Warn: [' + model_name + '] model not migrated in DB.' )
            #print(f'   Hint: run makemigrations, migrate commands')
            continue

        #print ( ' Valid API_GEN Model -> ' + val )
        retVal.append( val )

    return retVal
