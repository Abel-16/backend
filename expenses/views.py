from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, QuerySet
from .serializers import ExpanseSerializer
from .models import Expanse
from rest_framework import permissions
from .permissions import IsOwner

class ExpanseListAPIView(ListCreateAPIView):
    serializer_class = ExpanseSerializer
    queryset = Expanse,object.all()
    permission_classes = (permissions.IsAuthenticated)
    
    
    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class ExpanseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpanseSerializer
    queryset = Expanse,object.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"
    
    
    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)