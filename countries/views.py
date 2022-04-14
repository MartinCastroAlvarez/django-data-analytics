import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from countries.models import Country
from countries.serializers import CountrySerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class CountryViewSet(ModelViewSet):
    """
    Country Model API View.
    """

    http_method_names: List[str] = ["get", "post", "put", "delete"]
    queryset: QuerySet = Country.objects.all()
    serializer_class: type = CountrySerializer

    def list(self, request: Request) -> Response:
        """
        GET /countries
        """
        countries: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            countries: QuerySet = Country.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: CountrySerializer = self.serializer_class(
            countries, many=True, context={"request": request}
        )
        logger.debug("List: %s", countries)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /countries
        """
        serializer: CountrySerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            country: Country = serializer.save()
            logger.debug("Created: %s", country)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /countries/:int
        """
        country: Country = self.get_object()
        serializer: CountrySerializer = self.serializer_class(
            country, context={"request": request}
        )
        logger.debug("Details: %s", country)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /countries/:int
        """
        country: Country = self.get_object()
        serializer: CountrySerializer = self.serializer_class(
            country, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            country: Country = serializer.save()
            logger.debug("Updated: %s", client)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /countries/:int
        """
        country: Country = self.get_object()
        country.deleted_at = datetime.now()
        country.save()
        serializer: CountrySerializer = self.serializer_class(
            country, context={"request": request}
        )
        logger.debug("Deleted: %s", country)
        return Response(serializer.data, status=status.HTTP_200_OK)
