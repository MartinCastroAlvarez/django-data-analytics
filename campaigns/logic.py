import logging
from datetime import datetime
from typing import Dict, List

from django.db.models.query import QuerySet
from subscriptions.models import Subscription

from campaigns.models import Campaign

logger: logging.RootLogger = logging.getLogger(__name__)


class CampaignLogic:
    """
    Business logic related to Campaigns.
    """

    def __init__(self, campaign: Campaign) -> None:
        """
        Campaign Logic constructor.
        """
        self.campaign: Campaign = campaign

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.campaign}>"

    def get_subscriptions(
        self, start: datetime, end: datetime
    ) -> QuerySet:
        """
        Counts subscriptions by Campaign.
        """
        subscriptions: QuerySet = Subscription.active.filter(
            created_at__gte=start,
            created_at__lte=end,
            event__metric__campaign=self.campaign,
        )
        logger.debug("Subscriptions: %s %s", self, subscriptions)
        return subscriptions
