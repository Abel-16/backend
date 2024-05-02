from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, QuerySet
from .serializers import ExpanseSerializer
from .models import Expanse
from rest_framework import permissions
from .permissions import IsOwner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class ExpanseListAPIView(ListCreateAPIView):
    
    serializer_class = ExpanseSerializer
    queryset = Expanse.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'date': openapi.Schema(
                    type=openapi.TYPE_STRING, description="date Description"),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING, description="description Description"),
                'amount': openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="amount Description"),
                'category': openapi.Schema(
                    type=openapi.TYPE_STRING, description="category Description"),
            },
            required=['field1']
        )
    )
    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class ExpanseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpanseSerializer
    queryset = Expanse.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = "id"
    
    
    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)