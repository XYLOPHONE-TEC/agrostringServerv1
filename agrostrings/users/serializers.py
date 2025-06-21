from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
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

        elif role == "buyer":
            username = data.get("username")
            password = data.get("password")
            phone = data.get("phone_number")

            if not username or not password or not phone:
                raise serializers.ValidationError(
                    "Username, phone number, and password are required for buyers."
                )

            user = authenticate(username=username, password=password)
            if not user or user.role != "buyer" or user.phone_number != phone:
                raise serializers.ValidationError("Invalid buyer credentials.")

        else:
            raise serializers.ValidationError("Invalid role or missing role field.")

        return user
