from django.shortcuts import get_object_or_404, render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from userauths.models import User, Profile
from userauths.selializer import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer, UserPasswordResetSerializer, UserSerializer
from rest_framework import generics, permissions
import shortuuid
from rest_framework import status
from .models import Profile
from rest_framework.response import Response
import random

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        # Retrieve the profile of the currently authenticated user
        return Profile.objects.get(user=self.request.user)

def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

class PasswordResetEmailVerify(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserPasswordResetSerializer
    
    def get_object(self):
        email = self.kwargs['email']
        user = get_object_or_404(User,email=email)
        print("user *************", user)
         
        if user:
            user.otp = generate_otp()
            user.save()  # Save the OTP to the user object
            uid64 = user.pk
            otp = user.otp
            
            link = f"http://localhost:5173/create-new-password?otp={otp}&uidb64={uid64}"
            print("Link ============", link)
            print("otp ============", otp)
            print("uid64 ============", uid64)
            # send email
        return {user, link, otp, uid64}
  
   
class PasswordChangeView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    
    def create(self, request):
        payload = request.data
        
        otp = payload['otp']
        uidb64 = payload['uidb64']
        password = payload['password']
        
        user = User.objects.get(otp=otp, id = uidb64)
        if user:
            user.set_password(password)
            user.otp = ""
            user.save()
            return Response({"message":"Password Changed Successfully"}, status=status.HTTP_201_created)
        else:
            return Response({"message": "User Does Not Exists"}, status= status.HTTP_404_NOT_FOUND)
