from django.db import models
from django.utils.text import slugify
from userauths.models import User

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    image = models.FileField(upload_to="farmer", blank=True, null = True, default="farmer.jpg")
    name = models.CharField(max_length=100,help_text="Farmer Shop Name", blank=True, null=True)
    description = models.TextField(null = True, blank=True)
    mobile = models.CharField(max_length=20,help_text="Farmer Shop Mobile Number", blank=True, null=True)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=500)
    
    
    class Meta:
        verbose_name_plural = "Farmers"
        ordering = ['-date']
        
    def __str__(self) -> str:
        return str(self.name)
    
    def save(self, *args,**kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.name)
        
        super(Farmer, self).save()