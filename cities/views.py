import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cities.models import City
from cities.serializers import CitySerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class CityViewSet(ModelViewSet):
    """
    City Model API View.
    """

    http_method_names: List[str] = ["get", "post", "put", "delete"]
    queryset: QuerySet = City.objects.all()
    serializer_class: type = CitySerializer

    def list(self, request: Request) -> Response:
        """
        GET /cities
        """
        cities: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            cities: QuerySet = City.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: CitySerializer = self.serializer_class(
            cities, many=True, context={"request": request}
        )
        logger.debug("List: %s", cities)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /cities
        """
        serializer: CitySerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            city: City = serializer.save()
            logger.debug("Created: %s", city)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /cities/:int
        """
        city: City = self.get_object()
        serializer: CitySerializer = self.serializer_class(
            city, context={"request": request}
        )
        logger.debug("Details: %s", city)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /cities/:int
        """
        city: City = self.get_object()
        serializer: CitySerializer = self.serializer_class(
            city, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            city: City = serializer.save()
            logger.debug("Updated: %s", city)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /cities/:int
        """
        city: City = self.get_object()
        city.deleted_at = datetime.now()
        city.save()
        serializer: CitySerializer = self.serializer_class(
            city, context={"request": request}
        )
        logger.debug("Deleted: %s", city)
        return Response(serializer.data, status=status.HTTP_200_OK)
