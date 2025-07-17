from django.shortcuts import render

# Create your views here.

def services_list(request):
    """Liste des services"""
    return render(request, 'services.html')
