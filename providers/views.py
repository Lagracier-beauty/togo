from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Count
from .models import Provider, ProviderDocument, ProviderZone
from .forms import ProviderRegistrationForm, ProviderProfileForm, ProviderDocumentForm, ProviderZoneForm
from services.models import Service
from orders.models import Order

def providers(request):
    """Page listant tous les prestataires approuvés"""
    # Filtres
    service_filter = request.GET.get('service', 'all')
    location_filter = request.GET.get('location', 'all')
    availability_filter = request.GET.get('availability', 'all')
    show_all = request.GET.get('show_all', 'false') == 'true'  # Nouveau paramètre
    
    # Prestataires approuvés
    providers = Provider.objects.filter(status='approved').select_related('user').prefetch_related('zones')
    
    # Appliquer les filtres
    if service_filter != 'all':
        providers = providers.filter(service_type=service_filter)
    
    if location_filter != 'all':
        providers = providers.filter(zones__city__icontains=location_filter).distinct()
    
    if availability_filter == 'available':
        providers = providers.filter(is_available=True)
    
    # Annotations pour les statistiques
    providers = providers.annotate(
        avg_rating=Avg('received_orders__rating__customer_rating'),
        total_reviews=Count('received_orders__rating', distinct=True)
    )
    
    # Compter le total avant limitation
    total_providers = providers.count()
    
    # Limiter à 6 si pas "show_all"
    if not show_all:
        providers = providers[:6]
    
    # Catégories de services pour les filtres
    service_types = Provider.SERVICE_TYPES
    
    # Villes disponibles
    cities = ProviderZone.objects.values_list('city', flat=True).distinct()
    
    context = {
        'providers': providers,
        'service_types': service_types,
        'cities': cities,
        'service_filter': service_filter,
        'location_filter': location_filter,
        'availability_filter': availability_filter,
        'show_all': show_all,
        'total_providers': total_providers,
        'displayed_count': len(providers),
    }
    
    return render(request, 'providers.html', context)

def provider_detail(request, provider_id):
    """Page détail d'un prestataire"""
    provider = get_object_or_404(Provider, id=provider_id, status='approved')
    
    # Services du prestataire
    services = Service.objects.filter(provider=provider, is_active=True)
    
    # Statistiques
    total_orders = Order.objects.filter(provider=provider, status='completed').count()
    avg_rating = Order.objects.filter(
        provider=provider, 
        rating__isnull=False
    ).aggregate(avg_rating=Avg('rating__customer_rating'))['avg_rating'] or 0
    
    # Avis récents
    recent_reviews = Order.objects.filter(
        provider=provider,
        rating__isnull=False,
        rating__customer_comment__isnull=False
    ).select_related('customer', 'rating').order_by('-completed_at')[:5]
    
    context = {
        'provider': provider,
        'services': services,
        'total_orders': total_orders,
        'avg_rating': round(avg_rating, 1) if avg_rating else 0,
        'recent_reviews': recent_reviews,
    }
    
    return render(request, 'provider_detail.html', context)

def provider_register(request):
    """Page d'inscription prestataire"""
    if request.user.is_authenticated:
        # Vérifier si l'utilisateur a déjà un profil prestataire
        try:
            provider = Provider.objects.get(user=request.user)
            messages.info(request, 'Vous avez déjà un profil prestataire.')
            return redirect('providers:provider_dashboard')
        except Provider.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            provider = form.save()
            messages.success(request, 'Inscription prestataire réussie ! Votre profil est en cours de validation.')
            return redirect('providers:provider_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProviderRegistrationForm()
    
    return render(request, 'provider_register.html', {'form': form})

@login_required
def provider_register_complete(request):
    """Compléter l'inscription prestataire pour les utilisateurs existants"""
    # Vérifier si l'utilisateur a déjà un profil prestataire
    try:
        provider = Provider.objects.get(user=request.user)
        return redirect('providers:provider_dashboard')
    except Provider.DoesNotExist:
        pass
    
    if request.method == 'POST':
        # Créer un formulaire simplifié pour les utilisateurs existants
        service_type = request.POST.get('service_type')
        description = request.POST.get('description', '')
        experience_years = request.POST.get('experience_years', 0)
        hourly_rate = request.POST.get('hourly_rate', 0)
        zones = request.POST.get('zones', '')
        accept_terms = request.POST.get('accept_terms')
        
        if not accept_terms:
            messages.error(request, 'Vous devez accepter les conditions générales.')
        else:
            # Créer le profil prestataire
            provider = Provider.objects.create(
                user=request.user,
                service_type=service_type,
                description=description,
                experience_years=int(experience_years) if experience_years else 0,
                hourly_rate=float(hourly_rate) if hourly_rate else 0,
                status='pending'
            )
            
            # Créer les zones d'intervention
            if zones:
                zones_list = [zone.strip() for zone in zones.split(',') if zone.strip()]
                for zone_name in zones_list:
                    ProviderZone.objects.create(provider=provider, city=zone_name)
            
            messages.success(request, 'Profil prestataire créé ! Il est en cours de validation.')
            return redirect('providers:provider_dashboard')
    
    context = {
        'service_types': Provider.SERVICE_TYPES,
    }
    return render(request, 'provider_register_complete.html', context)

@login_required
def provider_dashboard(request):
    """Tableau de bord prestataire"""
    try:
        provider = Provider.objects.get(user=request.user)
    except Provider.DoesNotExist:
        messages.error(request, 'Vous n\'avez pas de profil prestataire.')
        return redirect('providers:provider_register_complete')
    
    # Statistiques du prestataire
    provider_stats = {
        'total_services': provider.received_orders.count(),
        'completed_services': provider.received_orders.filter(status='completed').count(),
        'in_progress': provider.received_orders.filter(status__in=['accepted', 'in_progress', 'on_route']).count(),
        'total_earnings': sum(
            order.total_amount for order in provider.received_orders.filter(status='completed')
            if order.total_amount
        ),
        'average_rating': provider.rating,
        'pending_orders': provider.received_orders.filter(status='pending').count(),
    }
    
    # Commandes récentes
    recent_orders = provider.received_orders.select_related('customer', 'service').order_by('-created_at')[:10]
    
    # Services proposés
    services = provider.services.filter(is_active=True)[:5]
    
    context = {
        'provider': provider,
        'provider_stats': provider_stats,
        'recent_orders': recent_orders,
        'services': services,
    }
    return render(request, 'provider_dashboard.html', context)

@login_required
def provider_profile(request):
    """Profil prestataire avec modification"""
    try:
        provider = Provider.objects.get(user=request.user)
    except Provider.DoesNotExist:
        return redirect('providers:provider_register_complete')
    
    if request.method == 'POST':
        form = ProviderProfileForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès !')
            return redirect('providers:provider_profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProviderProfileForm(instance=provider)
    
    # Documents du prestataire
    documents = provider.documents.all()
    
    # Zones d'intervention
    zones = provider.zones.all()
    
    context = {
        'provider': provider,
        'form': form,
        'documents': documents,
        'zones': zones,
    }
    return render(request, 'provider_profile.html', context)

@login_required
def provider_orders(request):
    """Gestion des commandes prestataire"""
    try:
        provider = Provider.objects.get(user=request.user)
    except Provider.DoesNotExist:
        return redirect('providers:provider_register_complete')
    
    # Filtres
    status_filter = request.GET.get('status', 'all')
    date_filter = request.GET.get('date', 'all')
    
    orders = provider.received_orders.select_related('customer', 'service').order_by('-created_at')
    
    # Appliquer les filtres
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)
    
    if date_filter == 'week':
        from datetime import datetime, timedelta
        week_ago = datetime.now() - timedelta(days=7)
        orders = orders.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        from datetime import datetime, timedelta
        month_ago = datetime.now() - timedelta(days=30)
        orders = orders.filter(created_at__gte=month_ago)
    
    # Statistiques des commandes
    order_stats = {
        'total': provider.received_orders.count(),
        'pending': provider.received_orders.filter(status='pending').count(),
        'completed': provider.received_orders.filter(status='completed').count(),
        'cancelled': provider.received_orders.filter(status='cancelled').count(),
        'total_earnings': sum(
            order.total_amount for order in provider.received_orders.filter(status='completed')
            if order.total_amount
        ),
    }
    
    context = {
        'provider': provider,
        'orders': orders,
        'order_stats': order_stats,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'provider_orders.html', context)

@login_required
def accept_order(request, order_id):
    """Accepter une commande"""
    try:
        provider = Provider.objects.get(user=request.user)
        order = get_object_or_404(Order, id=order_id, provider=provider, status='pending')
        
        order.status = 'accepted'
        order.save()
        
        messages.success(request, f'Commande {order.order_number} acceptée !')
        return JsonResponse({'success': True, 'message': 'Commande acceptée'})
    except Provider.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Profil prestataire requis'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def reject_order(request, order_id):
    """Rejeter une commande"""
    try:
        provider = Provider.objects.get(user=request.user)
        order = get_object_or_404(Order, id=order_id, provider=provider, status='pending')
        
        order.status = 'rejected'
        order.save()
        
        messages.success(request, f'Commande {order.order_number} rejetée.')
        return JsonResponse({'success': True, 'message': 'Commande rejetée'})
    except Provider.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Profil prestataire requis'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def update_order_status(request, order_id):
    """Mettre à jour le statut d'une commande"""
    if request.method == 'POST':
        try:
            provider = Provider.objects.get(user=request.user)
            order = get_object_or_404(Order, id=order_id, provider=provider)
            new_status = request.POST.get('status')
            
            if new_status in [choice[0] for choice in Order.STATUS_CHOICES]:
                order.status = new_status
                order.save()
                
                messages.success(request, f'Statut de la commande {order.order_number} mis à jour.')
                return JsonResponse({'success': True, 'message': 'Statut mis à jour'})
            else:
                return JsonResponse({'success': False, 'message': 'Statut invalide'})
                
        except Provider.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Profil prestataire requis'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

@login_required
def upload_document(request):
    """Télécharger un document justificatif"""
    try:
        provider = Provider.objects.get(user=request.user)
    except Provider.DoesNotExist:
        return redirect('providers:provider_register_complete')
    
    if request.method == 'POST':
        form = ProviderDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.provider = provider
            document.save()
            messages.success(request, 'Document téléchargé avec succès !')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    return redirect('providers:provider_profile')

@login_required
def add_zone(request):
    """Ajouter une zone d'intervention"""
    try:
        provider = Provider.objects.get(user=request.user)
    except Provider.DoesNotExist:
        return redirect('providers:provider_register_complete')
    
    if request.method == 'POST':
        form = ProviderZoneForm(request.POST)
        if form.is_valid():
            zone = form.save(commit=False)
            zone.provider = provider
            zone.save()
            messages.success(request, 'Zone d\'intervention ajoutée !')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    return redirect('providers:provider_profile')

@login_required
def toggle_availability(request):
    """Basculer la disponibilité du prestataire"""
    try:
        provider = Provider.objects.get(user=request.user)
        provider.is_available = not provider.is_available
        provider.save()
        
        status = "disponible" if provider.is_available else "indisponible"
        messages.success(request, f'Vous êtes maintenant {status}.')
        
        return JsonResponse({
            'success': True, 
            'available': provider.is_available,
            'message': f'Statut mis à jour: {status}'
        })
    except Provider.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Profil prestataire requis'})
