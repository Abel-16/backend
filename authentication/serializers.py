
from requests import Response
from rest_framework import serializers
from rest_framework import status
from authentication.utils import Util
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6)
    
    class Meta(BaseUserCreateSerializer.Meta):
        model=User
        fields = ['email', 'username', 'phone_number', 'user_type', 'password']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        username= attrs.get('username','')
        phone_number = attrs.get('phone_number','')
        
        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        if Util.validate_email(email) == False:
            raise serializers.ValidationError('The email should only contain alphanumeric characters')
        # if not phone_number.isPhoneNumber():
        #     raise serializers.ValidationError('The phone number should only contain alphanumeric characters')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    
    class Meta:
        model = User
        fields = ['token']
        
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length = 255, min_length=6, write_only=True)
    username = serializers.CharField(max_length = 255, min_length=6, read_only = True)
    user_type = serializers.CharField(max_length = 255, min_length=6, read_only = True)
    tokens = serializers.CharField(max_length = 255, min_length=6, read_only = True)
    
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username','user_type', 'tokens']
    
    def validate(self,attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        
        user=auth.authenticate(email=email, password=password)
        # import pdb
        # pdb.set_trace()
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
       
        
        return {
                'role': user.user_type,
                'username': user.username,
                'email': user.email,
                'tokens': user.tokens
                }
        
        return super().validate(attrs)
    
    
    # TODO: This must have to be fixed Leater

class LoginWithPhoneSerializer(serializers.ModelSerializer):
    phone_number=serializers.CharField(max_length=255, min_length=3)

    password = serializers.CharField(max_length = 255, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length = 255, min_length=6, read_only = True)
    
    
    class Meta:
        model = User
        fields = ['phone_number', 'password',  'tokens']
    
    def validate(self, data):
        phone_number = data.get('phone_number', None)
        password = data.get('password', None)

        # Perform any additional validation you need here
        if not phone_number:
            raise serializers.ValidationError("Phone number is required")
        if not password:
            raise serializers.ValidationError("Password is required")

        return data

    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
              fields = ['email']
    
    # def validate(self, attrs):
    #         import pdb
    #         pdb.set_trace()
    #         email = attrs['data'].get('email', '')
         
       
    #         return super().validate(attrs)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only = True)
    token = serializers.CharField(min_length=1,  write_only = True)
    uidb64 = serializers.CharField(min_length=1, write_only = True)
    
    class Meta:
        fields = ['password', 'token', 'uidb64']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password) 
            user.save()
            return(user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
    