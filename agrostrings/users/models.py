from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES = (
        ("farmer", "Farmer"),
        ("buyer", "Buyer"),
        ("admin", "Admin"),
        ("field_operator", "Field Operator"),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)
    district = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, null=True)  # ✅ Make email optional
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    operator_id = models.CharField(
        max_length=30, unique=False, null=True, blank=True
    )  # For field operators
    registered_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="registered_farmers",
    )  # For farmers
    is_super_admin = models.BooleanField(
        default=False
    )  # Only one user should have this True

    def __str__(self):
        return f"{self.username} ({self.role})"




class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=10)