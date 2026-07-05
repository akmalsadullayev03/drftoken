import re
from rest_framework import serializers, status
from .models import CustomUser
from rest_framework.exceptions import ValidationError

def validate_letters_only(value):
    if not re.match(r"^[A-Za-z'‘`’ ]+$", value):
        raise ValidationError("Bu maydonda faqat harflar va bo'shliqlar bo'lishi mumkin.")
    if len(value) < 2:
        raise ValidationError("Uzunlik kamida 2 ta belgidan iborat bo'lishi kerak.")
    return value

def validate_uzb_phone(value):
    cleaned_phone = re.sub(r'[\s\-()]+', '', value)
    phone_regex = r'^\+998\d{9}$'
    if not re.match(phone_regex, cleaned_phone):
        raise ValidationError("Telefon raqami noto'g'ri formatda. Namuna: +998901234567")
    return cleaned_phone

class CustomUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(validators=[validate_letters_only], max_length=50, required=True)
    last_name = serializers.CharField(validators=[validate_letters_only], max_length=50, required=True)
    phone_number = serializers.CharField(validators=[validate_uzb_phone], required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

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
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True}
        }
        
    def validate_username(self, username):
        user = CustomUser.objects.filter(username=username).first()
        if user:
            raise ValidationError({
                'msg': 'Bu username band',
                'status': status.HTTP_400_BAD_REQUEST
            })
            
        if username.isdigit():
            raise ValidationError({
                'msg': 'Username raqamlardan iborat bolmasligi kerak',
                'status': status.HTTP_400_BAD_REQUEST
            })
            
        if len(username) < 5:
            raise ValidationError({
                'msg': 'Username 5 ta harf va belgidan kam bolmasligi kerak',    
                'status': status.HTTP_400_BAD_REQUEST
            })  
            
        if username[0].isdigit():
            raise ValidationError({
                'msg': 'Username raqam bn bowlanmasin',
                'status': status.HTTP_400_BAD_REQUEST
            })
            
        if not re.match(r'^\w+$', username):
            raise ValidationError({
                'msg': 'Username faqat harf,raqam va _ bolishi kerak',
                'status': status.HTTP_400_BAD_REQUEST
            })
            
        return username

    def validate_email(self, value):
        email = value.lower().strip()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError({
                'msg': 'Bu email manzili allaqachon ro\'yxatdan o\'tgan.',
                'status': status.HTTP_400_BAD_REQUEST
            })
            
        forbidden_domains = ['mailinator.com', 'trashmail.com', 'tempmail.com']
        domain = email.split('@')[-1]
        if domain in forbidden_domains:
            raise ValidationError({
                'msg': 'Vaqtinchalik pochtalardan foydalanish taqiqlangan.',
                'status': status.HTTP_400_BAD_REQUEST
            })
            
        return email
        
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        if (password and confirm_password) and password != confirm_password:
            raise ValidationError({
                 'msg': 'Parolar mavjud emas',
                 'status': status.HTTP_400_BAD_REQUEST
            })  
            
        if first_name.lower() == last_name.lower():
            raise ValidationError({
                'msg': 'Ism va familiya bir xil bo\'lishi mumkin emas.',
                'status': status.HTTP_400_BAD_REQUEST
            })
            
        return data