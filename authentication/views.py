from django.shortcuts import render
from rest_framework import generics, status, views
from .serializers import EmailVerificationSerializer, LoginSerializer, LoginWithPhoneSerializer, RegisterSerializer, ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate, login
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

class RegisterView(generics.GenericAPIView):
    
    
    serializer_class=RegisterSerializer
    
    """
    Custom Endpoint Description
    """
    @swagger_auto_schema(
        operation_description="Endpoint Operation Description",
        responses={
            200: "Success",
            400: "Bad Request",
            401: "Unauthorized",
        },
        # request_body=openapi.Schema(
        #     type=openapi.TYPE_OBJECT,
        #     properties={
        #         'field1': openapi.Schema(
        #             type=openapi.TYPE_STRING, description="Field 1 Description"),
        #         'field2': openapi.Schema(
        #             type=openapi.TYPE_STRING, description="Field 2 Description"),
        #     },
        #     required=['field1']
        # )
    )
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        
        user = User.objects.get(email=user_data['email'])
        
        token = RefreshToken.for_user(user).access_token
        
        current_site = get_current_site(request).domain
        
        relativeLink = reverse('email-verify')
        
        absurl = 'http://' + current_site + relativeLink + '?token='+ str(token)
        email_body = 'Hi '+ user.username + ' Use the link below to verify your email \n' + absurl
        
        data={
            'email_body': email_body,
            'to_email': user.email, 
            'email_subject': 'Verify your email'
            }
        Util.send_email(data)
        
        return Response(data="Account created successfully please verify your email", status=status.HTTP_201_CREATED)
    


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description="Description", type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token') 
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,  algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            print(user)
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    
    serializer_class = LoginSerializer
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class LoginAPIWithPhoneView(generics.GenericAPIView):
    
    serializer_class = LoginWithPhoneSerializer
    
    def post(self, request):
        serializer = LoginWithPhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid phone number or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # serializer.is_valid(raise_exception = True)
        # phone_number = serializer.validated_data['phone_number']
        # password = serializer.validated_data['password']
        # print("hellooooooooooooo")
        # user = authenticate(request, phone_number=phone_number, password=password)
        # import pdb
        # pdb.set_trace()
        # print(user)
        # # serializer = self.serializer_class(data=request.data)
        # # serializer.is_valid(raise_exception = True)
        
        # return Response(serializer.data, status=status.HTTP_200_OK)
   
class RequestPasswordResetEmail(generics.GenericAPIView):
    
    serializer_class = ResetPasswordEmailRequestSerializer
    
    def post(self, request):
        data = {'request': request, 'data' : request.data}
        serializer = self.serializer_class(data=data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
             user = User.objects.get(email=email)
            #  import pdb
            #  pdb.set_trace()
             uid64 = urlsafe_base64_encode(smart_bytes(user.id))
             token = PasswordResetTokenGenerator().make_token(user)
             current_site = get_current_site(request=request).domain
             relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uid64, 'token':token})
             absurl = 'http://' + current_site + relativeLink 
             email_body = 'Hello, Use the link below to reset your password \n' + absurl
             data={
                 'email_body': email_body,
                 'to_email': user.email, 
                 'email_subject': 'Reset your password'
                 }
             Util.send_email(data)
           
        return Response({'success': 'We have send you a link to reset your password'}, status=status.HTTP_200_OK)
class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not  PasswordResetTokenGenerator().check_token(user, token ):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'success': True, 'message': 'Creddentials Valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

            
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'})
    

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception = True)
        return Response({'success': True, 'message': 'Password reset Success'}, status=status.HTTP_200_OK)
        