from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from pages.models import Page


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
                | Q(site__icontains=search)
                | Q(author__icontains=search)
                | Q(keywords__icontains=search)
                | Q(description__icontains=search)
            )
        return queryset


class Metadata(models.Model):
    """
    Page Metadata Model
    """

    page: models.OneToOneField = models.OneToOneField(
        Page,
        on_delete=models.CASCADE,
        null=False,
    )
    title: models.CharField = models.CharField(
        max_length=200, null=True
    )
    site: models.CharField = models.CharField(
        max_length=200, null=True
    )
    image: models.CharField = models.CharField(
        max_length=200, null=True
    )
    locale: models.CharField = models.CharField(
        max_length=50, null=True
    )
    description: models.CharField = models.CharField(
        max_length=500, null=True
    )
    keywords: models.CharField = models.CharField(
        max_length=200, null=True
    )
    author: models.CharField = models.CharField(
        max_length=200, null=True
    )
    viewport: models.CharField = models.CharField(
        max_length=100, null=True
    )
    published_at: models.DateTimeField = models.DateTimeField(
        null=True
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
