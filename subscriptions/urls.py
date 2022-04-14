from rest_framework.routers import DefaultRouter

from subscriptions.views import SubscriptionViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"subscriptions", SubscriptionViewSet)
