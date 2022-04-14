from rest_framework.routers import DefaultRouter

from audiences.views import AudienceViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"audiences", AudienceViewSet)
