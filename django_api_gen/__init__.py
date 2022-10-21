# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from . import manager

def generate_api():
    manager.generate_serializer_file()
    manager.generate_views_file()
    manager.generate_urls_file()