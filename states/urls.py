from rest_framework.routers import DefaultRouter

from states.views import StateViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"states", StateViewSet)
