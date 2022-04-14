import logging
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from metadata.models import Metadata
from metadata.serializers import MetadataSerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class MetadataViewSet(ModelViewSet):
    """
    Metadata Model API View.
    """

    http_method_names: List[str] = [
        "get",
    ]
    queryset: QuerySet = Metadata.objects.all()
    serializer_class: type = MetadataSerializer

    def list(self, request: Request) -> Response:
        """
        GET /metadata
        """
        metadata: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            metadata: QuerySet = Metadata.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: MetadataSerializer = self.serializer_class(
            metadata, many=True, context={"request": request}
        )
        logger.debug("List: %s", metadata)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /metadata
        """
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /metadata/:int
        """
        metadata: Metadata = self.get_object()
        serializer: MetadataSerializer = self.serializer_class(
            metadata, context={"request": request}
        )
        logger.debug("Details: %s", metadata)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /metadata/:int
        """
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /metadata/:int
        """
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
