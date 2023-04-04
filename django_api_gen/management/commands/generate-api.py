# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, importlib, shutil

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from django.conf import settings

from django_api_gen import generate_api
from django_api_gen import api

# Cross platform imports 
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

class Command(BaseCommand):
    help = 'API Code generator'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', action='store_true', help='Forcing Generate API for all models (no checks).',
        )

    def handle(self, *args, **options):

        #################################################    
        # Validate settings

        # BASE_DIR -> ROOT or the project
        if not hasattr(settings, 'BASE_DIR'):
            print(f" > Err: 'BASE_DIR' not found in settings")
            print(f'   Hint: this variable point to the ROOT of the project]')
            return 

        # BASE_DIR -> ROOT or the project
        if not hasattr(settings, 'API_GENERATOR'):
            print(f" > Err: 'API_GENERATOR' not found in settings")
            return 

        #################################################    

        API_GENERATOR = getattr(settings, 'API_GENERATOR')

        valid_models = 0
        for val in API_GENERATOR.values():

            app_name      = val.split('.')[0]
            model_name    = val.split('.')[-1]
            model_import  = val.replace('.'+model_name, '')             

            models       = importlib.import_module( model_import )
            model        = None 

            try:
                model = getattr(models, model_name)
                model_exists = True
            except:
                print(f' > Warn: Model [' + model_name + '] not defined in [' + val.replace(('.' + model_name),'') + ']' )
                continue

            try:
                model.objects.last()
            except:
                print(f' > Warn: [' + val + '] model not migrated in DB.' )
                continue
    
            valid_models += 1

        if 0 == valid_models:
            print(f" > Error: All Models defined in CFG are INVALID")
            print(f"      |-- (nothing is generated)")
            return             

        #################################################    
        # User Confirmation

        print(f" > Configuration looks good.")
        print(f"   !!! The API folder will be overwritten !!! ")

        if options['f']:

            print(f" > Generate API (forcing mode).")

        else:
            answer = input("Continue? [Y/n]")

            if answer.upper() not in ["Y", "YES"]:
                print(f"API generation cancelled.")
                return 

        #################################################    
        # API folder - deleted at each cycle
        
        API_DIR        = os.path.join( settings.BASE_DIR, 'api' )
        API_FILE_INIT  = os.path.join( API_DIR, '__init__.py' )
        API_FILE_VIEWS = os.path.join( API_DIR, 'views.py' )
        API_FILE_URLS  = os.path.join( API_DIR, 'urls.py'  )
        API_FILE_SERIZ = os.path.join( API_DIR, 'serializers.py' )

        try:
            shutil.rmtree( API_DIR )
        except:
            pass

        # create API dir (all cases)
        os.mkdir( API_DIR )         

        API_FILE_INIT_content  = pkg_resources.read_text(api, '__init__.py'    )
        API_FILE_VIEWS_content = pkg_resources.read_text(api, 'views.py'       )
        API_FILE_URLS_content  = pkg_resources.read_text(api, 'urls.py'        )
        API_FILE_SERIZ_content = pkg_resources.read_text(api, 'serializers.py' )

        with open( API_FILE_INIT, 'w') as API_FILE_INIT_py:
            API_FILE_INIT_py.write( API_FILE_INIT_content )

        with open( API_FILE_VIEWS, 'w') as API_FILE_VIEWS_py:
            API_FILE_VIEWS_py.write( API_FILE_VIEWS_content )

        with open( API_FILE_URLS, 'w') as API_FILE_URLS_py:
            API_FILE_URLS_py.write( API_FILE_URLS_content )            

        with open( API_FILE_SERIZ, 'w') as API_FILE_SERIZ_py:
            API_FILE_SERIZ_py.write( API_FILE_SERIZ_content )    

        # Proceed with the SQL part
        generate_api()
        print(f"API successfully generated")

        # exit
        return 
