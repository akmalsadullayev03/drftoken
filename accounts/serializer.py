from rest_framework import serializers,status
from .models import CustomUser
from rest_framework.exceptions import ValidationError




class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'photo',
            'password',
            'confirm_password',
        ]
        
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if (password and confirm_password) and password != confirm_password:
            raise ValidationError({
                 'msg':'Parolar mavjud emas',
                 'status':status.HTTP_400_BAD_REQUEST
            })  
            
    def validate(self,username):
        
        
        user = CustomUser.objects.filter(username=username).first()
        if user:
            raise ValidationError({
                'msg':'Bu username band',
                'status':status.HTTP_400_BAD_REQUEST
            })
            
            
        if username.isdigit():
            raise ValidationError({
                'msg':'Username raqamlardan iborat bolmasligi kerak',
                'status':status.HTTP_400_BAD_REQUEST
            })
            
        if len(username) < 5 :
            raise ValidationError({
                'msg':'Username 5 ta harf va belgidan kam bolmasligi kerak',    
                'status':status.HTTP_400_BAD_REQUEST
            })  
            
            
        if  not username.isintance(username[0],str):
            raise ValidationError({
                'msg':'Username raqam bn bowlanmasin',
                'status':status.HTTP_400_BAD_REQUEST
            })
            
            
        if len ([i for i in username if i.isdigit()]) == 0:
            raise ValidationError({
                'msg':'Username faqat harf,raqam va _ bolishi kerak',
                'status':status.HTTP_400_BAD_REQUEST
            })
            
            
            