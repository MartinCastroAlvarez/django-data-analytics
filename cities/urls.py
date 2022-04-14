from rest_framework.routers import DefaultRouter

from cities.views import CityViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"cities", CityViewSet)
