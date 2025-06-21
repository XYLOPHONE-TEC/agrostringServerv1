from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsFarmer, IsBuyer, IsAdmin, IsSuperAdmin, IsFieldOperator


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get_permissions(self):
        # Only super admin or field operator can access registration
        if self.request.method == "POST":
            role = self.request.data.get("role")
            user = self.request.user
            if role == "admin" or role == "field_operator":
                return [permissions.IsAuthenticated(), IsSuperAdmin()]
            elif role == "farmer":
                return [permissions.IsAuthenticated(), IsFieldOperator()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()


class FieldOperatorFarmersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsFieldOperator]

    def get_queryset(self):
        # Only field operators can view their registered farmers
        user = self.request.user
        if user.role == "field_operator":
            return User.objects.filter(registered_by=user, role="farmer")
        return User.objects.none()


class LoginView(APIView):
    def post(self, request):
        from .serializers import LoginSerializer

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        # Determine dashboard
        dashboard_url = {
            "farmer": "/api/users/dashboard/farmer/",
            "buyer": "/api/users/dashboard/buyer/",
            "admin": "/api/users/dashboard/admin/",
        }.get(user.role, "/")

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "dashboard": dashboard_url,
                "user": UserSerializer(user).data,
            }
        )


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class FarmerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsFarmer]

    def get(self, request):
        return Response(
            {
                "message": "Welcome to the Farmer dashboard",
                "user": request.user.username,
            }
        )


class BuyerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        return Response(
            {"message": "Welcome to the Buyer dashboard", "user": request.user.username}
        )


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response(
            {"message": "Welcome to the Admin dashboard", "user": request.user.username}
        )
