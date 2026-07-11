from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, ForgetPasswordSerializer
from .models import User, PasswordResetOTP

from datetime import timedelta
import random

from .email import send_otp_email

# Create your views here.
def hello(request):
    return JsonResponse({"hello":"cookcircle"})

class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "Email already registered."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = User(
                username = email,
                email = email
            )

            user.set_password(password)
            user.save()

            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
                
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    serializer_class = ForgetPasswordSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        otp = str(random.randint(100000, 999999))

        PasswordResetOTP.objects.create(
            user=user,
            otp=otp,
            expires_at=timezone.now()+timedelta(minutes=5)
        )

        send_otp_email(email, otp)

        return Response(
            {"message": "OTP sent successfully"},
            status = status.HTTP_200_OK
        )

        
        
