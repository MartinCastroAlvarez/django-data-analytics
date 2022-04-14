import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from clients.models import Client
from clients.serializers import ClientSerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class ClientViewSet(ModelViewSet):
    """
    Client Model API View.
    """

    http_method_names: List[str] = ["get", "post", "put", "delete"]
    queryset: QuerySet = Client.objects.all()
    serializer_class: type = ClientSerializer

    def list(self, request: Request) -> Response:
        """
        GET /clients
        """
        clients: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            clients: QuerySet = Client.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: ClientSerializer = self.serializer_class(
            clients, many=True, context={"request": request}
        )
        logger.debug("List: %s", clients)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /clients
        """
        serializer: ClientSerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            client: Client = serializer.save()
            logger.debug("Created: %s", client)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /clients/:int
        """
        client: Client = self.get_object()
        serializer: ClientSerializer = self.serializer_class(
            client, context={"request": request}
        )
        logger.debug("Details: %s", client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /clients/:int
        """
        client: Client = self.get_object()
        serializer: ClientSerializer = self.serializer_class(
            client, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            client: Client = serializer.save()
            logger.debug("Updated: %s", client)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /clients/:int
        """
        client: Client = self.get_object()
        client.deleted_at = datetime.now()
        client.save()
        serializer: ClientSerializer = self.serializer_class(
            client, context={"request": request}
        )
        logger.debug("Deleted: %s", client)
        return Response(serializer.data, status=status.HTTP_200_OK)
