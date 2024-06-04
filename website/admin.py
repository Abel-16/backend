from django.contrib import admin
from website.models import Website, Support, Partners, SocialMedia

class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'phone']
    list_editable = ['email']
    


  
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Support)
admin.site.register(Partners)
admin.site.register(SocialMedia)