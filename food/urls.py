from django.urls import path
from . import views

urlpatterns = [

    path('get-foodlist', views.AllFoodPostView.as_view()),
    path('post-food', views.FoodPostView.as_view()),  
    path('upload-image', views.FoodImageView.as_view()),  

    path('get-food-by-id/<int:id>', views.FoodById.as_view()),

    path('food-showcase', views.FoodShowCaseView.as_view()),
]
