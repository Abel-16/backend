from django.urls import path, include

from userauths import views as userauths_views


urlpatterns = [
    path('auth/', include('userauths.urls')),
    path('store/', include('store.urls')),
    path('web/', include('website.urls')),
]
