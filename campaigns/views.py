import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class CampaignViewSet(ModelViewSet):
    """
    Campaign Model API View.
    """

    http_method_names: List[str] = ["get", "post", "put", "delete"]
    queryset: QuerySet = Campaign.objects.all()
    serializer_class: type = CampaignSerializer

    def list(self, request: Request) -> Response:
        """
        GET /campaigns
        """
        campaigns: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            campaigns: QuerySet = Campaign.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: CampaignSerializer = self.serializer_class(
            campaigns, many=True, context={"request": request}
        )
        logger.debug("List: %s", campaigns)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /campaigns
        """
        serializer: CampaignSerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            campaign: Campaign = serializer.save()
            logger.debug("Created: %s", campaign)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /campaigns/:int
        """
        campaign: Campaign = self.get_object()
        serializer: CampaignSerializer = self.serializer_class(
            campaign, context={"request": request}
        )
        logger.debug("Details: %s", campaign)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /campaigns/:int
        """
        campaign: Campaign = self.get_object()
        serializer: CampaignSerializer = self.serializer_class(
            campaign, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            campaign: Campaign = serializer.save()
            logger.debug("Updated: %s", campaign)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /campaigns/:int
        """
        campaign: Campaign = self.get_object()
        campaign.deleted_at = datetime.now()
        campaign.save()
        serializer: CampaignSerializer = self.serializer_class(
            campaign, context={"request": request}
        )
        logger.debug("Deleted: %s", campaign)
        return Response(serializer.data, status=status.HTTP_200_OK)
