from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions, filters
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
    permission_classes = [
        permissions.IsAuthenticated,
        IsFieldOperator | IsAdmin | IsSuperAdmin,
    ]

    def get_queryset(self):
        user = self.request.user
        if user.role == "field_operator":
            return User.objects.filter(registered_by=user, role="farmer")
        elif user.role == "admin" or getattr(user, "is_super_admin", False):
            # Admins and super admin can see all farmers registered by any field operator
            return User.objects.filter(role="farmer")
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


# should take research about this
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


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin | IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ["role", "username", "district", "phone_number"]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get("role")
        if role:
            queryset = queryset.filter(role=role)
        return queryset


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin | IsAdmin]
    lookup_field = "id"


class AdminListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    def get_queryset(self):
        return User.objects.filter(role="admin", is_super_admin=False)


# class UserUpdateView(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated, IsSuperAdmin | IsAdmin]
#     lookup_field = 'id'


# class UserDeleteView(generics.DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]
#     lookup_field = 'id'
