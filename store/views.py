from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from store.models import Cart, CartOrder, CartOrderItem, Product, Category, Tax
from store.serializers import CartOrderSerializer, ProductSerializer, CategorySerializer,CartSerializer
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
    


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    queryset = Cart.objects.all()

    def get_queryset(self):
        cart_id = self.kwargs.get('cart_id')
        user_id = self.kwargs.get('user_id')

        if user_id is not None:
            user = User.objects.filter(id=user_id).first()
            if user:
                queryset = Cart.objects.filter(user=user, cart_id=cart_id)
            else:
                queryset = Cart.objects.none()  # No user found, return empty queryset
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    lookup_field = "cart_id"
    queryset = Cart.objects.all()
    
    def get_queryset(self):
        cart_id = self.kwargs.get('cart_id')
        user_id = self.kwargs.get('user_id')

        if user_id is not None:
            user = User.objects.filter(id=user_id).first()
            if user:
                queryset = Cart.objects.filter(user=user, cart_id=cart_id)
            else:
                queryset = Cart.objects.none()  # No user found, return empty queryset
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        total_shipping = 0.0
        total_tax = 0.0
        total_service_fee = 0.0
        total_sub_total = 0.0
        total_total = 0.0
        
        for cart_item in queryset:
            total_shipping += float(self.calculate_shipping(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_service_fee += float(self.calculate_service_fee(cart_item))
            total_sub_total += float(self.calculate_sub_total(cart_item))
            total_total += float(self.calculate_total(cart_item))
            
        data = {
            'shipping' : total_shipping,
            'total_tax' : total_tax,
            'total_service_fee' : total_service_fee,
            'total_sub_total' : total_sub_total,
            'total_total' : total_total,
          
        }
        
        return Response(data)
    def calculate_shipping(self, cart_item):
        return cart_item.shipping_amount
    
    def calculate_tax(self, cart_item):
        return cart_item.tax_fee
    
    
    def calculate_service_fee(self, cart_item):
        return cart_item.service_fee
    
    
    def calculate_sub_total(self, cart_item):
        return cart_item.sub_total
    
    def calculate_total(self, cart_item):
        return cart_item.total
    
class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    lookup_field = 'cart_id'
    
    def get_object(self):
        cart_id = self.kwargs['cart_id']
        item_id = self.kwargs['item_id']
        user_id = self.kwargs.get('user_id')
        
        if user_id:
            
            user = get_object_or_404(User,id=user_id)
            cart = get_object_or_404(Cart, id=item_id, cart_id=cart_id, user=user)
        else:
            cart = Cart.objects.get(id=item_id, cart_id = cart_id)
        
        return cart   


class SearchProductApiView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        query = self.request.GET.get("query")
        product = Product.objects.filter(status="Published", title__icontains=query)
        return product


class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = CartOrderSerializer
    queryset = CartOrder.objects.all()
    permission_classes = [AllowAny]
    
    def create(self, request):
        payload = request.data
        
        full_name = payload["full_name"]
        email = payload["email"]
        mobile = payload["mobile"]
        address = payload["address"]
        city = payload["city"]
        state = payload["state"]
        country = payload["country"]
        cart_id = payload["cart_id"]
        user_id = payload["user_id"]
        
        try:
            user = User.objects.get(id = user_id)
        except:
            user = None
            
   
        
        cart_items = Cart.objects.filter(cart_id = cart_id)
        
        total_shipping = Decimal(0.00)
        total_tax = Decimal(0.00)
        total_service_fee = Decimal(0.00)
        total_sub_total = Decimal(0.00)
        total_initial_total = Decimal(0.00)
        total_total = Decimal(0.00)
        
        order = CartOrder.objects.create(
            full_name = full_name,
            email=email,
            mobile = mobile,
            address = address,
            city = city,
            state = state,
            country = country
        )

        for c in cart_items:
            CartOrderItem.objects.create(
                order=order,
                product=c.product,
                farmer=c.farmer,
                size=c.size,
                price=c.price,
                sub_total=c.sub_total,
                shipping_amount=c.shipping_amount,
                service_fee=c.service_fee,
                tax_fee=c.tax_fee,
                initial_total = c.total_initial_total,
                total=c.total
            )
            
            total_shipping  += Decimal(c.shipping_amount)
            total_tax  += Decimal(c.total_tax)
            total_service_fee  += Decimal(c.total_service_fee)
            total_sub_total  += Decimal(c.total_sub_total)
            total_initial_total += Decimal(c.total)
            total_total += Decimal(c.total)
            
            order.farmer.add(c.product.farmer)
        
        order.sub_total = total_sub_total
        order.shipping_amount = total_shipping
        order.tax_fee = total_tax
        order.service_fee = total_service_fee
        order.initial_total = total_initial_total
        order.total = total_total
        
        order.save()
        
        return Response({"message": "Order Created Successfully", "Order_oid": order.oid}, status=status.HTTP_201_CREATED)
       
        
        
        
            
    