from django.urls import path
from .views import LoginAPIView, LoginAPIWithPhoneView, PasswordTokenCheckAPI, RegisterView, SetNewPasswordAPIView, VerifyEmail,RequestPasswordResetEmail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('loginWithPhone/', LoginAPIWithPhoneView.as_view(), name='login-with-phone'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-email', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-rest-complete', SetNewPasswordAPIView.as_view(), name = 'password-reset-complete')
    
]
