from django.contrib import admin
from django.urls import path, include
from store import views as store_views

urlpatterns = [
    path('category/', store_views.CategoryListAPIView.as_view()),
    path('products/', store_views.ProductListAPIView.as_view()),
    path('products/<int:pk>/', store_views.ProductDetailListAPIView.as_view()),

]