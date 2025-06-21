from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


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
    email = models.EmailField(blank=True, null=True)  # ✅ Make email optional
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
