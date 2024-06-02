from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save
from farmer.models import Farmer
from userauths.models import User, Profile
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="category", default="category.jpg", null=True, blank=True)
    active = models.BooleanField(default= True)
    slug = models.SlugField(unique=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['title']

class Product(models.Model):
    STATUS = {
        ("draft", "Drafted"),
        ("disabled", "Disabled"),
        ("in_review", "In review"),
        ("published", "Published"),
       
    }
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="category", default="category.jpg", null=True, blank=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    old_price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    shipping_amount = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    
    stock_qty = models.PositiveIntegerField(default=1)
    in_stock = models.BooleanField(default=True)
    
    status = models.CharField(max_length=100, choices=STATUS, default="published")
    
    featured  = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    pid = ShortUUIDField(unique=True, length = 10, prefix = "ASP")
    slug = models.SlugField(unique=True)
    date = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.slug == "" or  self.slug == None:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
            
    
    def __str__(self) -> str:
        return self.title
    
    # def product_rating(self):
    #     product_rating = Review.objects.filter(product=self).aaggregate(avg_rating=models.Avg("rating"))
    #     return product_rating['avg_rating']
    
    def rating_count(self):
        rating_count = Review.objects.filter(product=self).count()
        return rating_count
    
    def gallery(self):
        return Gallery.objects.filter(product=self)
    
    def save(self, *args, **kwargs):
        # self.rating = self.product_rating()
        super(Product, self).save(*args, **kwargs)

class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to="products", default="category.jpg")
    active = models.BooleanField(default=True)
    gid = ShortUUIDField(unique=True, length=10)
    
    def __str__(self):
        return self.product.title
    
    class Meta:
        verbose_name_plural = "Product Images"
    
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default = 0)
    price = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    sub_total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    service_free = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    country = models.CharField(max_length=100, null = True, blank=True)
    cart_id = models.CharField(max_length=100, null = True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.cart_id} - {self.product.title}"
    

class CartOrder(models.Model):
    PAYMENT_STATUS = {
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("Cancelled", "Cancelled"),  
    }
    ORDER_STATUS = {
        ("pending", "Pending"),
        ("fulfilled", "Fulfilled"),
        ("Cancelled", "Cancelled"),  
    }
    farmer = models.ManyToManyField(Farmer, blank=True)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sub_total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    service_free = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=100, default="processing")
    order_status = models.CharField(choices=ORDER_STATUS, max_length=100, default="pending")
    
    
    # Coupons
    initial_total = models.DecimalField(default=0.09, max_digits = 12, decimal_places = 2)
    saved = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    
    #person data
    full_name = models.CharField(max_length=100, null= True, blank=True)
    email = models.CharField(max_length=100, null= True, blank=True)
    mobile = models.CharField(max_length=100, null= True, blank=True)
   
   # shiping Address
    address = models.CharField(max_length=100, null= True, blank=True)
    city = models.CharField(max_length=100, null= True, blank=True)
    state = models.CharField(max_length=100, null= True, blank=True)
    country = models.CharField(max_length=100, null= True, blank=True)
    
    oid = ShortUUIDField(unique=True, length = 10, prefix = "ASP-Order")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.oid
    

class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    qty = models.PositiveIntegerField(default = 0)
    price = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    sub_total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    service_free = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    country = models.CharField(max_length=100, null = True, blank=True)
    
    initial_total = models.DecimalField(default=0.00, max_digits = 12, decimal_places = 2)
    saved = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    oid = ShortUUIDField(unique=True, length = 10, prefix = "ASP-Order")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.oid
    
class ProductFaq(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True,  blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField(null = True, blank=True)
    question = models.CharField(max_length=10000)
    answer = models.TextField(null=True, blank=True)
    active = models.BooleanField(default = False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.question

    class Meta:
        verbose_name_plural = "Product FAQs"

class Review(models.Model):
    RATING = {
        ("1", "1 Star"),
        ("2", "2 Star"),
        ("3", "3 Star"),
        ("4", "4 Star"),
        ("5", "5 Star"),
    }
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    replay = models.TextField(null = True, blank=True)
    rating = models.IntegerField(default=None, choices=RATING )
    
    def __str__(self) -> str:
        return self.RATING

    class Meta:
        verbose_name_plural = "Reviews & Rating"
        
    def profile(self):
        return Profile.objects.get(user = self.user)
    
@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    if instance.product:
        instance.product.save()
        
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.product.title

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, null = True, blank=True)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.SET_NULL,  null = True, blank=True)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       if self.order:
           return self.order.oid
       else:
           return f"Notification - {self.pk}"

class Coupon(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    user_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=1000)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.code

class Tax(models.Model):
    country = models.CharField(max_length=40)
    rate = models.IntegerField(default=5, help_text="Numbers added here are in percentage e.g 5%")
    active = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.country
    
    class Meta:
        verbose_name_plural = "Taxes"
    