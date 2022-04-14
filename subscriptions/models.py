from datetime import datetime

from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from events.models import Event
from products.models import Product


class ActiveManager(models.Manager):
    """
    Django Model Manager.
    """

    def get_queryset(self) -> QuerySet:
        """
        QuerySet filter for active rows.
        """
        return super().get_queryset().filter(deleted_at=None)

    def search(
        self, search: str = "", start: str = "", end: str = ""
    ) -> QuerySet:
        """
        Search & filter active objects.
        """
        queryset: QuerySet = self.get_queryset()
        if start and end:
            queryset: QuerySet = queryset.filter(
                created_at__gte=start,
                created_at__lte=end,
            )
        if search:
            queryset: Queryset = queryset.filter(
                Q(product__title__icontains=search)
                | Q(event__client__name__icontains=search)
                | Q(event__client__email__icontains=search)
                | Q(product__title__icontains=search)
                | Q(event__metric__campaign__title__icontains=search)
                | Q(
                    event__metric__campaign__audience__title__icontains=search
                )
                | Q(
                    event__metric__campaign__city__title__icontains=search
                )
                | Q(
                    event__metric__campaign__city__state__title__icontains=search
                )
                | Q(
                    event__metric__campaign__city__state__country__title__icontains=search
                )
            )
        return queryset


class Subscription(models.Model):
    """
    Subscription Model
    """

    event: models.ForeignKey = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=False,
    )
    product: models.ForeignKey = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=False,
    )
    price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=False,
        default=0,
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True
    )
    canceled_at: models.DateTimeField = models.DateTimeField(
        null=True
    )
    deleted_at: models.DateTimeField = models.DateTimeField(
        default=None, null=True
    )

    objects: models.Manager = models.Manager()
    active: ActiveManager = ActiveManager()

    def __str__(self) -> str:
        """
        String serializer.
        """
        return f"<{self.__class__.__name__}: {self.event.client.name}, {self.product.title}>"

    @property
    def dow(self) -> str:
        """
        Returns day of the week of the Subscription.
        """
        return self.created_at.strftime("%a")

    @property
    def day(self) -> int:
        """
        Returns day of the month of the Subscription.
        """
        return self.created_at.day

    @property
    def hod(self) -> int:
        """
        Returns hour of the day of the Subscription.
        """
        return self.created_at.hour

    @property
    def month(self) -> str:
        """
        Returns month of the year of the Subscription.
        """
        return self.created_at.strftime("%b")

    @property
    def margin(self) -> float:
        """
        Returns the marginal revenue of this Subscription
        """
        return self.price - self.product.cost

    @property
    def life(self) -> int:
        """
        Returns the amount of months that this Subscription was live.
        """
        if self.canceled_at:
            until: datetime = self.canceled_at
        else:
            until: datetime = datetime.now()
        return (
            (until.year - self.created_at.year) * 12
            + until.month
            - self.created_at.month
        )

    @property
    def ltv(self) -> float:
        """
        Returns the LTV of this Subscription.
        """
        return self.life * self.margin
