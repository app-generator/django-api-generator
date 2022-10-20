# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import importlib
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from django_api_gen import generate_api

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
        
        generate_api()
        self.stdout.write(f"API successfully generated.")
