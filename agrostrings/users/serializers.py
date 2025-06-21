from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'role', 'district']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'role', 'district']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    district = serializers.CharField(required=False)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    def validate(self, data):
        role = data.get("role")

        if role == "farmer":
            phone = data.get("phone_number")
            district = data.get("district")

            if not phone or not district:
                raise serializers.ValidationError("Phone number and district are required for farmers.")
            
            try:
                user = User.objects.get(phone_number=phone, role="farmer", district=district)
            except User.DoesNotExist:
                raise serializers.ValidationError("Farmer with those credentials not found.")

        elif role == "buyer":
            username = data.get("username")
            password = data.get("password")
            phone = data.get("phone_number")

            if not username or not password or not phone:
                raise serializers.ValidationError("Username, phone number, and password are required for buyers.")

            user = authenticate(username=username, password=password)
            if not user or user.role != "buyer" or user.phone_number != phone:
                raise serializers.ValidationError("Invalid buyer credentials.")

        else:
            raise serializers.ValidationError("Invalid role or missing role field.")

        return user

