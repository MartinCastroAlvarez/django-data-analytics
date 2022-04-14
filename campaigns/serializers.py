from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from campaigns.models import Campaign


class CampaignSerializer(HyperlinkedModelSerializer):
    """
    Campaign Model Serializer.
    """

    class Meta:
        model: Campaign = Campaign
        fields: List[str] = [
            "id",
            "title",
            "audience",
            "is_active",
            "city",
            "spend",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "deleted_at",
        ]
