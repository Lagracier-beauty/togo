from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from users.models import UserProfile

def home(request):
    """Page d'accueil"""
    return render(request, 'home.html')

def user_login(request):
    """Page de connexion avec feedback et connexion par email ou username"""
    errors = {}
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = None
        # Permettre la connexion par email ou username
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        if '@' in username_or_email:
            try:
                user_obj = UserModel.objects.get(email=username_or_email)
                username = user_obj.username
            except UserModel.DoesNotExist:
                username = username_or_email
        else:
            username = username_or_email
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie !')
            return redirect('users:user_dashboard')
        else:
            errors['general'] = "Identifiants incorrects."
    return render(request, 'login.html', {'errors': errors})

def user_register(request):
    """Page d'inscription client avec création réelle d'utilisateur et validation"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        errors = {}

        # Validation des champs
        if not name:
            errors['name'] = "Le nom complet est requis."
        if not email:
            errors['email'] = "L'email est requis."
        elif User.objects.filter(email=email).exists():
            errors['email'] = "Cet email est déjà utilisé."
        if not phone:
            errors['phone'] = "Le numéro de téléphone est requis."
        if not password or len(password) < 8:
            errors['password'] = "Le mot de passe doit contenir au moins 8 caractères."

        # Découper le nom complet
        first_name, *last_name = name.split(' ', 1)
        last_name = last_name[0] if last_name else ''

        if not errors:
            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                # Mettre à jour le profil
                user.profile.phone = phone
                user.profile.save()
                messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
                return redirect('users:login')
            except Exception as e:
                errors['general'] = "Erreur lors de la création du compte. Veuillez réessayer."
        # Afficher les erreurs dans le template
        return render(request, 'register.html', {
            'errors': errors,
            'form': {
                'name': name,
                'email': email,
                'phone': phone
            }
        })
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
    from orders.models import Order
    commandes = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_orders.html', {'commandes': commandes})

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
