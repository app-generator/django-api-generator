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

# For cross platform imports 
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

class Command(BaseCommand):
    help = 'API Code generator'

    def add_arguments(self, parser):
        pass
        parser.add_argument(
            '-f',
            action='store_true',
            help='Generate API for all models without checking migrated in database or not.',
        )

    def handle(self, *args, **options):
        
        # @Todo - Validate settings
        
        # @Todo - Check models exists 

        # Check API folder
        # Note: Needs a reset at each generation
        
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

        generate_api()

        self.stdout.write(f"API successfully generated")
