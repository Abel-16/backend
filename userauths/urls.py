from django.urls import path
from .views import MyTokenObtainPairView, RegisterView, ProfileView, PasswordResetEmailVerify, PasswordChangeView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/<email>', PasswordResetEmailVerify.as_view(), name='register'),
    path('password-change/', PasswordChangeView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # Add more paths for other views
]
