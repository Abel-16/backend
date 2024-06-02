from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField

class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100,unique=True, null= True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self) -> str:
        return self.email
    
    def save(self, *args, **kwargs):
        email_username, mobile = self.email.split("@")
        # if self.full_name == "" or self.full_name == None:
        #     self.full_name = email_username
        if self.username == "" or self.username == None:
            self.username = email_username
        
        super(User, self).save(*args, **kwargs)

class UserAddress(models.Model):
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    house_number = models.CharField(max_length=100, null=True, blank=True)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="image", default="default/default-user.jpg", null=True, blank=True)
    
    about = models.CharField(max_length=250,null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    address = models.OneToOneField(UserAddress,  null=True,on_delete=models.PROTECT) 
    date = models.DateField(auto_now_add=True)
    pid = ShortUUIDField(unique= True, length = 10, max_length = 20, alphabet="abcdefghijk")
    
    def __str__(self) -> str:
        return str(self.user)
    def save(self, *args, **kwargs):
      
        super(Profile, self).save(*args, **kwargs)    

def create_user_profile(sender, instance, created ,**kwargs):
    if created:
        Profile.objects.create(user = instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)