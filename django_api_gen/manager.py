# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf import settings
from .util import *

API_GENERATOR = {}

try:
    API_GENERATOR = getattr(settings, 'API_GENERATOR') 
except:     
    pass 

# For cross platform imports 
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

def generate_serializer_file():

    # serializers should be visible in the local namespace
    from . import serializers

    serializers_structure = pkg_resources.read_text(serializers, 'serializers_structure')
    library_imports       = pkg_resources.read_text(serializers, 'library_imports')
    base_imports          = pkg_resources.read_text(serializers, 'base_imports')
    base_serializer       = pkg_resources.read_text(serializers, 'base_serializer')

    models = []
    project_imports = ''

    #for val in API_GENERATOR.values():
    for val in valid_models():
        
        # extract model from import path
        model_name    = val.split('.')[-1]
        model_import  = val.replace('.'+model_name, '') 
        models.append( model_name )

        # Build Imports
        project_imports += '    from ' + model_import + ' import ' + model_name + '\n' 
        
    serializers = '\n'.join(base_serializer.format(model_name=model_name) for model_name in models )
    
    generation = serializers_structure.format(
        library_imports=library_imports,
        project_imports=project_imports,
        serializers=serializers
    )

    with open('api/serializers.py', 'w') as serializers_py:
        serializers_py.write(generation)

    return generation

def generate_views_file():

    # views should be visible in the local namespace
    from . import views

    views_structure = pkg_resources.read_text(views, 'views_structure')  
    library_imports = pkg_resources.read_text(views, 'library_imports')
    base_imports    = pkg_resources.read_text(views, 'base_imports')
    base_views      = pkg_resources.read_text(views, 'base_views')

    models = []
    project_imports = ''

    #for val in API_GENERATOR.values():
    for val in valid_models():
        
        # extract model from import path
        model_name    = val.split('.')[-1]
        model_import  = val.replace('.'+model_name, '') 
        models.append( model_name )

        # Build Imports
        project_imports += '    from ' + model_import + ' import ' + model_name + '\n'     

    views = '\n'.join(base_views.format(
        serializer_name=f'{model_name}Serializer',
        model_name=model_name
    ) for model_name in models)

    generation = views_structure.format(
        library_imports=library_imports,
        project_imports=project_imports,
        base_imports=base_imports,
        views=views
    )

    with open('api/views.py', 'w') as views_py:
        views_py.write(generation)

    return generation

def generate_urls_file():

    # urls should be visible in the local namespace
    from . import urls
    
    urls_file_structure = """{library_imports}\n{project_imports}\nurlpatterns = [\n{paths}\n\n]"""

    library_imports = pkg_resources.read_text(urls, 'library_imports') 
    base_imports    = pkg_resources.read_text(urls, 'base_imports')
    base_urls_path  = pkg_resources.read_text(urls, 'base_urls_path')

    models = []
    project_imports = ''

    #for val in API_GENERATOR.values():
    for val in valid_models():
        
        # extract model from import path
        model_name    = val.split('.')[-1]
        model_import  = val.replace('.'+model_name, '') 
        models.append( model_name )

    views_name = ", ".join(list(map(lambda model_name: f'{model_name}View', models)))
    paths = ''

    for endpoint, model_path in API_GENERATOR.items():
        
        if model_path in valid_models():

            model_name    = model_path.split('.')[-1]
            model_import  = model_path.replace('.'+model_name, '') 

            view_name = f'{model_name}View'
            paths = f'{paths}\n\t{base_urls_path.format(endpoint=endpoint, view_name=view_name)}'

    generation = urls_file_structure.format(
        library_imports=library_imports,
        project_imports=base_imports.format(views_name=views_name),
        paths=paths
    )
    with open('api/urls.py', 'w') as urls_py:
        urls_py.write(generation)

    return generation
