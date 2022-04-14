import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from states.models import State
from states.serializers import StateSerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class StateViewSet(ModelViewSet):
    """
    State Model API View.
    """

    http_method_names: List[str] = ["get", "post", "put", "delete"]
    queryset: QuerySet = State.objects.all()
    serializer_class: type = StateSerializer

    def list(self, request: Request) -> Response:
        """
        GET /states
        """
        states: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            states: QuerySet = State.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: StateSerializer = self.serializer_class(
            states, many=True, context={"request": request}
        )
        logger.debug("List: %s", states)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /states
        """
        serializer: StateSerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            state: State = serializer.save()
            logger.debug("Created: %s", state)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /states/:int
        """
        state: State = self.get_object()
        serializer: StateSerializer = self.serializer_class(
            state, context={"request": request}
        )
        logger.debug("Details: %s", state)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /states/:int
        """
        state: State = self.get_object()
        serializer: StateSerializer = self.serializer_class(
            state, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            state: State = serializer.save()
            logger.debug("Updated: %s", state)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /states/:int
        """
        state: State = self.get_object()
        state.deleted_at = datetime.now()
        state.save()
        serializer: StateSerializer = self.serializer_class(
            state, context={"request": request}
        )
        logger.debug("Deleted: %s", state)
        return Response(serializer.data, status=status.HTTP_200_OK)
