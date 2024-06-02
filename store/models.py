from django.db import models


from farmer.models import Farmer
from userauths.models import User, Profile
from shortuuid.django_fields import ShortUUIDField

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="category", defaults="category.jpg", null=True, blank=True)
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
    image = models.FileField(upload_to="category", defaults="category.jpg", null=True, blank=True)
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
    farmer = models.ForeignKey(Farmer, models=models.CASCADE)
    pid = ShortUUIDField(unique=True, length = 10, prefix = "ASP")
    slug = models.SlugField(unique=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
    
