from rest_framework.routers import DefaultRouter

from pages.views import PageViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"pages", PageViewSet)
