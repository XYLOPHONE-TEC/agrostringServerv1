from django.shortcuts import render
from rest_framework import generics
from .models import FarmerCarbonData
from .serializers import FarmerCarbonDataSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .services import calculate_score
from django.utils.translation import gettext_lazy as _

class FarmerCarbonDataCreate(generics.CreateAPIView):
    queryset = FarmerCarbonData.objects.all()
    serializer_class = FarmerCarbonDataSerializer

class FarmerCarbonDataDetail(generics.RetrieveAPIView):
    queryset = FarmerCarbonData.objects.all()
    serializer_class = FarmerCarbonDataSerializer




class FarmerCarbonSummary(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = []
        for record in FarmerCarbonData.objects.all():
            score_result = calculate_score(record)
            data.append({
                'farmer': record.farmer.username,
                'score': score_result['total'],
                'level': score_result['level'],
                'date': record.date_recorded
            })
        return Response(data)
