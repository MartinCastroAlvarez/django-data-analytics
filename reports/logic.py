import logging
from datetime import datetime, timedelta
from typing import Dict

from audiences.logic import AudienceLogic
from audiences.models import Audience
from campaigns.logic import CampaignLogic
from campaigns.models import Campaign
from cities.logic import CityLogic
from cities.models import City
from countries.logic import CountryLogic
from countries.models import Country
from django.db.models.query import QuerySet
from events.logic import EventLogic
from events.models import Event
from metadata.logic import MetadataLogic
from metadata.models import Metadata
from metrics.logic import MetricLogic
from metrics.models import Metric
from pages.logic import PageLogic
from pages.models import Page
from products.logic import ProductLogic
from products.models import Product
from states.logic import StateLogic
from states.models import State
from subscriptions.logic import SubscriptionLogic
from subscriptions.models import Subscription

logger: logging.RootLogger = logging.getLogger(__name__)


class ReportLogic:
    """
    Business logic related to Reports.
    """

    DATE_FORMAT: str = "%b %d %Y"
    MONTH_FORMAT: str = "%b %Y"

    def __init__(
        self, start: datetime, end: datetime, search: str
    ) -> None:
        """
        Report Logic constructor.
        """
        self.search: str = search.lower()
        self.start: datetime = start
        self.end: datetime = end

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.search} ({self.start} - {self.end})>"

    def get_subscriptions_by_campaign(self) -> Dict[Campaign, int]:
        """
        Searches subscriptions by Campaign.
        """
        frequencies: Dict[Campaign, int] = {
            campaign: CampaignLogic(campaign)
            .get_subscriptions(start=self.start, end=self.end)
            .count()
            for campaign in Campaign.active.search(self.search)
        }
        logger.debug("Subscriptions by Campaign: %s", frequencies)
        frequencies: Dict[Campaign, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_subscriptions_by_audience(self) -> Dict[Audience, int]:
        """
        Searches subscriptions by Audience.
        """
        frequencies: Dict[Audience, int] = {
            audience: AudienceLogic(audience)
            .get_subscriptions(start=self.start, end=self.end)
            .count()
            for audience in Audience.active.search(self.search)
        }
        logger.debug("Subscriptions by Audience: %s", frequencies)
        frequencies: Dict[Audience, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_subscriptions_by_product(self) -> Dict[Product, int]:
        """
        Searches subscriptions by Product.
        """
        frequencies: Dict[Product, int] = {
            product: ProductLogic(product)
            .get_subscriptions(start=self.start, end=self.end)
            .count()
            for product in Product.active.search(self.search)
        }
        logger.debug("Subscriptions by Product: %s", frequencies)
        frequencies: Dict[Product, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_subscriptions_by_city(self) -> Dict[City, int]:
        """
        Searches subscriptions by City.
        """
        frequencies: Dict[City, int] = {
            city: CityLogic(city)
            .get_subscriptions(start=self.start, end=self.end)
            .count()
            for city in City.active.search(self.search)
        }
        logger.debug("Subscriptions by City: %s", frequencies)
        frequencies: Dict[City, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_subscriptions_by_state(self) -> Dict[State, int]:
        """
        Searches subscriptions by State.
        """
        frequencies: Dict[State, int] = {
            state: StateLogic(state)
            .get_subscriptions(start=self.start, end=self.end)
            .count()
            for state in State.active.search(self.search)
        }
        logger.debug("Subscriptions by State: %s", frequencies)
        frequencies: Dict[State, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_subscriptions_by_country(self) -> Dict[Country, int]:
        """
        Searches subscriptions by Country.
        """
        frequencies: Dict[Country, int] = {
            country: CountryLogic(country)
            .get_subscriptions(start=self.start, end=self.end)
            .count()
            for country in Country.active.search(self.search)
        }
        logger.debug("Subscriptions by Country: %s", frequencies)
        frequencies: Dict[Country, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_events_by_page(self) -> Dict[Page, int]:
        """
        Searches events by Page.
        """
        frequencies: Dict[Page, int] = {
            page: PageLogic(page)
            .get_events(start=self.start, end=self.end)
            .count()
            for page in Page.active.search(self.search)
        }
        logger.debug("Events by Page: %s", frequencies)
        frequencies: Dict[Page, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_subscriptions_by_dow_and_hod(
        self,
    ) -> Dict[str, Dict[str, int]]:
        """
        Searches subscriptions by day of the week and hour of the day.
        """
        frequencies: Dict[str, Dict[str, int]] = {
            "Mon": {hour: 0 for hour in range(0, 24)},
            "Tue": {hour: 0 for hour in range(0, 24)},
            "Wed": {hour: 0 for hour in range(0, 24)},
            "Thu": {hour: 0 for hour in range(0, 24)},
            "Fri": {hour: 0 for hour in range(0, 24)},
            "Sat": {hour: 0 for hour in range(0, 24)},
            "Sun": {hour: 0 for hour in range(0, 24)},
        }
        for subscription in SubscriptionLogic.get_subscriptions(
            start=self.start, end=self.end
        ):
            frequencies[subscription.dow][subscription.hod] += 1
        logger.debug("Subscriptions by DoW and HoD: %s", frequencies)
        return frequencies

    def get_subscriptions_by_dom(self) -> Dict[int, int]:
        """
        Searches subscriptions by day of the month.
        """
        frequencies: Dict[int, int] = {i: 0 for i in range(0, 32)}
        for subscription in SubscriptionLogic.get_subscriptions(
            start=self.start, end=self.end
        ):
            frequencies[subscription.day] += 1
        logger.debug("Subscriptions by DoM: %s", frequencies)
        return frequencies

    def get_subscriptions_by_moy(self) -> Dict[str, int]:
        """
        Searches subscriptions by month of the year.
        """
        frequencies: Dict[str, int] = {
            "Jan": 0,
            "Feb": 0,
            "Mar": 0,
            "Apr": 0,
            "May": 0,
            "Jun": 0,
            "Jul": 0,
            "Aug": 0,
            "Sep": 0,
            "Oct": 0,
            "Nov": 0,
            "Dec": 0,
        }
        for subscription in SubscriptionLogic.get_subscriptions(
            start=self.start, end=self.end
        ):
            frequencies[subscription.month] += 1
        logger.debug("Subscriptions by MoY: %s", frequencies)
        return frequencies

    def get_subscriptions_by_date(self) -> Dict[str, int]:
        """
        Searches all subscriptions.
        """
        histogram: Dict[str, int] = {}
        current: datetime = self.start
        while current <= self.end:
            histogram[current.strftime(self.DATE_FORMAT)] = 0
            current += timedelta(days=1)
        subscriptions: QuerySet = SubscriptionLogic.get_subscriptions(
            start=self.start, end=self.end
        )
        for subscription in subscriptions:
            date: str = subscription.created_at.strftime(
                self.DATE_FORMAT
            )
            histogram[date] += 1
        logger.debug("Subscriptions by Date: %s", histogram)
        return histogram

    def get_margin_by_month(self) -> Dict[str, float]:
        """
        Searches all Subscription margins.
        """
        histogram: Dict[str, int] = {}
        current: datetime = self.start
        while current <= self.end:
            histogram[current.strftime(self.MONTH_FORMAT)] = 0
            current += timedelta(days=1)
        subscriptions: QuerySet = SubscriptionLogic.get_subscriptions(
            start=self.start, end=self.end
        )
        for subscription in subscriptions:
            date: str = subscription.created_at.strftime(
                self.MONTH_FORMAT
            )
            histogram[date] += subscription.margin
        logger.debug("Margin by Month: %s", histogram)
        return histogram

    def get_ltv_by_campaign(self) -> Dict[Campaign, float]:
        """
        Searches all LTVs by Campaign.
        """
        frequencies: Dict[Campaign, int] = {}
        for campaign in Campaign.active.search(self.search):
            logic: CampaignLogic = CampaignLogic(campaign)
            subscriptions: QuerySet = logic.get_subscriptions(
                start=self.start, end=self.end
            )
            total_ltv: int = sum(
                subscription.ltv for subscription in subscriptions
            )
            total_subscriptions: int = subscriptions.count() or 0.0001
            frequencies[campaign] = total_ltv / total_subscriptions
        logger.debug("Average LTV by Campaign: %s", frequencies)
        frequencies: Dict[Campaign, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_margin_by_campaign(self) -> Dict[Campaign, float]:
        """
        Searches subscription average durations by Campaign.
        """
        frequencies: Dict[Campaign, int] = {}
        for campaign in Campaign.active.search(self.search):
            logic: CampaignLogic = CampaignLogic(campaign)
            subscriptions: QuerySet = logic.get_subscriptions(
                start=self.start, end=self.end
            )
            total_ltv: float = sum(
                subscription.ltv for subscription in subscriptions
            )
            frequencies[campaign] = total_ltv - campaign.spend
        logger.debug("Margin by Campaign: %s", frequencies)
        frequencies: Dict[Campaign, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_retention_by_campaign(self) -> Dict[Campaign, float]:
        """
        Searches subscription average durations by Campaign.
        """
        frequencies: Dict[Campaign, int] = {}
        for campaign in Campaign.active.search(self.search):
            logic: CampaignLogic = CampaignLogic(campaign)
            subscriptions: QuerySet = logic.get_subscriptions(
                start=self.start, end=self.end
            )
            total_life: int = sum(
                subscription.life for subscription in subscriptions
            )
            total_subscriptions: int = subscriptions.count() or 0.0001
            frequencies[campaign] = total_life / total_subscriptions
        logger.debug("Average Life by Campaign: %s", frequencies)
        frequencies: Dict[Campaign, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_retention_by_product(self) -> Dict[Product, float]:
        """
        Searches subscription average durations by Product.
        """
        frequencies: Dict[Product, int] = {}
        for product in Product.active.search(self.search):
            logic: ProductLogic = ProductLogic(product)
            subscriptions: QuerySet = logic.get_subscriptions(
                start=self.start, end=self.end
            )
            total_life: int = sum(
                subscription.life for subscription in subscriptions
            )
            total_subscriptions: int = subscriptions.count() or 0.0001
            frequencies[product] = total_life / total_subscriptions
        logger.debug("Average Life by Product: %s", frequencies)
        frequencies: Dict[Product, int] = dict(
            filter(lambda x: x[1], frequencies.items())
        )
        return dict(
            sorted(
                frequencies.items(), key=lambda x: x[1], reverse=True
            )
        )

    def get_events_by_date(self) -> Dict[str, int]:
        """
        Searches all events.
        """
        histogram: Dict[str, int] = {}
        current: datetime = self.start
        while current <= self.end:
            histogram[current.strftime(self.DATE_FORMAT)] = 0
            current += timedelta(days=1)
        events: QuerySet = EventLogic.get_events(
            start=self.start, end=self.end
        )
        for event in events:
            date: str = event.created_at.strftime(self.DATE_FORMAT)
            histogram[date] += 1
        logger.debug("Events by Date: %s", histogram)
        return histogram
