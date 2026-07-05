from django.shortcuts import rende
from rest_framework.response import Response
from rest_framework import status
from .serializer import SignUpSerializer
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView


# Create your views here.

class SignUpView(APIView):
    
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(commit=False)
            
            
            user_data = serializer.validated_data
            user_data.pop('confrim_password',)  
            
            
            CustomUser.objects.create_user(user_data)
            
            
            
        return Response({
            'msg':'signup',
            'status': status.HTTP_201_CREATED,
            'data': serializer.data
        })