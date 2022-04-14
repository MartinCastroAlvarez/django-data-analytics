from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from events.models import Event


class EventSerializer(HyperlinkedModelSerializer):
    """
    Event Model Serializer.
    """

    class Meta:
        model: Event = Event
        fields: List[str] = [
            "id",
            "client",
            "metric",
            "value",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "deleted_at",
        ]
