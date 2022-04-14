from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from states.models import State


class StateSerializer(HyperlinkedModelSerializer):
    """
    State Model Serializer.
    """

    class Meta:
        model: State = State
        fields: List[str] = [
            "id",
            "title",
            "country",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "deleted_at",
        ]
