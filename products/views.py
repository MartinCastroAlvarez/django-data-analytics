import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.serializers import ProductSerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class ProductViewSet(ModelViewSet):
    """
    Product Model API View.
    """

    http_method_names: List[str] = ["get", "post", "put", "delete"]
    queryset: QuerySet = Product.objects.all()
    serializer_class: type = ProductSerializer

    def list(self, request: Request) -> Response:
        """
        GET /products
        """
        products: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            products: QuerySet = Product.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: ProductSerializer = self.serializer_class(
            products, many=True, context={"request": request}
        )
        logger.debug("List: %s", products)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /products
        """
        serializer: ProductSerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            product: Product = serializer.save()
            logger.debug("Created: %s", product)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /products/:int
        """
        product: Product = self.get_object()
        serializer: ProductSerializer = self.serializer_class(
            product, context={"request": request}
        )
        logger.debug("Details: %s", product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /products/:int
        """
        product: Product = self.get_object()
        serializer: ProductSerializer = self.serializer_class(
            product, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            product: Product = serializer.save()
            logger.debug("Updated: %s", product)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /products/:int
        """
        product: Product = self.get_object()
        product.deleted_at = datetime.now()
        product.save()
        serializer: ProductSerializer = self.serializer_class(
            product, context={"request": request}
        )
        logger.debug("Deleted: %s", product)
        return Response(serializer.data, status=status.HTTP_200_OK)
