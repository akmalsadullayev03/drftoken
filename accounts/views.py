from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializer import CustomUserSerializer
from .models import CustomUser

class SignUpView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            
            user = serializer.save()
            
           
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "msg": "Muvaffaqiyatli ro'yxatdan o'tdingiz.",
                "status": status.HTTP_201_CREATED,
                "token": token.key,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"detail": "Username va parol kiritilishi shart."}, status=status.HTTP_400_BAD_REQUEST)
            
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "username": user.username
            }, status=status.HTTP_200_OK)
            
        return Response({"detail": "Username yoki parol noto'g'ri."}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Tizimdan muvaffaqiyatli chiqildi."}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            return Response({"detail": "Barcha parol maydonlari to'ldirilishi shart."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(old_password):
            return Response({"old_password": ["Eski parol noto'g'ri."]}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"confirm_password": ["Yangi parollar mos kelmadi."]}, status=status.HTTP_400_BAD_REQUEST)

        if old_password == new_password:
            return Response({"new_password": ["Yangi parol eskisi bilan bir xil bo'lmasligi kerak."]}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({"new_password": ["Parol kamida 8 ta belgidan iborat bo'lishi kerak."]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        user.auth_token.delete()
        
        return Response({"detail": "Parol o'zgartirildi. Qaytadan login qiling."}, status=status.HTTP_200_OK)