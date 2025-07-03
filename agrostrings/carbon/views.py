from django.shortcuts import render

from rest_framework import generics
from .models import FarmerCarbonData
from .serializers import FarmerCarbonDataSerializer

class FarmerCarbonDataCreate(generics.CreateAPIView):
    queryset = FarmerCarbonData.objects.all()
    serializer_class = FarmerCarbonDataSerializer

class FarmerCarbonDataDetail(generics.RetrieveAPIView):
    queryset = FarmerCarbonData.objects.all()
    serializer_class = FarmerCarbonDataSerializer
