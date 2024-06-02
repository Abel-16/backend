from django.shortcuts import render
from store.models import Cart, Product, Category
from store.serializers import ProductSerializer, CategorySerializer,CartSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from userauths.models import User

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
class ProductDetailListAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    
    permission_classes = [AllowAny]

class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        payload = request.data
        
        product_id = payload['product_id']
        user_id = payload['user_id']
        qty = payload['qty']
        price = payload['price']
        shipping_amount = payload['shipping_amount']
        country = payload['country']
        cart_id = payload['cart_id']
        
        product = Product.objects.get(id=product_id)
        
        if user_id != "undefined":
            user = User.objects.get(id = user_id)
        else:
            user = None
        
        
    

