# app/models/format.py
from django.db import models
from .collection import Collection
from .theme_color import Theme

class Format(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='formats/', blank=True, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='formats')

    # Optional: direct relation to themes via a through model (see below)
    themes = models.ManyToManyField(Theme, through='FormatTheme', related_name='formats', blank=True)

    class Meta:
        unique_together = [('collection', 'title')]  # same format title cannot repeat inside the same collection

    def __str__(self):
        return f"{self.title} ({self.collection.title})"
    
    def get_image(self, obj):
        return obj.image.name if obj.image else None
