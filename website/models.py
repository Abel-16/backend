from django.db import models
from django.utils.text import slugify
from userauths.models import User

class Support(models.Model):
    address = models.CharField(max_length=100, help_text="Support Address", blank=True, null=True)
    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100, help_text="Support Phone", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact_email


class Website(models.Model):
    title = models.CharField(max_length=20, help_text="Website title", blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, help_text="Website phone", blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    main_logo = models.FileField(upload_to="website", blank=True, null=True, default="website_logo.jpg")
    icon_logo = models.FileField(upload_to="website", blank=True, null=True, default="website_logo.jpg")
    support = models.ForeignKey(Support, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.title)


class SocialMedia(models.Model):
    name = models.CharField(max_length=100, help_text="Social Media Name", blank=True, null=True)
    link = models.CharField(max_length=100, help_text="Social Media linkpy", blank=True, null=True)
    logo = models.FileField(upload_to="socialmedia", blank=True, null=True, default="socialmedia.jpg")
    date = models.DateTimeField(auto_now_add=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='social_medias')

    def __str__(self):
        return self.name


class Partners(models.Model):
    name = models.CharField(max_length=100, help_text="Partners Name", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to="partners", blank=True, null=True, default="partners.jpg")

    def __str__(self):
        return self.name