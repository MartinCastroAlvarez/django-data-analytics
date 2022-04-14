import logging
from datetime import datetime
from typing import Dict, List

from django.db.models.query import QuerySet
from subscriptions.models import Subscription

from audiences.models import Audience

logger: logging.RootLogger = logging.getLogger(__name__)


class AudienceLogic:
    """
    Business logic related to Audiences.
    """

    def __init__(self, audience: Audience) -> None:
        """
        Audience Logic constructor.
        """
        self.audience: Audience = audience

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.audience}>"

    def get_subscriptions(
        self, start: datetime, end: datetime
    ) -> QuerySet:
        """
        Counts subscriptions by Audience.
        """
        subscriptions: QuerySet = Subscription.active.filter(
            created_at__gte=start,
            created_at__lte=end,
            event__metric__campaign__audience=self.audience,
        )
        logger.debug("Subscriptions: %s %s", self, subscriptions)
        return subscriptions
