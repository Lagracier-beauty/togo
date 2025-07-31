from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django import forms

# Formulaires simples
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nom d\'utilisateur ou Email',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Entrez votre nom d\'utilisateur ou email'
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Entrez votre mot de passe'
        })
    )

class RegisterForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('provider', 'Prestataire de services'),
    ]
    
    user_type = forms.ChoiceField(
        label='Type de compte',
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-radio'})
    )
    first_name = forms.CharField(
        label='Prénom',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Votre prénom'
        })
    )
    last_name = forms.CharField(
        label='Nom de famille',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Votre nom de famille'
        })
    )
    username = forms.CharField(
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Choisissez un nom d\'utilisateur'
        })
    )
    email = forms.EmailField(
        label='Adresse email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'votre@email.com'
        })
    )
    phone = forms.CharField(
        label='Téléphone',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+228 XX XX XX XX'
        })
    )
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Créez un mot de passe sécurisé'
        })
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirmez votre mot de passe'
        })
    )

def home(request):
    """Page d'accueil avec statistiques et services en vedette"""
    # Version simplifiée
    context = {
        'stats': {
            'total_users': 0,
            'total_providers': 0,
            'total_orders': 0,
            'total_services': 0,
        },
        'featured_services': [],
        'categories': [],
    }
    
    return render(request, 'home.html', context)

def test_page(request):
    """Page de test pour diagnostiquer les problèmes"""
    from datetime import datetime
    
    context = {
        'now': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'debug_info': {
            'user_agent': request.META.get('HTTP_USER_AGENT', 'Non disponible'),
            'ip': request.META.get('REMOTE_ADDR', 'Non disponible'),
            'method': request.method,
            'path': request.path,
        },
        'urls_test': {
            'login_url': '/login/',
            'register_url': '/register/',
            'home_url': '/',
        }
    }
    
    return render(request, 'test.html', context)



def user_login(request):
    """Page de connexion avec redirection intelligente"""
    # Temporairement commenté pour permettre l'accès
    # if request.user.is_authenticated:
    #     return redirect('users:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Essayer de s'authentifier avec le nom d'utilisateur
            user = authenticate(username=username_or_email, password=password)
            
            # Si ça ne marche pas, essayer avec l'email
            if user is None and '@' in username_or_email:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bon retour, {user.first_name or user.username} !')
                return redirect('users:home')
            else:
                messages.error(request, 'Identifiants incorrects.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def user_register(request):
    """Page d'inscription client avec validation"""
    # Temporairement commenté pour permettre l'accès
    # if request.user.is_authenticated:
    #     return redirect('users:home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Validation des mots de passe
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            
            if password1 != password2:
                messages.error(request, 'Les mots de passe ne correspondent pas.')
                return render(request, 'register.html', {'form': form})
            
            # Vérifier si l'utilisateur existe déjà
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Ce nom d\'utilisateur est déjà pris.')
                return render(request, 'register.html', {'form': form})
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Cette adresse email est déjà utilisée.')
                return render(request, 'register.html', {'form': form})
            
            # Créer l'utilisateur
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name')
                )
                
                # Connexion automatique
                login(request, user)
                
                user_type = form.cleaned_data.get('user_type')
                if user_type == 'provider':
                    messages.success(request, 'Inscription réussie ! Vous pouvez maintenant compléter votre profil prestataire.')
                else:
                    messages.success(request, 'Inscription réussie ! Bienvenue sur Tog-Services.')
                
                return redirect('users:home')
                
            except Exception as e:
                messages.error(request, f'Erreur lors de la création du compte: {str(e)}')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    """Déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('users:home')

def force_logout(request):
    """Déconnexion forcée pour tests"""
    logout(request)
    messages.success(request, 'Déconnexion forcée effectuée.')
    return redirect('users:home')
