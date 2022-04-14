from audiences.models import Audience
from cities.models import City
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet


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
                Q(title__icontains=search)
                | Q(audience__title__icontains=search)
                | Q(city__title__icontains=search)
                | Q(city__state__title__icontains=search)
                | Q(city__state__country__title__icontains=search)
            )
        return queryset


class Campaign(models.Model):
    """
    Campaign Model
    """

    title: models.CharField = models.CharField(max_length=200)
    audience: models.ForeignKey = models.ForeignKey(
        Audience, on_delete=models.CASCADE
    )
    city: models.ForeignKey = models.ForeignKey(
        City, on_delete=models.CASCADE
    )
    spend: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=False,
        default=0,
    )
    is_active: models.BooleanField = models.BooleanField(
        default=False
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
        return f"<{self.__class__.__name__}: {self.title}>"
