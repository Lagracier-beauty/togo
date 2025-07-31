from django.urls import path
from . import views

app_name = 'providers'

urlpatterns = [
    # Pages publiques
    path('', views.providers, name='providers'),
    path('<int:provider_id>/', views.provider_detail, name='provider_detail'),
    
    # Inscription prestataire
    path('register/', views.provider_register, name='provider_register'),
    path('register/complete/', views.provider_register_complete, name='provider_register_complete'),
    
    # Dashboard et profil prestataire
    path('dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('profile/', views.provider_profile, name='provider_profile'),
    path('orders/', views.provider_orders, name='provider_orders'),
    
    # Gestion des commandes
    path('order/<int:order_id>/accept/', views.accept_order, name='accept_order'),
    path('order/<int:order_id>/reject/', views.reject_order, name='reject_order'),
    path('order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    
    # Gestion du profil
    path('upload-document/', views.upload_document, name='upload_document'),
    path('add-zone/', views.add_zone, name='add_zone'),
    path('toggle-availability/', views.toggle_availability, name='toggle_availability'),
] 