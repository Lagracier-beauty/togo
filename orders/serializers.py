from rest_framework import serializers
from .models import Order
from django.contrib.auth.models import User
from providers.models import Provider

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProviderShortSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    class Meta:
        model = Provider
        fields = ['id', 'user', 'service_type', 'rating']

class OrderSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    provider = ProviderShortSerializer(read_only=True)
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'provider', 'service_type', 'service_type_display', 'description',
            'status', 'status_display', 'price', 'address', 'scheduled_date', 'created_at', 'updated_at'
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['provider', 'service_type', 'description', 'price', 'address', 'scheduled_date']

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'description', 'price', 'address', 'scheduled_date'] 