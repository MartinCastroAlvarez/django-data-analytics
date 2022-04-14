from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from metrics.models import Metric


class MetricSerializer(HyperlinkedModelSerializer):
    """
    Metric Model Serializer.
    """

    class Meta:
        model: Metric = Metric
        fields: List[str] = [
            "id",
            "campaign",
            "metric_type",
            "page",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "deleted_at",
        ]
