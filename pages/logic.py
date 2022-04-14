import logging
import os
from datetime import datetime
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from cache.logic import CacheLogic
from django.db.models.query import QuerySet
from events.models import Event
from metadata.logic import MetadataLogic
from metadata.models import Metadata
from requests import Response
from subscriptions.models import Subscription

from pages.models import Page

logger: logging.RootLogger = logging.getLogger(__name__)


class PageLogic:
    """
    Business logic related to Pages.
    """

    MAPPINGS: str = os.path.join(
        os.path.dirname(__file__), "mappings.json"
    )

    def __init__(self, page: Page) -> None:
        """
        Page Logic constructor.
        """
        self.page: Page = page

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.page}>"

    def get_html(self) -> bytes:
        """
        Downloads web page.
        """
        response: Response = requests.get(self.page.url)
        if response.status_code != 200:
            raise RuntimeError(response.status_code, response.reason)
        logger.debug(
            "HTML: %s %s %s",
            self.page.url,
            response.status_code,
            response.reason,
        )
        return response.content

    def get_soup(self) -> BeautifulSoup:
        """
        Parse HTML using BS4.
        """
        cache: CacheLogic = CacheLogic(self.page.url)
        if not cache.exists():
            data: bytes = self.get_html()
            cache.save(data)
        else:
            data: bytes = cache.load()
        encoding: str = EncodingDetector.find_declared_encoding(
            data, is_html=True
        )
        return BeautifulSoup(
            data.decode("utf-8"), "lxml", from_encoding=encoding
        )

    def update_metadata(self) -> None:
        """
        Extracts metadata from HTML page.
        """
        try:
            metadata: Metadata = self.page.metadata
        except Metadata.DoesNotExist:
            metadata: Metadata = Metadata()
            metadata.page = self.page
            metadata.save()
        logic: MetadataLogic = MetadataLogic(metadata)
        logic.find_tags(self.get_soup())
        logger.debug("Metadata: %s", logic.metadata)

    def get_events(self, start: datetime, end: datetime) -> QuerySet:
        """
        Counts events by Page.
        """
        events: QuerySet = Event.active.filter(
            created_at__gte=start,
            created_at__lte=end,
            metric__page=self.page,
        )
        logger.debug("Events: %s %s", self, events)
        return events
