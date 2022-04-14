import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from metrics.models import Metric
from metrics.serializers import MetricSerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class MetricViewSet(ModelViewSet):
    """
    Metric Model API View.
    """

    http_method_names: List[str] = ["get", "post", "put", "delete"]
    queryset: QuerySet = Metric.objects.all()
    serializer_class: type = MetricSerializer

    def list(self, request: Request) -> Response:
        """
        GET /metrics
        """
        metrics: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            metrics: QuerySet = Metric.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: MetricSerializer = self.serializer_class(
            metrics, many=True, context={"request": request}
        )
        logger.debug("List: %s", metrics)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /metrics
        """
        serializer: MetricSerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            metric: Metric = serializer.save()
            logger.debug("Created: %s", metric)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /metrics/:int
        """
        metric: Metric = self.get_object()
        serializer: MetricSerializer = self.serializer_class(
            metric, context={"request": request}
        )
        logger.debug("Details: %s", metric)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /metrics/:int
        """
        metric: Metric = self.get_object()
        serializer: MetricSerializer = self.serializer_class(
            metric, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            metric: Metric = serializer.save()
            logger.debug("Updated: %s", metric)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /metrics/:int
        """
        metric: Metric = self.get_object()
        metric.deleted_at = datetime.now()
        metric.save()
        serializer: MetricSerializer = self.serializer_class(
            metric, context={"request": request}
        )
        logger.debug("Deleted: %s", metric)
        return Response(serializer.data, status=status.HTTP_200_OK)
