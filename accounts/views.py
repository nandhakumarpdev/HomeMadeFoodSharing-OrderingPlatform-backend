from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import User

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


        
