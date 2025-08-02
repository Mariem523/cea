import os
import uuid
from django.db import models
from django.utils import timezone

def catalog_image_upload_to(instance, filename):
    """
    Store images under MEDIA_ROOT/catalogs/images/YYYY/MM/<uuid>.<ext>
    """
    ext = filename.rsplit('.', 1)[-1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    # use now() rather than instance.created_at
    subdir = timezone.now().strftime("%Y/%m")
    return os.path.join("catalogs", "images", subdir, unique_name)

def catalog_pdf_upload_to(instance, filename):
    """
    Store PDFs under MEDIA_ROOT/catalogs/pdfs/YYYY/MM/<uuid>.<ext>
    """
    ext = filename.rsplit('.', 1)[-1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    subdir = timezone.now().strftime("%Y/%Y/%m")  # you can choose YYYY/MM
    return os.path.join("catalogs", "pdfs", subdir, unique_name)

class Catalog(models.Model):
    PUBLIC  = "public"
    PRIVATE = "private"
    TYPE_CHOICES = [
        (PUBLIC,  "Public"),
        (PRIVATE, "Private"),
    ]

    title      = models.CharField(max_length=255)
    type       = models.CharField(max_length=7, choices=TYPE_CHOICES, default=PUBLIC)
    image      = models.ImageField(upload_to=catalog_image_upload_to, blank=True, null=True)
    pdf_file   = models.FileField(upload_to=catalog_pdf_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.type})"
