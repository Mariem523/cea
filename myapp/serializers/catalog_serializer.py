from rest_framework import serializers
from ..models.catalog import Catalog
from django.urls import reverse

class CatalogSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model  = Catalog
        fields = ("id", "title", "type", "image", "download_url", "created_at")
        read_only_fields = fields
    def get_cover_url(self, obj: Catalog):
        if not obj.image:
            return None
        req = self.context.get("request")
        url = obj.image.url
        return req.build_absolute_uri(url) if req else url
    def get_download_url(self, obj: Catalog):
        req = self.context.get("request")
        # Your urls.py should name this route 'catalog-download'
        url = reverse("catalog-download", kwargs={"pk": obj.pk})
        return req.build_absolute_uri(url) if req else url