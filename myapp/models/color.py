# app/models/color.py
from django.db import models
from django.core.exceptions import ValidationError
from .collection import Collection
from .format import Format
from .theme_color import Theme
from .bridges import CollectionTheme, FormatTheme

class Color(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True, related_name='colors')
    image = models.ImageField(upload_to='colors/', blank=True, null=True)

    # Always tied to exactly one collection
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='colors')

    # Optional format (required when collection.type == WITH_FORMATS)
    format = models.ForeignKey(Format, on_delete=models.CASCADE, null=True, blank=True, related_name='colors')

    class Meta:
        # Avoid duplicates of the same color name under the same (collection, format, theme) combination
        constraints = [
            models.UniqueConstraint(
                fields=['collection', 'format', 'theme', 'title'],
                name='uniq_color_per_collection_format_theme_title'
            ),
        ]

    def clean(self):
        # If collection requires formats, format must be set
        if self.collection and self.collection.type == Collection.CollectionType.WITH_FORMATS and self.format is None:
            raise ValidationError("This collection requires a format for each color.")

        # If a format is set, it must belong to the same collection
        if self.format and self.format.collection_id != self.collection_id:
            raise ValidationError("The selected format does not belong to the same collection as the color.")

        # If a theme is set, verify it’s linked either to the collection or to the format
        if self.theme:
            linked_to_collection = CollectionTheme.objects.filter(
                collection=self.collection, theme=self.theme, is_active=True
            ).exists()

            linked_to_format = False
            if self.format:
                linked_to_format = FormatTheme.objects.filter(
                    format=self.format, theme=self.theme, is_active=True
                ).exists()

            if not (linked_to_collection or linked_to_format):
                raise ValidationError("Theme must be linked to the collection or the selected format.")

    def __str__(self):
        t = self.theme.title if self.theme else "NoTheme"
        f = self.format.title if self.format else "NoFormat"
        return f"{self.title} [{self.collection.title} / {f} / {t}]"
    
    def get_image(self, obj):
        return obj.image.name if obj.image else None
