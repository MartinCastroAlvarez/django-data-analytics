import logging
from datetime import datetime
from typing import Dict, List

from django.db.models.query import QuerySet
from subscriptions.models import Subscription

from clients.models import Client

logger: logging.RootLogger = logging.getLogger(__name__)


class ClientLogic:
    """
    Business logic related to Clients.
    """

    def __init__(self, client: Client) -> None:
        """
        Client Logic constructor.
        """
        self.client: Client = client

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.client}>"

    def get_subscriptions(
        self, start: datetime, end: datetime
    ) -> QuerySet:
        """
        Counts subscriptions by Client.
        """
        subscriptions: QuerySet = Subscription.active.filter(
            created_at__gte=start,
            created_at__lte=end,
            client=self.client,
        )
        logger.debug("Subscriptions: %s %s", self, subscriptions)
        return subscriptions
