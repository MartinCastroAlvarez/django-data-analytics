from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from cities.models import City


class CitySerializer(HyperlinkedModelSerializer):
    """
    City Model Serializer.
    """

    class Meta:
        model: City = City
        fields: List[str] = [
            "id",
            "title",
            "state",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "deleted_at",
        ]
