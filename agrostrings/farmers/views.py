from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Produce  # CarbonTracker
from .serializers import ProduceSerializer  # CarbonTrackerSerializer


class FarmerProduceListCreateView(generics.ListCreateAPIView):
    serializer_class = ProduceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "is_super_admin") and user.is_super_admin:
            return Produce.objects.all()
        elif hasattr(user, "role") and user.role == "admin":
            return Produce.objects.all()
        elif hasattr(user, "role") and user.role == "buyer":
            return Produce.objects.filter(status="approved")
        return Produce.objects.filter(farmer=user)

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user, status="pending")


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
