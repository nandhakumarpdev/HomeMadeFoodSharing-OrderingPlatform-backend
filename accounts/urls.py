from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('user-register', views.RegisterAPIView.as_view()),
    path('forgot-password', views.ForgotPasswordView.as_view()),
]
