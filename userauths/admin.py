from django.contrib import admin
from userauths.models import Profile, User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['gender']
 

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)