import logging
import os

from slugify import slugify

logger: logging.RootLogger = logging.getLogger(__name__)


class CacheLogic:
    """
    Business logic related to caching.
    """

    def __init__(self, key: str) -> None:
        """
        Initializing cache.
        """
        self.key: str = key
        self.hash: str = slugify(self.key)

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<Cache: {self.key}>"

    def exists(self) -> bool:
        """
        Returns True if key is cached.
        """
        if os.path.isfile(self.get_path()):
            logger.debug("Cache Hit: %s", self)
            return True
        logger.debug("Cache Miss: %s", self)
        return False

    def get_path(self) -> str:
        """
        Generates a cache key.
        """
        path: str = os.path.join(os.sep, "tmp", self.hash)
        logger.debug("Cache Path: %s", path)
        return path

    def save(self, data: bytes) -> None:
        """
        Writes data to the cache.
        """
        logger.debug("Cache Save: %s", data[:30])
        with open(self.get_path(), "wb") as file_handler:
            file_handler.write(data)

    def load(self) -> bytes:
        """
        Reads data from the cache.
        """
        with open(self.get_path(), "rb") as file_handler:
            data: bytes = file_handler.read()
        logger.debug("Cache Load: %s", data[:30])
        return data
