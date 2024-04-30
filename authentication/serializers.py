
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

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6)
    
    
    class Meta(BaseUserCreateSerializer.Meta):
        model=User
        fields = ['email', 'username', 'phone_number', 'password']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        username= attrs.get('username','')
        phone_number = attrs.get('phone_number','')
        
        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        if Util.validate_email(email) == False:
            raise serializers.ValidationError('The email should only contain alphanumeric characters')
        if not phone_number.isPhoneNumber():
            raise serializers.ValidationError('The phone number should only contain alphanumeric characters')
        return attrs
    
    def create(self, validated_data):

        User.objects.create_user(**validated_data)
        return Response(status=status.HTTP_201_CREATED, data={'success':'User created successfully Please verify your email'})

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    
    class Meta:
        model = User
        fields = ['token']
        
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length = 255, min_length=6, write_only=True)
    username = serializers.CharField(max_length = 255, min_length=6, read_only = True)
    tokens = serializers.CharField(max_length = 255, min_length=6, read_only = True)
    
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']
    
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
                'email': user.email,
                'username': user.username,
                'tokens': user.tokens
                }
        
        return super().validate(attrs)
    
    
    # TODO: This must have to be fixed Leater

class LoginWithPhoneSerializer(serializers.ModelSerializer):
    phone_number=serializers.CharField(max_length=255, min_length=3)

    password = serializers.CharField(max_length = 255, min_length=6, write_only=True)
   
    
    
    class Meta:
        model = User
        fields = ['phone_number', 'password',  'tokens']
    
    def validate(self,attrs):
        phone = attrs.get('phone_number', '')
        password = attrs.get('password', '')
        
        print(phone + " " + password)
        user=auth.authenticate(phone_number=phone, password=password)
        
        # user= User.objects.filter(phone_number = phone).exists()
        user = User.objects.get("email")

        print(user)
        # import pdb
        # pdb.set_trace()
        # if not user:
        #     raise AuthenticationFailed('Invalid credentials, try again')
        
        # if not user.is_active:
        #     raise AuthenticationFailed('Account disabled, contact admin')
        
        # if not user.is_verified:
        #     raise AuthenticationFailed('Email is not verified')
        
       
        
        return {
                'email': user.email,
                'username': user.username,
                'tokens': user.tokens
                }
        
        return super().validate(attrs)
    
        