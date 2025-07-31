from django.shortcuts import render
from django.db.models import Q, Avg, Count
from .models import Service, ServiceCategory
from providers.models import ProviderZone

# Create your views here.

def services_list(request):
    """Liste des services avec filtres"""
    # Filtres
    category_filter = request.GET.get('category', 'all')
    location_filter = request.GET.get('location', 'all')
    price_filter = request.GET.get('price', 'all')
    show_all = request.GET.get('show_all', 'false') == 'true'  # Nouveau paramètre
    
    # Services actifs
    services = Service.objects.filter(is_active=True).select_related(
        'provider', 'provider__user', 'category'
    ).prefetch_related('images')
    
    # Appliquer les filtres
    if category_filter != 'all':
        services = services.filter(category_id=category_filter)
    
    if location_filter != 'all':
        services = services.filter(
            provider__zones__city__icontains=location_filter
        ).distinct()
    
    # Filtre prix
    if price_filter != 'all':
        if price_filter == '0-25':
            services = services.filter(
                Q(base_price__lte=25) | Q(max_price__lte=25)
            )
        elif price_filter == '25-50':
            services = services.filter(
                Q(base_price__range=(25, 50)) | Q(max_price__range=(25, 50))
            )
        elif price_filter == '50-100':
            services = services.filter(
                Q(base_price__range=(50, 100)) | Q(max_price__range=(50, 100))
            )
        elif price_filter == '100+':
            services = services.filter(
                Q(base_price__gte=100) | Q(min_price__gte=100)
            )
    
    # Annotations pour les statistiques
    # Note: On utilise les @property methods du modèle au lieu d'annotations
    # car la relation avec les reviews n'est pas directe
    
    # Compter le total avant limitation
    total_services = services.count()
    
    # Limiter à 6 si pas "show_all"
    if not show_all:
        services = services[:6]
    
    # Catégories pour les filtres
    categories = ServiceCategory.objects.filter(is_active=True).order_by('order')
    
    # Villes disponibles
    cities = ProviderZone.objects.values_list('city', flat=True).distinct()
    
    context = {
        'services': services,
        'categories': categories,
        'cities': cities,
        'category_filter': category_filter,
        'location_filter': location_filter,
        'price_filter': price_filter,
        'show_all': show_all,
        'total_services': total_services,
        'displayed_count': len(services),
    }
    
    return render(request, 'services.html', context)
