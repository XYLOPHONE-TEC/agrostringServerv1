from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Produce(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='produce')
    crop_type = models.CharField(max_length=100)  # No choices — fully flexible
    quantity_kg = models.FloatField()
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    region = models.CharField(max_length=100)
    image = models.ImageField(upload_to='produce_images/', blank=True, null=True)  # Allow farmers to upload photos
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.crop_type} by {self.farmer.username}"
