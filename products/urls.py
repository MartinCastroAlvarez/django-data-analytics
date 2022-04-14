from rest_framework.routers import DefaultRouter

from products.views import ProductViewSet

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.register(r"products", ProductViewSet)
