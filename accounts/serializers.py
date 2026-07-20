from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", "email", "phone_number", "profile_image", "bio", "city", "state", "country", "pincode", "latitude", "longitude", "is_verified", "created_at",
        ]
        read_only_fields = [
            "id",
            "is_verified",
            "created_at"
        ]