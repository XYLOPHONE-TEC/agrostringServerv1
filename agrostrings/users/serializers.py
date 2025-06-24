from rest_framework import serializers
from .models import User, PasswordResetCode
from django.contrib.auth import authenticate
import random
from utils.sms import send_sms_africastalking
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



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
            "operator_id",
            "registered_by",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.get("role")
        request = self.context.get("request")
        current_user = request.user if request else None

        # Super admin can create admins and field operators
        if role == "admin" or role == "field_operator":
            if not current_user or not getattr(current_user, "is_super_admin", False):
                raise serializers.ValidationError(
                    "Only the super admin can register admins or field operators."
                )
            if role == "field_operator":
                # operator_id must be provided
                operator_id = validated_data.get("operator_id")
                if not operator_id:
                    raise serializers.ValidationError(
                        "operator_id is required for field operators."
                    )
        # Field operator can create farmers
        elif role == "farmer":
            if not current_user or current_user.role != "field_operator":
                raise serializers.ValidationError(
                    "Only field operators can register farmers."
                )
            validated_data["registered_by"] = current_user
            validated_data["operator_id"] = current_user.operator_id
        # Prevent anyone else from registering
        else:
            raise serializers.ValidationError("Invalid role for registration.")

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
                raise serializers.ValidationError(
                    "Phone number and district are required for farmers."
                )

            try:
                user = User.objects.get(
                    phone_number=phone, role="farmer", district=district
                )
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "Farmer with those credentials not found."
                )

        elif role in ["buyer", "admin", "field_operator"]:
            username = data.get("username")
            password = data.get("password")
            phone = data.get("phone_number")

            if not username or not password or not phone:
                raise serializers.ValidationError(
                    "Username, phone number, and password are required for buyers, admins, and field operators."
                )

            user = authenticate(username=username, password=password)
            if not user or user.role != role or user.phone_number != phone:
                raise serializers.ValidationError(f"Invalid {role} credentials.")

        else:
            raise serializers.ValidationError("Invalid role or missing role field.")

        return user
    




class UserUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "phone_number",
            "district",
            "email"
        ]
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
        phone = data['phone_number']
        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with that phone number does not exist.")

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
        phone = data['phone_number']
        code = data['code']
        new_password = data['new_password']

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid phone number.")

        try:
            reset_entry = PasswordResetCode.objects.filter(user=user, code=code).latest('created_at')
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
