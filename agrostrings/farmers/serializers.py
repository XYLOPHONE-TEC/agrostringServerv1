from rest_framework import serializers
from .models import Produce  # CarbonTracker


class ProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = "__all__"
        read_only_fields = ["farmer", "posted_at", "status"]


# class CarbonTrackerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CarbonTracker
#         fields = '__all__'
#         read_only_fields = ['farmer', 'last_updated']
