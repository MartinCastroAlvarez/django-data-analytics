import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from audiences.models import Audience
from audiences.serializers import AudienceSerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class AudienceViewSet(ModelViewSet):
    """
    Audience Model API View.
    """

    http_method_names: List[str] = ["get", "post", "put", "delete"]
    queryset: QuerySet = Audience.objects.all()
    serializer_class: type = AudienceSerializer

    def list(self, request: Request) -> Response:
        """
        GET /audiences
        """
        audiences: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            audiences: QuerySet = Audience.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: AudienceSerializer = self.serializer_class(
            audiences, many=True, context={"request": request}
        )
        logger.debug("List: %s", audiences)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /audiences
        """
        serializer: AudienceSerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            audience: Audience = serializer.save()
            logger.debug("Created: %s", audience)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /audiences/:int
        """
        audience: Audience = self.get_object()
        serializer: AudienceSerializer = self.serializer_class(
            audience, context={"request": request}
        )
        logger.debug("Details: %s", audience)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /audiences/:int
        """
        audience: Audience = self.get_object()
        serializer: AudienceSerializer = self.serializer_class(
            audience, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            audience: Audience = serializer.save()
            logger.debug("Updated: %s", audience)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /audiences/:int
        """
        audience: Audience = self.get_object()
        audience.deleted_at = datetime.now()
        audience.save()
        serializer: AudienceSerializer = self.serializer_class(
            audience, context={"request": request}
        )
        logger.debug("Deleted: %s", audience)
        return Response(serializer.data, status=status.HTTP_200_OK)
