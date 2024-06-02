from rest_framework import serializers

from farmer.models import Farmer
from .models import Gallery, Product,Category,CartOrder,CartOrderItem,Cart,Coupon,Notification,ProductFaq, Review,Wishlist

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"

class GallerySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Gallery
        fields = "__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True, read_only = True)
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "image",
            "category",
            "price",
            "old_price",
            "shipping_amount",
            "stock_qty",
            "in_stock",
            "status",
            "featured",
            "views",
            "rating",
            # "product_rating",
            "rating_count",
            "gallery",
            "farmer",
            "pid",
            "slug",
            "date",
            ]
    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(CartSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class CartOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartOrderItem
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(CartOrderSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
class ProductFaqSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductFaq
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(ProductFaqSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
class FarmerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Farmer
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(FarmerSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(ReviewSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
class WishlistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wishlist
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(WishlistSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(NotificationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
class CouponSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coupon
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(CouponSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3