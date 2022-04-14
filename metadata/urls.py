from rest_framework.routers import DefaultRouter

from metadata.views import MetadataViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"metadata", MetadataViewSet)
