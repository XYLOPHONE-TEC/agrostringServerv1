from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsFarmer, IsBuyer, IsAdmin


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# class LoginView(APIView):
#     def post(self, request):
#         from .serializers import LoginSerializer
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": UserSerializer(user).data,
#         })


class LoginView(APIView):
    def post(self, request):
        from .serializers import LoginSerializer
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        # Determine dashboard
        dashboard_url = {
            'farmer': '/api/users/dashboard/farmer/',
            'buyer': '/api/users/dashboard/buyer/',
            'admin': '/api/users/dashboard/admin/',
        }.get(user.role, '/')

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "dashboard": dashboard_url,
            "user": UserSerializer(user).data,
        })




class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)



class FarmerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsFarmer]

    def get(self, request):
        return Response({"message": "Welcome to the Farmer dashboard", "user": request.user.username})


class BuyerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        return Response({"message": "Welcome to the Buyer dashboard", "user": request.user.username})


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Welcome to the Admin dashboard", "user": request.user.username})