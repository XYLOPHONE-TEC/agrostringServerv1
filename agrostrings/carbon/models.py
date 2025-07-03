from django.db import models

from django.conf import settings

class FarmerCarbonData(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    measured_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='measured_data', null=True)
    date_recorded = models.DateField(auto_now_add=True)

# New data sections:
class TreeData(models.Model):
    record = models.OneToOneField(FarmerCarbonData, on_delete=models.CASCADE)
    num_trees = models.PositiveIntegerField()
    avg_height_m = models.FloatField()
    avg_age_years = models.FloatField()
    pct_indigenous = models.FloatField()

class FertilizerData(models.Model):
    record = models.OneToOneField(FarmerCarbonData, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=[('organic','Organic'),('chemical','Chemical'),('mixed','Mixed')])
    qty_kg = models.FloatField()
    freq_per_season = models.IntegerField()

class EnergyData(models.Model):
    record = models.OneToOneField(FarmerCarbonData, on_delete=models.CASCADE)
    uses_solar = models.BooleanField(default=False)
    pct_solar = models.FloatField(null=True, blank=True)

class WasteData(models.Model):
    record = models.OneToOneField(FarmerCarbonData, on_delete=models.CASCADE)
    burns_waste = models.BooleanField(default=False)
    uses_compost = models.BooleanField(default=False)
    waste_separation = models.BooleanField(default=False)

class CropData(models.Model):
    record = models.OneToOneField(FarmerCarbonData, on_delete=models.CASCADE)
    crop_types = models.CharField(max_length=200)  # comma-separated
    intercropping = models.BooleanField(default=False)
    pct_land_used = models.FloatField()
    pesticide_type = models.CharField(max_length=20, choices=[('organic','Organic'),('chemical','Chemical')])
