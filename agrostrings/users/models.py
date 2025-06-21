from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)
    district = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, null=True)  # ✅ Make email optional

    def __str__(self):
        return f"{self.username} ({self.role})"
