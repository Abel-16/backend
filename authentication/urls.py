from django.urls import path
from .views import LoginAPIView, LoginAPIWithPhoneView, RegisterView, VerifyEmail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('loginWithPhone/', LoginAPIWithPhoneView.as_view(), name='login-with-phone'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    
]
