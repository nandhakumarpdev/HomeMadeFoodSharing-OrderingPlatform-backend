from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, ForgetPasswordSerializer, UserProfileSerializer
from .models import User, PasswordResetOTP

from datetime import timedelta
import random

from .email import send_otp_email

# Create your views here.
def hello(request):
    return JsonResponse({"hello":"cookcircle"})

class UserRegister(APIView):
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

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Field already exists"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"error": "Email not exists"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(password):
            return Response(
                {"error":"Invalid password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User Login Successfully",
                "user_id": user.id,
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            },
            status= status.HTTP_200_OK
        )

class ForgotPassword(APIView):
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
        
class CheckOtp(APIView):

    def otp_validation(self, otp, user_id):
        check_otp = PasswordResetOTP.objects.filter(
            user_id=user_id,
            otp=otp
        ).last()
        return check_otp

    def post(self, request):
        otp = request.data.get("otp")
        user_id = request.data.get("user_id")

        if not otp:
            return Response(
                {"error": "Otp not entered"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        check_otp = self.otp_validation(otp, user_id)

        if check_otp is None:
            return Response(
                {"error": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        if check_otp.expires_at < timezone.now():
            return Response(
                {"error": "OTP has expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response (
            {
                "result": str(check_otp.otp) == str(otp)
        
            }
        )
    
class ResetPassword(APIView):
    def post(self, request):
        result = request.data.get("result")
        user_id = request.data.get("user_id")
        new_password = request.data.get("new_password")


        if not result:
            return Response(
                {"error": "Invalid result to send by frontend"},
                 status = status.HTTP_400_BAD_REQUEST
            )
        
        if result:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()

        return Response(
            { "result": result},
            status = status.HTTP_200_OK
        )
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    
    def patch(self, request, id):
        profile = get_object_or_404(User, pk=id)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 