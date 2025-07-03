from django.db import models

from django.conf import settings
from django.contrib.auth.models import User


class Produce(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="produce"
    )
    crop_type = models.CharField(max_length=100)  # No choices — fully flexible
    quantity_kg = models.FloatField()
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    region = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="produce_images/", blank=True, null=True
    )  # Allow farmers to upload photos
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.crop_type} by {self.farmer.username}"



class FarmerCommunityQuestion(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class FarmInputRequest(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tool_name = models.CharField(max_length=100)
    purpose = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)



class CommunityReply(models.Model):
    question = models.ForeignKey(FarmerCommunityQuestion, on_delete=models.CASCADE, related_name='replies')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class AdminReplyToRequest(models.Model):
    request = models.ForeignKey(FarmInputRequest, on_delete=models.CASCADE, related_name='admin_replies')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)