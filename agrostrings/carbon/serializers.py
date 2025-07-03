from rest_framework import serializers
from .models import FarmerCarbonData, TreeData, FertilizerData, EnergyData, WasteData, CropData

from django.contrib.auth import get_user_model

User = get_user_model()

#from django.conf import settings
class TreeDataSerializer(serializers.ModelSerializer):
    class Meta: model = TreeData; fields = '__all__'

# Repeat similar for FertilizerDataSerializer, EnergyDataSerializer, etc.
class FertilizerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FertilizerData
        fields = '__all__'

class EnergyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyData
        fields = '__all__'

class WasteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteData
        fields = '__all__'

class CropDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropData
        fields = '__all__'






class FarmerCarbonDataSerializer(serializers.ModelSerializer):
    tree = TreeDataSerializer(source='treedata')
    fertilizer = FertilizerDataSerializer(source='fertilizerdata')
    energy = EnergyDataSerializer(source='energydata')
    waste = WasteDataSerializer(source='wastedata')
    crop = CropDataSerializer(source='cropdata')
    score = serializers.SerializerMethodField()

    farmer = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    measured_by = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = FarmerCarbonData
        fields = ['id', 'farmer', 'measured_by', 'date_recorded', 'tree', 'fertilizer', 'energy', 'waste', 'crop', 'score']

    def get_score(self, obj):
        from .services import calculate_score
        return calculate_score(obj)

