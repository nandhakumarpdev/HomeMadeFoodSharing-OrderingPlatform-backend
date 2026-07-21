from rest_framework import serializers
from .models import FoodImage, FoodPost

class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields = ["id", "image"]

class FoodPostSerializer(serializers.ModelSerializer):
    images = FoodImageSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = FoodPost
        fields = [
            "id",
            "user",
            "food_name",
            "food_description",
            "meals_type",
            "quantity_available",
            "unit",
            "price",
            "available_date",
            "available_from",
            "available_until",
            "status",
            "images"
        ]
