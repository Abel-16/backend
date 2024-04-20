from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from .swagger import schema_view


urlpatterns = [
    # path('auth/', include('djoser.urls')),
    path('api/admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]