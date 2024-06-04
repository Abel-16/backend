from rest_framework import viewsets
from .models import Website, SocialMedia, Support, Partners
from .serializers import WebsiteSerializer, SocialMediaSerializer, SupportSerializer, PartnersSerializer
from rest_framework import generics

class SupportViewSet(generics.ListAPIView):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer

class SocialMediaViewSet(generics.ListAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer

class WebsiteViewSet(generics.ListAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer

class PartnersViewSet(generics.ListAPIView):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializer
