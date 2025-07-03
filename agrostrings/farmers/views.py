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




# views.py

from rest_framework import viewsets, permissions
from .models import (
    FarmerCommunityQuestion,
    CommunityReply,
    FarmInputRequest,
    AdminReplyToRequest
)
from .serializers import (
    FarmerCommunityQuestionSerializer,
    CommunityReplySerializer,
    FarmInputRequestSerializer,
    AdminReplyToRequestSerializer
)

class FarmerCommunityQuestionViewSet(viewsets.ModelViewSet):
    queryset = FarmerCommunityQuestion.objects.all().order_by('-created_at')
    serializer_class = FarmerCommunityQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommunityReplyViewSet(viewsets.ModelViewSet):
    queryset = CommunityReply.objects.all().order_by('created_at')
    serializer_class = CommunityReplySerializer
    permission_classes = [permissions.IsAuthenticated]


class FarmInputRequestViewSet(viewsets.ModelViewSet):
    queryset = FarmInputRequest.objects.all().order_by('-created_at')
    serializer_class = FarmInputRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class AdminReplyToRequestViewSet(viewsets.ModelViewSet):
    queryset = AdminReplyToRequest.objects.all().order_by('created_at')
    serializer_class = AdminReplyToRequestSerializer
    permission_classes = [permissions.IsAuthenticated]



