import logging
from datetime import datetime
from typing import Dict, List

from django.db.models.query import QuerySet
from subscriptions.models import Subscription

from states.models import State

logger: logging.RootLogger = logging.getLogger(__name__)


class StateLogic:
    """
    Business logic related to States.
    """

    def __init__(self, state: State) -> None:
        """
        State Logic constructor.
        """
        self.state: State = state

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.state}>"

    def get_subscriptions(
        self, start: datetime, end: datetime
    ) -> QuerySet:
        """
        Counts subscriptions by State.
        """
        subscriptions: QuerySet = Subscription.active.filter(
            created_at__gte=start,
            created_at__lte=end,
            event__metric__campaign__city__state=self.state,
        )
        logger.debug("Subscriptions: %s %s", self, subscriptions)
        return subscriptions
