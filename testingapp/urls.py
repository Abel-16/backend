from django.urls import path
from . import views


#url conf module
urlpatterns = [
    path('', views.hello),
    
]
