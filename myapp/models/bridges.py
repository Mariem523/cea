# app/models/bridges.py
from django.db import models
from .collection import Collection
from .theme_color import Theme
from .format import Format

class CollectionTheme(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='collection_themes')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='collection_themes')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('collection', 'theme')]

    def __str__(self):
        return f"{self.collection} ↔ {self.theme}"

class FormatTheme(models.Model):
    format = models.ForeignKey(Format, on_delete=models.CASCADE, related_name='format_themes')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='format_themes')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('format', 'theme')]

    def __str__(self):
        return f"{self.format} ↔ {self.theme}"
