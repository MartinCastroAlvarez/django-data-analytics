from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from countries.models import Country


class CountrySerializer(HyperlinkedModelSerializer):
    """
    Country Model Serializer.
    """

    class Meta:
        model: Country = Country
        fields: List[str] = [
            "id",
            "title",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "deleted_at",
        ]
