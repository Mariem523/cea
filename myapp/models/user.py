# myapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    We extend AbstractUser so you can customize later.
    By default you'll get: username, password, email, is_staff, is_superuser, etc.
    """
    # add extra fields here if you like, e.g.:
    # bio = models.TextField(blank=True)
    pass
    