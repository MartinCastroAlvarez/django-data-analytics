from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from subscriptions.models import Subscription


class SubscriptionSerializer(HyperlinkedModelSerializer):
    """
    Subscription Model Serializer.
    """

    class Meta:
        model: Subscription = Subscription
        fields: List[str] = [
            "id",
            "event",
            "product",
            "price",
            "created_at",
            "updated_at",
            "canceled_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "deleted_at",
        ]
