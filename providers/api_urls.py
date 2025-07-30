from django.urls import path
from . import api_views

urlpatterns = [
    path('register/', api_views.ProviderRegisterAPIView.as_view(), name='api_provider_register'),
    path('profile/', api_views.ProviderProfileAPIView.as_view(), name='api_provider_profile'),
    path('orders/', api_views.ProviderOrdersAPIView.as_view(), name='api_provider_orders'),
    path('list/', api_views.ProvidersListAPIView.as_view(), name='api_providers_list'),
] 