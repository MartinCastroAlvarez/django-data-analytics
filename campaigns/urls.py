from rest_framework.routers import DefaultRouter

from campaigns.views import CampaignViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"campaigns", CampaignViewSet)
