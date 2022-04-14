from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from metadata.models import Metadata


class MetadataSerializer(HyperlinkedModelSerializer):
    """
    Metadata Model Serializer.
    """

    class Meta:
        model: Metadata = Metadata
        fields: List[str] = [
            "id",
            "page",
            "title",
            "site",
            "image",
            "locale",
            "description",
            "keywords",
            "author",
            "viewport",
            "published_at",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "id",
            "page",
            "title",
            "site",
            "image",
            "locale",
            "description",
            "keywords",
            "author",
            "viewport",
            "published_at",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
