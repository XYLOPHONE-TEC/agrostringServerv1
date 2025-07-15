from rest_framework import serializers
from .models import User, PasswordResetCode
from django.contrib.auth import authenticate
import random
from utils.sms import send_sms_africastalking
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.translation import gettext_lazy as _
import requests
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    operator_id = serializers.CharField(read_only=True)
    registered_by = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "phone_number",
            "role",
            "district",
            "country_code",
            "latitude",
            "longitude",
            "operator_id",
            "registered_by",
        ]
        read_only_fields = ["operator_id", "registered_by"]

    def get_registered_by(self, obj):
        if obj.registered_by:
            return obj.registered_by.username
        return None


class RegisterSerializer(serializers.ModelSerializer):
    operator_id = serializers.CharField(required=False, allow_blank=True)
    registered_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "phone_number",
            "role",
            "district",
            "country_code",
            "latitude",
            "longitude",
            "operator_id",
            "registered_by",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.get("role")
        request = self.context.get("request")
        current_user = request.user if request else None

        # Role-based access control
        if role in ["admin", "field_operator"]:
            if not current_user or not getattr(current_user, "is_super_admin", False):
                raise serializers.ValidationError("Only the super admin can register admins or field operators.")
            if role == "field_operator" and not validated_data.get("operator_id"):
                raise serializers.ValidationError("operator_id is required for field operators.")
        elif role == "farmer":
            if not current_user or current_user.role != "field_operator":
                raise serializers.ValidationError("Only field operators can register farmers.")
            validated_data["registered_by"] = current_user
            validated_data["operator_id"] = current_user.operator_id
        else:
            raise serializers.ValidationError("Invalid role for registration.")

        # Geocode location
        latitude = validated_data.get('latitude')
        longitude = validated_data.get('longitude')
        district = validated_data.get("district")
        country_code = validated_data.get("country_code")

        if (not latitude or not longitude) and district and country_code and settings.OPENWEATHERMAP_API_KEY:
            location_query = f"{district},{country_code},East Africa"
            base_url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": location_query,
                "limit": 1,
                "appid": settings.OPENWEATHERMAP_API_KEY,
            }
            try:
                response = requests.get(base_url, params=params)
                response.raise_for_status()
                data = response.json()
                if data:
                    location = data[0]
                    validated_data['latitude'] = location.get('lat')
                    validated_data['longitude'] = location.get('lon')
            except requests.exceptions.RequestException:
                pass  # Optional: log the exception

        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    district = serializers.CharField(required=False)

    def validate(self, data):
        phone = data.get("phone_number")
        district = data.get("district")
        username = data.get("username")
        password = data.get("password")

        # Try to authenticate as farmer first
        if phone and district:
            try:
                user = User.objects.get(phone_number=phone, district=district)
                if user.role == "farmer":
                    return user
            except User.DoesNotExist:
                pass  # Try other roles below

        # If not a farmer, try to authenticate as buyer, admin, or field_operator
        if username and password and phone:
            user = authenticate(username=username, password=password)
            if user and user.phone_number == phone:
                return user
            else:
                raise serializers.ValidationError("Invalid credentials.")

        raise serializers.ValidationError(
            "Provide phone number and district for farmers, or username, phone number, and password for other roles."
        )


class UserUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "phone_number", "district", "email"]
        extra_kwargs = {
            "username": {"required": False},
            "phone_number": {"required": False},
            "district": {"required": False},
            "email": {"required": False},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PasswordResetRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, data):
        phone = data["phone_number"]
        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with that phone number does not exist."
            )

        code = f"{random.randint(100000, 999999)}"
        PasswordResetCode.objects.create(user=user, code=code)

        # Send SMS
        message = f"Your password reset code is: {code}"
        send_sms_africastalking(phone, message)

        return {"message": "Reset code sent to your phone number."}


class PasswordResetConfirmSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data["phone_number"]
        code = data["code"]
        new_password = data["new_password"]

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid phone number.")

        try:
            reset_entry = PasswordResetCode.objects.filter(user=user, code=code).latest(
                "created_at"
            )
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired reset code.")

        if not reset_entry.is_valid():
            raise serializers.ValidationError("Reset code has expired.")

        user.set_password(new_password)
        user.save()
        reset_entry.delete()
        return {"message": "Password reset successful."}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError("Token is invalid or expired.")
