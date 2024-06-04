from django.urls import path
from website import views as website

urlpatterns = [
    path('website-information/', website.WebsiteViewSet.as_view(), name='website-information'),
    path('support-information/', website.SupportViewSet.as_view(), name='support-information'),
    path('partners-information/', website.PartnersViewSet.as_view(), name='support-information'),
    path('social-media/', website.SocialMediaViewSet.as_view(), name='support-information'),
   
  
]
