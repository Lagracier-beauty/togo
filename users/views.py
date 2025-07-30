from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

def home(request):
    """Page d'accueil"""
    return render(request, 'home.html')

def user_login(request):
    """Page de connexion"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie !')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Identifiants incorrects.')
    return render(request, 'login.html')

def user_register(request):
    """Page d'inscription client"""
    if request.method == 'POST':
        # Pour l'instant, on affiche juste un message de succès
        messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
        return redirect('login')
    return render(request, 'register.html')

def user_logout(request):
    """Déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('home')

@login_required
def user_dashboard(request):
    """Tableau de bord client"""
    return render(request, 'user_dashboard.html')

@login_required
def user_profile(request):
    """Profil utilisateur"""
    return render(request, 'user_profile.html')

@login_required
def user_orders(request):
    """Historique des commandes utilisateur"""
    return render(request, 'user_orders.html')

def search_services(request):
    """Recherche de services (pour HTMX)"""
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        location = request.POST.get('location')
        
        # Données fictives pour la démonstration
        providers = [
            {
                'name': 'Kossi A.',
                'service': 'Livraison de repas',
                'rating': 4.8,
                'reviews': 120,
                'available': True,
                'image': 'https://randomuser.me/api/portraits/men/32.jpg'
            },
            {
                'name': 'Ama D.',
                'service': 'Ménage',
                'rating': 4.9,
                'reviews': 98,
                'available': True,
                'image': 'https://randomuser.me/api/portraits/women/44.jpg'
            }
        ]
        
        return render(request, 'search_results.html', {
            'providers': providers,
            'service_type': service_type,
            'location': location
        })
    
    return HttpResponse('')
