from django.contrib import admin
from . import models
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price']
    
@admin.register(models.Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured_product']