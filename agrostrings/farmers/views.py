from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Produce #CarbonTracker
from .serializers import ProduceSerializer #CarbonTrackerSerializer

class FarmerProduceListCreateView(generics.ListCreateAPIView):
    serializer_class = ProduceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Produce.objects.filter(farmer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

class FarmerProduceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProduceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Produce.objects.filter(farmer=self.request.user)

# class FarmerCarbonView(generics.RetrieveUpdateAPIView):
#     serializer_class = CarbonTrackerSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         obj, created = CarbonTracker.objects.get_or_create(farmer=self.request.user)
#         return obj

