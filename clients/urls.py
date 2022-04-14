from typing import List

from django.urls import URLPattern, path
from rest_framework.routers import DefaultRouter

from clients.views import ClientViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"clients", ClientViewSet)
