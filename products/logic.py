import logging
from datetime import datetime
from typing import Dict, List

from django.db.models.query import QuerySet
from subscriptions.models import Subscription

from products.models import Product

logger: logging.RootLogger = logging.getLogger(__name__)


class ProductLogic:
    """
    Business logic related to Products.
    """

    def __init__(self, product: Product) -> None:
        """
        Product Logic constructor.
        """
        self.product: Product = product

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name}: {self.product}>"

    def get_subscriptions(
        self, start: datetime, end: datetime
    ) -> QuerySet:
        """
        Counts subscriptions by Product.
        """
        subscriptions: QuerySet = Subscription.active.filter(
            created_at__gte=start,
            created_at__lte=end,
            product=self.product,
        )
        logger.debug("Subscriptions: %s %s", self, subscriptions)
        return subscriptions
