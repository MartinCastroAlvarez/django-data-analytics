import logging
from datetime import datetime
from typing import Dict, List

from django.db.models.query import QuerySet
from subscriptions.models import Subscription

from cities.models import City

logger: logging.RootLogger = logging.getLogger(__name__)


class CityLogic:
    """
    Business logic related to Cities.
    """

    def __init__(self, city: City) -> None:
        """
        City Logic constructor.
        """
        self.city: City = city

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.city}>"

    def get_subscriptions(
        self, start: datetime, end: datetime
    ) -> QuerySet:
        """
        Counts subscriptions by City.
        """
        subscriptions: QuerySet = Subscription.active.filter(
            created_at__gte=start,
            created_at__lte=end,
            event__metric__campaign__city=self.city,
        )
        logger.debug("Subscriptions: %s %s", self, subscriptions)
        return subscriptions
