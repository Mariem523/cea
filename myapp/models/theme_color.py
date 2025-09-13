# app/models/theme.py
from django.db import models

class Theme(models.Model):
    # formerly ThemeColor
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    def get_image(self, obj):
        return obj.image.name if obj.image else None
    