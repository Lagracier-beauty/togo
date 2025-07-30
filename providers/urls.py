from django.urls import path
from . import views

app_name = 'providers'

urlpatterns = [
    path('register/', views.provider_register, name='provider_register'),
    path('dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('profile/', views.provider_profile, name='provider_profile'),
    path('orders/', views.provider_orders, name='provider_orders'),
    path('list/', views.providers_list, name='providers'),
] 