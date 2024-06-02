from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from userauths.models import User, Profile
from userauths.selializer import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer
from rest_framework import generics, permissions

from .models import Profile


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