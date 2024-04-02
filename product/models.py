from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now = True)
    created_date = models.DateTimeField(auto_now = True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name = 'category')
     
    def __str__(self) -> str:
        return self.title
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True, related_name = '+')
    
    def __str__(self) -> str:
        return self.title