import json
import logging
import os
from datetime import datetime
from typing import Dict, List

import dateutil.parser as parser
from bs4 import BeautifulSoup
from django.conf import settings

from metadata.models import Metadata

logger: logging.RootLogger = logging.getLogger(__name__)


class MetadataLogic:
    """
    Business logic related to Metadata.
    """

    MAPPINGS: str = os.path.join(
        settings.BASE_DIR, "metadata", "mappings.json"
    )

    def __init__(self, metadata: Metadata) -> None:
        """
        Metadata Logic constructor.
        """
        self.metadata: Metadata = metadata

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.metadata}>"

    def get_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extracts Metadata tags an HTML page.
        """
        return {
            tag.get("property", tag.get("name")): tag.get("content")
            for tag in soup.find_all("meta")
            if tag.get("name") or tag.get("property")
        }

    def find_tags(self, soup: BeautifulSoup) -> None:
        """
        Applies mappings to the Page Metadata.
        """
        with open(self.MAPPINGS) as file_handler:
            mappings: Dict[str, List[str]] = json.load(file_handler)
        tags: Dict[str, str] = self.get_tags(soup)
        for attribute, keywords in mappings.items():
            for keyword in keywords:
                if keyword in tags:
                    logger.debug(
                        "Metadata hit: %s %s %s",
                        attribute,
                        keyword,
                        tags[keyword],
                    )
                    if (
                        Metadata._meta.get_field(
                            attribute
                        ).get_internal_type()
                        == "DateTimeField"
                    ):
                        setattr(
                            self.metadata,
                            attribute,
                            parser.parse(tags[keyword]),
                        )
                    else:
                        setattr(
                            self.metadata, attribute, tags[keyword]
                        )
                    break
        self.metadata.save()
