from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FoodPost
from .serializer import FoodPostSerializer, FoodImageSerializer


# Create your views here.
def hello(request):
    return HttpResponse("hello")

class FoodPostView(APIView):
    serializer_class = FoodPostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)