from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from .serializers import ProduceSerializer

from rest_framework.exceptions import PermissionDenied
from .models import *
from .serializers import *
from users.permissions import IsFarmer, IsAdmin, IsSuperAdmin

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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




class FarmerCommunityQuestionListCreateView(generics.ListCreateAPIView):
    queryset = FarmerCommunityQuestion.objects.all().order_by('-created_at')
    serializer_class = FarmerCommunityQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)


class CommunityReplyCreateView(generics.CreateAPIView):
    queryset = CommunityReply.objects.all()
    serializer_class = CommunityReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    

class CommunityRepliesByQuestionView(generics.ListAPIView):
    serializer_class = CommunityReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        question_id = self.request.query_params.get('question')
        return CommunityReply.objects.filter(question_id=question_id).order_by('created_at')



# TOOL REQUESTS (Private)

class FarmInputRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = FarmInputRequestSerializer
    permission_classes = [IsFarmer]

    def get_queryset(self):
        # Return only farmer's own requests
        return FarmInputRequest.objects.filter(farmer=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)


class AdminViewAllFarmInputRequests(generics.ListAPIView):
    queryset = FarmInputRequest.objects.all().order_by('-created_at')
    serializer_class = FarmInputRequestSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_reviewed', 'farmer__district']


class AdminReplyToRequestCreateView(generics.CreateAPIView):
    queryset = AdminReplyToRequest.objects.all()
    serializer_class = AdminReplyToRequestSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]

    def perform_create(self, serializer):
        if self.request.user.role != 'admin' and not self.request.user.is_super_admin:
            raise PermissionDenied("Only admins can reply to requests.")
        serializer.save(admin=self.request.user)


class AdminRepliesByRequestView(generics.ListAPIView):
    serializer_class = AdminReplyToRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request_id = self.request.query_params.get('request')
        return AdminReplyToRequest.objects.filter(request_id=request_id).order_by('created_at')
