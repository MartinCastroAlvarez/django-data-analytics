from typing import List

from rest_framework.serializers import HyperlinkedModelSerializer

from products.models import Product


class ProductSerializer(HyperlinkedModelSerializer):
    """
    Product Model Serializer.
    """

    class Meta:
        model: Product = Product
        fields: List[str] = [
            "id",
            "title",
            "cost",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields: List[str] = [
            "deleted_at",
        ]
