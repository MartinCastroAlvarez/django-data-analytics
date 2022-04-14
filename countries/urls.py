from rest_framework.routers import DefaultRouter

from countries.views import CountryViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"countries", CountryViewSet)
