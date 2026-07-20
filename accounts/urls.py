from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('user-register', views.UserRegister.as_view()),
    path('user-login', views.UserLogin.as_view()),
    path('forgot-password', views.ForgotPassword.as_view()),
    path('verify-otp', views.CheckOtp.as_view()),
    path('reset-password', views.ResetPassword.as_view()),

    # profile
    path('update-profile/<int:id>', views.UserProfileView.as_view()),
]
