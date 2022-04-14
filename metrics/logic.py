import logging
from datetime import datetime
from typing import Dict, List

from django.db.models.query import QuerySet

from metrics.models import Metric

logger: logging.RootLogger = logging.getLogger(__name__)


class MetricLogic:
    """
    Business logic related to Metric.
    """

    def __init__(self, metric: Metric) -> None:
        """
        Metric Logic constructor.
        """
        self.metric: Metric = metric

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.metric}>"
