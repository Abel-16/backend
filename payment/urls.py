from django.urls import path
from . import views

urlpatterns = [
    path('payment/', views.PaymentAPIView.as_view(), name='initiate_payment'),
    # path('callback/', views.payment_callback, name='payment_callback'),
]
