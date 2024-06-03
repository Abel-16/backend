from django.contrib import admin
from django.urls import path, include
from store import views as store_views

urlpatterns = [
    path('category/', store_views.CategoryListAPIView.as_view()),
    path('products/', store_views.ProductListAPIView.as_view()),
    path('products/<int:pk>/', store_views.ProductDetailListAPIView.as_view()),
    path('cart-view', store_views.CartAPIView.as_view()),
    path('cart-list/<str:cart_id>/<int:user_id>/', store_views.CartListView.as_view()),

]