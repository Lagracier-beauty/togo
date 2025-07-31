from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from providers.models import Provider
from orders.models import Order
from services.models import Service

def is_admin(user):
    """Vérifie si l'utilisateur est admin (staff ou superuser)"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
def admin_dashboard(request):
    """Tableau de bord administrateur - SÉCURISÉ"""
    
    # Vérification de connexion
    if not request.user.is_authenticated:
        return redirect('/users/login/')
    
    # Vérification de sécurité admin
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Accès refusé. Vous devez être administrateur pour accéder à cette page.")
        return redirect('users:home')
    
    # Statistiques de la plateforme
    stats = {
        'total_users': User.objects.count(),
        'total_providers': Provider.objects.count(),
        'total_orders': Order.objects.count(),
        'total_services': Service.objects.filter(is_active=True).count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'completed_orders': Order.objects.filter(status='completed').count(),
        'providers_pending': Provider.objects.filter(status='pending').count(),
    }
    
    # Activité récente
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_orders = Order.objects.select_related('customer', 'provider', 'service').order_by('-created_at')[:10]
    recent_providers = Provider.objects.select_related('user').order_by('-created_at')[:5]
    
    context = {
        'stats': stats,
        'recent_users': recent_users,
        'recent_orders': recent_orders,
        'recent_providers': recent_providers,
    }
    
    return render(request, 'admin_dashboard.html', context)
