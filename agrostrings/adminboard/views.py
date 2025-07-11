from django.shortcuts import render
from rest_framework import generics, permissions, status as drf_status
from rest_framework.response import Response
from farmers.models import Produce
from farmers.serializers import ProduceSerializer
from users.permissions import IsAdmin, IsSuperAdmin
from django.utils.translation import gettext_lazy as _


class ProduceApproveRejectView(generics.UpdateAPIView):
    queryset = Produce.objects.all()
    serializer_class = ProduceSerializer
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]

    def patch(self, request, *args, **kwargs):
        produce = self.get_object()
        action = request.data.get("action")
        if action == "approve":
            produce.status = "approved"
        elif action == "reject":
            produce.status = "rejected"
        else:
            return Response(
                {"detail": "Invalid action."}, status=drf_status.HTTP_400_BAD_REQUEST
            )
        produce.save()
        return Response({"status": produce.status})


