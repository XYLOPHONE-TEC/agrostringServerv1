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




class CarbonActivity(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # or a FarmerProfile model
    uses_organic_fertilizer = models.BooleanField(default=False)
    uses_solar_energy = models.BooleanField(default=False)
    plants_trees = models.BooleanField(default=False)
    burns_waste = models.BooleanField(default=False)
    date_recorded = models.DateField(auto_now_add=True)

    def carbon_score(self):
        score = 0
        if self.uses_organic_fertilizer:
            score += 25
        if self.uses_solar_energy:
            score += 25
        if self.plants_trees:
            score += 25
        if not self.burns_waste:  # good if they don't burn
            score += 25
        return score

    def readiness_level(self):
        score = self.carbon_score()
        if score >= 75:
            return "High"
        elif score >= 50:
            return "Medium"
        else:
            return "Low"




# class CarbonTracker(models.Model):
#     farmer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     total_planted_trees = models.IntegerField(default=0)
#     sustainable_farming_score = models.FloatField(default=0.0)
#     last_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Carbon Data for {self.farmer.username}"
