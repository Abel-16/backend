from django.db import models
from django .contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.validators import RegexValidator

from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    
    def create_user(self, username, email, phone_number, user_type, password=None):
        
        if username is None:
            raise TypeError("Users should have a Username")
        
        if email is None:
            raise TypeError("Users should have an Email")
        
        if phone_number is None:
            raise TypeError("Users should have an Phone Number")
        
        user = self.model(username=username, email=self.normalize_email(email), user_type = user_type, phone_number = phone_number)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, phone_number, password):
        
        if password is None:
            raise TypeError("Password should not be none")
        
     
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('agent', 'Agent'),
        ('farmer', 'Farmer'),
    )
    
    username = models.CharField(max_length = 255, unique = True, db_index = True)
    email = models.EmailField(max_length=254, unique= True, db_index = True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    is_verified = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username', 'user_type']
    
    objects = UserManager()
    
    def __str__(self) -> str:
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
       