from clients.models import Client
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from metrics.models import Metric


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
                Q(client__name__icontains=search)
                | Q(client__email__icontains=search)
                | Q(metric__campaign__title__icontains=search)
                | Q(
                    metric__campaign__audience__title__icontains=search
                )
                | Q(metric__campaign__city__title__icontains=search)
                | Q(
                    metric__campaign__city__state__title__icontains=search
                )
                | Q(
                    metric__campaign__city__state__country__title__icontains=search
                )
                | Q(metric__page__title__icontains=search)
                | Q(metric__page__url__icontains=search)
                | Q(metric__page__metadata__title__icontains=search)
                | Q(metric__page__metadata__site__icontains=search)
                | Q(metric__page__metadata__author__icontains=search)
                | Q(
                    metric__page__metadata__keywords__icontains=search
                )
                | Q(
                    metric__page__metadata__description__icontains=search
                )
            )
        return queryset


class Event(models.Model):
    """
    Event Model
    """

    client: models.ForeignKey = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=False,
    )
    metric: models.ForeignKey = models.ForeignKey(
        Metric,
        on_delete=models.CASCADE,
        null=False,
    )
    value: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=False,
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True
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
        return f"<{self.__class__.__name__}: {self.metric}, {self.value}>"
