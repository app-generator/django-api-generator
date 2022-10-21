# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from http import HTTPStatus
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
