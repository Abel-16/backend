from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExpanseListAPIView.as_view(), name="expenses"),
    path('<int:id>', views.ExpanseDetailAPIView.as_view(), name="expense"),
]
