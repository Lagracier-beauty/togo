from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def support_page(request):
    """Page support et FAQ"""
    if request.method == 'POST':
        # Pour l'instant, on affiche juste un message de succès
        messages.success(request, 'Votre message a été envoyé ! Nous vous répondrons dans les plus brefs délais.')
        return redirect('support')
    return render(request, 'support.html')
