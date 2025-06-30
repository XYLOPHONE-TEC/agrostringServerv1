from rest_framework import generics, permissions, status as drf_status
from rest_framework.response import Response
from .models import Produce
from .serializers import ProduceSerializer
from users.permissions import IsAdmin, IsSuperAdmin


class PublicProduceListView(generics.ListAPIView):
    queryset = Produce.objects.filter(status="approved")
    serializer_class = ProduceSerializer
    permission_classes = []  # No authentication required
