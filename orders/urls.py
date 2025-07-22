from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # API endpoints
    path('api/orders/', views.OrderListCreateAPIView.as_view(), name='api_order_list_create'),
    path('api/orders/<int:pk>/', views.OrderDetailAPIView.as_view(), name='api_order_detail'),
    path('api/provider/orders/', views.ProviderOrderListAPIView.as_view(), name='api_provider_orders'),
] 