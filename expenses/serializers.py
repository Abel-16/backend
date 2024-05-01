from rest_framework import serializers
from .models import Expanse

class ExpanseSerializer(serializers.Serializer):
    
    class Meta:
        model = Expanse
        fields = ['date',  'description', 'amount', 'category']
        