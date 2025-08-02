from rest_framework import serializers
from ..models.catalog import Catalog

class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Catalog
        fields = ("id", "title", "type", "image", "pdf_file", "created_at")
        read_only_fields = ("id", "created_at")

