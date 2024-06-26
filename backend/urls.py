from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from .swagger import schema_view
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # path('auth/', include('djoser.urls')),
    path('api/admin/', admin.site.urls),
path('api/chapa-webhook', include('django_chapa.urls')),
     path('api/payment/', include('payment.urls')),
    # path('api/auth/', include('authentication.urls')),
    # path('api/expanses/', include('expenses.urls')),
    path('api/v1/', include('api.urls')),
    # path('api/store/', include('store.urls')),
    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.MEDIA_ROOT)
