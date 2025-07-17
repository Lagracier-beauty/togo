from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def provider_register(request):
    """Page d'inscription prestataire"""
    if request.method == 'POST':
        # Pour l'instant, on affiche juste un message de succès
        messages.success(request, 'Inscription prestataire soumise ! Votre compte sera validé sous 24h.')
        return redirect('home')
    return render(request, 'provider_register.html')

@login_required
def provider_dashboard(request):
    """Tableau de bord prestataire"""
    return render(request, 'provider_dashboard.html')

@login_required
def provider_profile(request):
    """Profil prestataire"""
    return render(request, 'provider_profile.html')

@login_required
def provider_orders(request):
    """Historique des prestations"""
    return render(request, 'provider_orders.html')

def providers_list(request):
    """Liste des prestataires"""
    return render(request, 'providers.html')
