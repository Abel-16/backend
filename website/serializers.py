from rest_framework import serializers
from .models import Website, SocialMedia, Support, Partners

class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = '__all__'

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'

class WebsiteSerializer(serializers.ModelSerializer):
    social_medias = SocialMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Website
        fields = '__all__'

class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = '__all__'
