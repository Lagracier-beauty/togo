from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer
from providers.models import Provider
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class OrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderUpdateSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        # Un utilisateur peut voir ses commandes, un provider les siennes
        if hasattr(user, 'provider_profile'):
            provider = user.provider_profile
            return Order.objects.filter(provider=provider)
        return Order.objects.filter(user=user)

class ProviderOrderListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'provider_profile'):
            provider = user.provider_profile
            return Order.objects.filter(provider=provider).order_by('-created_at')
        return Order.objects.none()
