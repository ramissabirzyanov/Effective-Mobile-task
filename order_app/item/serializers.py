from rest_framework import serializers
from .models import Item


class ItemSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = '__all__'
