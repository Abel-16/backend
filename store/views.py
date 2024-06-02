from decimal import Decimal
from django.shortcuts import render
from store.models import Cart, Product, Category, Tax
from store.serializers import ProductSerializer, CategorySerializer,CartSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from userauths.models import User
from rest_framework import status
\
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
        
        tax = Tax.objects.filter(country=country).first()
        if tax:
            tax_rate = tax.rate / 100
        else:
            tax_rate = 0
        
        cart = Cart.objects.filter(cart_id=cart_id, product=product).first()
        
        if cart:
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * Decimal(qty)
            cart.shipping_amount = Decimal(shipping_amount) * Decimal(qty)
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            
            service_fee_percentage = 20/100
            cart.service_free = service_fee_percentage * cart.sub_total
            
            cart.total = cart.sub_total + cart.shipping_amount + cart_id.service_fee + cart.tax_fee
            cart.save()
        
            return Response({'message': "Cart Updated Successfully"}, status=status.HTTP_200_CREATED)
        
        else:
            cart = Cart()
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * Decimal(qty)
            cart.shipping_amount = Decimal(shipping_amount) * Decimal(qty)
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            
            service_fee_percentage = 20/100
            cart.service_free = service_fee_percentage * cart.sub_total
            
            cart.total = cart.sub_total + cart.shipping_amount + cart_id.service_fee + cart.tax_fee
            cart.save()
        
            return Response({'message': "Cart Created Successfully"}, status=status.HTTP_202_CREATED)
    

