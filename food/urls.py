from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),

    path('post-food', views.FoodPostView.as_view()),    
]
