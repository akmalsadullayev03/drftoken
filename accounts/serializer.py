import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser

# ================= VALIDATORS =================

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


# ================= SERIALIZER =================

class CustomUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(validators=[validate_letters_only], max_length=50, required=True)
    last_name = serializers.CharField(validators=[validate_letters_only], max_length=50, required=True)
    phone_number = serializers.CharField(validators=[validate_uzb_phone], required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
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
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Bu username allaqachon band.")
            
        if username.isdigit():
            raise ValidationError("Username faqat raqamlardan iborat bo'lishi mumkin emas.")
            
        if len(username) < 5:
            raise ValidationError("Username kamida 5 ta belgidan iborat bo'lishi kerak.")    
            
        if username[0].isdigit():
            raise ValidationError("Username raqam bilan boshlanishi mumkin emas.")
            
        if not re.match(r'^\w+$', username):
            raise ValidationError("Username faqat harf, raqam va pastki chiziq (_) dan iborat bo'lishi kerak.")
            
        return username

    def validate_email(self, value):
        email = value.lower().strip()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Bu email manzili allaqachon ro'yxatdan o'tgan.")
            
        forbidden_domains = ['mailinator.com', 'trashmail.com', 'tempmail.com']
        domain = email.split('@')[-1]
        if domain in forbidden_domains:
            raise ValidationError("Vaqtinchalik pochtalardan foydalanish taqiqlangan.")
            
        return email
        
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
       
        if password != confirm_password:
            raise ValidationError({"confirm_password": "Kiritilgan parollar bir-biriga mos kelmadi."})  
            
   
        if first_name.lower() == last_name.lower():
            raise ValidationError({"last_name": "Ism va familiya bir xil bo'lishi mumkin emas."})
            
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        photo = validated_data.pop('photo', None)
        
        user = CustomUser.objects.create_user(**validated_data)
        
        if photo:
            user.photo = photo
            user.save()
            
        return user