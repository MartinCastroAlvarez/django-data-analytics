from rest_framework.routers import DefaultRouter

from metrics.views import MetricViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"metrics", MetricViewSet)
