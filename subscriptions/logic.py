import logging
from datetime import datetime
from typing import Dict, List

from django.db.models.query import QuerySet

from subscriptions.models import Subscription

logger: logging.RootLogger = logging.getLogger(__name__)


class SubscriptionLogic:
    """
    Business logic related to Subscription.
    """

    def __init__(self, subscription: Subscription) -> None:
        """
        Subscription Logic constructor.
        """
        self.subscription: Subscription = subscription

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.subscription}>"

    @classmethod
    def get_subscriptions(
        cls, start: datetime, end: datetime
    ) -> QuerySet:
        """
        Returns subscriptions by date range.
        """
        subscriptions: QuerySet = Subscription.active.filter(
            created_at__gte=start,
            created_at__lte=end,
        )
        logger.debug("Subscriptions: %s %s", cls, subscriptions)
        return subscriptions
