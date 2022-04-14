from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from audiences.models import Audience


class AudienceSerializer(HyperlinkedModelSerializer):
    """
    Audience Model Serializer.
    """

    class Meta:
        model: Audience = Audience
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
