from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from pages.models import Page


class PageSerializer(HyperlinkedModelSerializer):
    """
    Page Model Serializer.
    """

    class Meta:
        model: Page = Page
        fields: List[str] = [
            "id",
            "title",
            "url",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "deleted_at",
        ]
