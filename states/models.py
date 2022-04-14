from countries.models import Country
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
                | Q(country__title__icontains=search)
            )
        return queryset


class State(models.Model):
    """
    State Model
    """

    title: models.CharField = models.CharField(
        max_length=50,
        null=False,
    )
    country: models.ForeignKey = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
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
        return f"<{self.__class__.__name__}: {self.country.title}, {self.title}>"
