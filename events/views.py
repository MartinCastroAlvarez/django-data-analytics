import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from events.models import Event
from events.serializers import EventSerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class EventViewSet(ModelViewSet):
    """
    Event Model API View.
    """

    http_method_names: List[str] = ["get", "post", "put", "delete"]
    queryset: QuerySet = Event.objects.all()
    serializer_class: type = EventSerializer

    def list(self, request: Request) -> Response:
        """
        GET /events
        """
        events: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            events: QuerySet = Event.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: EventSerializer = self.serializer_class(
            events, many=True, context={"request": request}
        )
        logger.debug("List: %s", events)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /events
        """
        serializer: EventSerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            event: Event = serializer.save()
            logger.debug("Created: %s", event)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /events/:int
        """
        event: Event = self.get_object()
        serializer: EventSerializer = self.serializer_class(
            event, context={"request": request}
        )
        logger.debug("Details: %s", event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /events/:int
        """
        event: Event = self.get_object()
        serializer: EventSerializer = self.serializer_class(
            event, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            event: Event = serializer.save()
            logger.debug("Updated: %s", event)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /events/:int
        """
        event: Event = self.get_object()
        event.deleted_at = datetime.now()
        event.save()
        serializer: EventSerializer = self.serializer_class(
            event, context={"request": request}
        )
        logger.debug("Deleted: %s", event)
        return Response(serializer.data, status=status.HTTP_200_OK)
