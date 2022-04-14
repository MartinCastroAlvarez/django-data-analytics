import logging
from datetime import datetime
from typing import Dict, List

from django.db.models.query import QuerySet
from subscriptions.models import Subscription

from countries.models import Country

logger: logging.RootLogger = logging.getLogger(__name__)


class CountryLogic:
    """
    Business logic related to Countries.
    """

    def __init__(self, country: Country) -> None:
        """
        Country Logic constructor.
        """
        self.country: Country = country

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.country}>"

    def get_subscriptions(
        self, start: datetime, end: datetime
    ) -> QuerySet:
        """
        Counts subscriptions by Country.
        """
        subscriptions: QuerySet = Subscription.active.filter(
            created_at__gte=start,
            created_at__lte=end,
            event__metric__campaign__city__state__country=self.country,
        )
        logger.debug("Subscriptions: %s %s", self, subscriptions)
        return subscriptions
