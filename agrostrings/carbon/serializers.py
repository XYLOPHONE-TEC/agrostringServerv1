from rest_framework import serializers
from .models import FarmerCarbonData, TreeData, FertilizerData, EnergyData, WasteData, CropData

from django.contrib.auth import get_user_model

User = get_user_model()

#from django.conf import settings
class TreeDataSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TreeData 
        fields = '__all__'
        extra_kwargs = {
            'record': {'read_only': True}  # Ensure record is read-only
        }


# Repeat similar for FertilizerDataSerializer, EnergyDataSerializer, etc.
class FertilizerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FertilizerData
        fields = '__all__'
        extra_kwargs = {
            'record': {'read_only': True}  # Ensure record is read-only
        }

class EnergyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyData
        fields = '__all__'
        extra_kwargs = {
            'record': {'read_only': True}  # Ensure record is read-only
        }

class WasteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteData
        fields = '__all__'
        extra_kwargs = {
            'record': {'read_only': True}  # Ensure record is read-only
        }

class CropDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropData
        fields = '__all__'
        extra_kwargs = {
            'record': {'read_only': True}  # Ensure record is read-only
        }






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
    

    class Meta:
        model = FarmerCarbonData
        fields = ['id', 'farmer', 'measured_by', 'date_recorded', 'tree', 'fertilizer', 'energy', 'waste', 'crop', 'score']

    def get_score(self, obj):
        from .services import calculate_score
        return calculate_score(obj)
    


    def create(self, validated_data):
        tree_data = validated_data.pop('treedata')
        fertilizer_data = validated_data.pop('fertilizerdata')
        energy_data = validated_data.pop('energydata')
        waste_data = validated_data.pop('wastedata')
        crop_data = validated_data.pop('cropdata')

        carbon_record = FarmerCarbonData.objects.create(**validated_data)

        TreeData.objects.create(record=carbon_record, **tree_data)
        FertilizerData.objects.create(record=carbon_record, **fertilizer_data)
        EnergyData.objects.create(record=carbon_record, **energy_data)
        WasteData.objects.create(record=carbon_record, **waste_data)
        CropData.objects.create(record=carbon_record, **crop_data)

        return carbon_record

