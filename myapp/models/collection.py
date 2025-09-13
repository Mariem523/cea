# app/models/collection.py
from django.db import models

class Collection(models.Model):
    class CollectionType(models.TextChoices):
        WITH_FORMATS = "WITH_FORMATS", "With Formats (Formats → Themes → Colors)"
        DIRECT_COLORS = "DIRECT_COLORS", "Direct Colors (Colors grouped by Formats)"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=50, choices=CollectionType.choices, default=CollectionType.WITH_FORMATS)
    image = models.ImageField(upload_to='collections/', blank=True, null=True)

    def __str__(self):
        return self.title
    def get_image(self, obj):
        return obj.image.name if obj.image else None