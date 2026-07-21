from django.db import models
from accounts.models import User

# Create your models here.

class FoodPost(models.Model):
    
    MEAL_TYPE_CHOICES = [
        ("BREAKFAST", "Breakfast"),
        ("LUNCH", "Lunch"),
        ("DINNER", "Dinner"),
        ("SNACKS", "Snacks"),
    ]

    UNIT_CHOICES = [
        ("PLATES", "Plates"),
        ("BOWL", "Bowl"),
        ("BOX", "Box"),
        ("PIECE", "Piece"),
        ("KG", "Kilogram"),
        ("GRAM", "Gram"),
        ("LITRE", "Litre"),
        ("ML", "Millilitre")
    ]

    STATUS_CHOICES = [
        ("COMING_SOON", "Coming Soon"),
        ("AVAILABLE", "Available"),
        ("SOLD_OUT", "Sold out"),
        ("EXPIRED", "Expired"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="food_posts"
    )

    food_name = models.CharField(max_length=150)
    food_description = models.TextField(blank=True)
    meals_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    
    quantity_available = models.PositiveIntegerField()
    unit = models.CharField(max_length=30, choices=UNIT_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    available_date = models.DateField()
    available_from = models.TimeField()
    available_until = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_name
    

class FoodImage(models.Model):
    
    food_post = models.ForeignKey(
        FoodPost,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="food_images/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_post.food_name} Image"


