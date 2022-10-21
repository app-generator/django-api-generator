# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from core.settings import API_GENERATOR

# For cross platform imports 
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from . import serializers as serializers
from . import views       as views
from . import urls        as urls 

def generate_serializer_file():

    from . import serializers

    serializers_structure = pkg_resources.read_text(serializers, 'serializers_structure')

    '''
    with open('django_api_gen/serializers/serializers_structure', 'r') as serializers_structure_file:
        serializers_structure = serializers_structure_file.read()
    '''

    library_imports = pkg_resources.read_text(serializers, 'library_imports')

    '''
    with open('django_api_gen/serializers/library_imports', 'r') as library_imports_file:
        library_imports = library_imports_file.read()
    '''

    base_imports = pkg_resources.read_text(serializers, 'base_imports')

    '''
    with open('django_api_gen/serializers/base_imports', 'r') as base_imports_file:
        base_imports = base_imports_file.read()
    '''

    base_serializer = pkg_resources.read_text(serializers, 'base_serializer')

    '''
    with open('django_api_gen/serializers/base_serializer', 'r') as base_serializer_file:
        base_serializer = base_serializer_file.read()
    '''

    # This produces: from apps.models import app1.models.Book, app2.models.City
    # project_imports = base_imports.format(models_name=", ".join(API_GENERATOR.values()))

    models = []
    project_imports = ''

    for val in API_GENERATOR.values():
        
        # extract model from import path
        model_name    = val.split('.')[-1]
        model_import  = val.replace('.'+model_name, '') 
        models.append( model_name )

        # print( ' >> VAL -> ' + val )
        # print( ' >> model_name ->  ' + model_name )
        # print( ' >> model_import --> ' + model_import ) 

        # Build Imports
        project_imports += 'from ' + model_import + ' import ' + model_name + '\n\n' 
        
    serializers = '\n\n'.join(base_serializer.format(model_name=model_name) for model_name in models )
    
    generation = serializers_structure.format(
        library_imports=library_imports,
        project_imports=project_imports,
        serializers=serializers
    )

    with open('api/serializers.py', 'w') as serializers_py:
        serializers_py.write(generation)

    return generation


def generate_views_file():

    from . import views

    views_structure = pkg_resources.read_text(views, 'views_structure')

    '''
    with open('django_api_gen/views/views_structure', 'r') as views_structure_file:
        views_structure = views_structure_file.read()
    '''    

    library_imports = pkg_resources.read_text(views, 'library_imports')

    '''    
    with open('django_api_gen/views/library_imports', 'r') as library_imports_file:
        library_imports = library_imports_file.read()
    '''

    base_imports = pkg_resources.read_text(views, 'base_imports')

    '''
    with open('django_api_gen/views/base_imports', 'r') as base_imports_file:
        base_imports = base_imports_file.read()
    '''

    base_views = pkg_resources.read_text(views, 'base_views')

    '''
    with open('django_api_gen/views/base_view', 'r') as base_views_file:
        base_views = base_views_file.read()
    '''


    '''
    project_imports = base_imports.format(
        models_name=', '.join(API_GENERATOR.values()),
        serializers_name=', '.join(list(map(lambda model_name: f'{model_name}Serializer', API_GENERATOR.values())))
    )
    '''

    models = []
    project_imports = ''

    for val in API_GENERATOR.values():
        
        # extract model from import path
        model_name    = val.split('.')[-1]
        model_import  = val.replace('.'+model_name, '') 
        models.append( model_name )

        # print( ' >> VAL -> ' + val )
        # print( ' >> model_name ->  ' + model_name )
        # print( ' >> model_import --> ' + model_import ) 

        # Build Imports
        project_imports += 'from ' + model_import + ' import ' + model_name + '\n\n'     

    views = '\n\n'.join(base_views.format(
        serializer_name=f'{model_name}Serializer',
        model_name=model_name
    ) for model_name in models)

    generation = views_structure.format(
        library_imports=library_imports,
        project_imports=project_imports,
        views=views
    )

    with open('api/views.py', 'w') as views_py:
        views_py.write(generation)

    return generation


def generate_urls_file():

    from . import urls
    
    urls_file_structure = """{library_imports}\n{project_imports}\nurlpatterns = [\n{paths}\n\n]"""

    library_imports = pkg_resources.read_text(urls, 'library_imports')

    '''
    with open('django_api_gen/urls/library_imports', 'r') as library_imports_file:
        library_imports = library_imports_file.read()
    '''

    base_imports = pkg_resources.read_text(urls, 'base_imports')

    '''
    with open('django_api_gen/urls/base_imports', 'r') as base_imports_file:
        base_imports = base_imports_file.read()
    '''

    base_urls_path = pkg_resources.read_text(urls, 'base_urls_path')

    '''
    with open('django_api_gen/urls/base_url_path', 'r') as base_urls_file:
        base_urls_path = base_urls_file.read()
    '''

    models = []
    project_imports = ''

    for val in API_GENERATOR.values():
        
        # extract model from import path
        model_name    = val.split('.')[-1]
        model_import  = val.replace('.'+model_name, '') 
        models.append( model_name )

    views_name = ", ".join(list(map(lambda model_name: f'{model_name}View', models)))
    paths = ''

    '''
    for endpoint, model_name in API_GENERATOR.items():
        view_name = f'{model_name}View'
        paths = f'{paths}\n\t{base_urls_path.format(endpoint=endpoint, view_name=view_name)}'
    '''

    for endpoint, model_path in API_GENERATOR.items():

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
