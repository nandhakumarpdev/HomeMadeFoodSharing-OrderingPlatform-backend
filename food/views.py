from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FoodPost, FoodImage
from .serializer import FoodPostSerializer, FoodImageSerializer



class AllFoodPostView(APIView):
    serializer_class = FoodPostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        foods = FoodPost.objects.all()
        serializer = self.serializer_class(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FoodPostView(APIView):
    serializer_class = FoodPostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        foods = FoodPost.objects.filter(user=request.user)
        serializer = self.serializer_class(foods, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FoodById(APIView):
    serializer_class = FoodPostSerializer
    permission_classes = [IsAuthenticated]    

    def get(self, request, id):
        food = FoodPost.objects.get(pk=id)
        serializer = self.serializer_class(food)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        food = get_object_or_404(FoodPost, pk=id)
        serializer = self.serializer_class(food, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodImageView(APIView):
    serializer_class = FoodImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FoodImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodShowCaseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                select 
                u.first_name, 
                u.phone_number, 
                fn.food_name, 
                fn.price, 
                fn.status,
                fi.image from food_foodpost fn 
                inner join food_foodimage fi
                on fn.id = fi.food_post_id
                inner join accounts_user u 
                on fn.user_id = u.id;

            """)

            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        rows = [dict(zip(columns, row)) for row in rows]

        return Response(rows, status=status.HTTP_200_OK)