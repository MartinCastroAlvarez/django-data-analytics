from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from clients.models import Client


class ClientSerializer(HyperlinkedModelSerializer):
    """
    Client Model Serializer.
    """

    class Meta:
        model: Client = Client
        fields: List[str] = [
            "id",
            "name",
            "email",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "deleted_at",
        ]
