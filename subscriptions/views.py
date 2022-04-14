import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class SubscriptionViewSet(ModelViewSet):
    """
    Subscription Model API View.
    """

    http_method_names: List[str] = ["get", "post", "put", "delete"]
    queryset: QuerySet = Subscription.objects.all()
    serializer_class: type = SubscriptionSerializer

    def list(self, request: Request) -> Response:
        """
        GET /subscriptions
        """
        subscriptions: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            subscriptions: QuerySet = Subscription.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: SubscriptionSerializer = self.serializer_class(
            subscriptions, many=True, context={"request": request}
        )
        logger.debug("List: %s", subscriptions)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /subscriptions
        """
        serializer: SubscriptionSerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            subscription: Subscription = serializer.save()
            logger.debug("Created: %s", subscription)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /subscriptions/:int
        """
        subscription: Subscription = self.get_object()
        serializer: SubscriptionSerializer = self.serializer_class(
            subscription, context={"request": request}
        )
        logger.debug("Details: %s", subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /subscriptions/:int
        """
        subscription: Subscription = self.get_object()
        serializer: SubscriptionSerializer = self.serializer_class(
            subscription,
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            subscription: Subscription = serializer.save()
            logger.debug("Updated: %s", subscription)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /subscriptions/:int
        """
        subscription: Subscription = self.get_object()
        subscription.deleted_at = datetime.now()
        if not subscription.canceled_at:
            subscription.canceled_at = datetime.now()
        subscription.save()
        serializer: SubscriptionSerializer = self.serializer_class(
            subscription, context={"request": request}
        )
        logger.debug("Deleted: %s", subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)
