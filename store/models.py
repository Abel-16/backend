from django.db import models

from userauths.models import User, Profile


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
        