from rest_framework.routers import DefaultRouter

from events.views import EventViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"events", EventViewSet)
