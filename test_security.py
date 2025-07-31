#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'togo_service.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

def test_admin_security():
    """Test la sécurité du dashboard admin"""
    client = Client()
    
    print("🔒 Test de sécurité du Dashboard Admin")
    print("=" * 50)
    
    # Test 1: Accès sans connexion
    print("\n1. Test accès sans connexion...")
    response = client.get('/dashboard/admin/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 302:
        print(f"   Redirection vers: {response.url}")
        if 'login' in response.url:
            print("   ✅ Redirection vers login correcte")
        else:
            print("   ❌ Mauvaise redirection")
    else:
        print("   ❌ Pas de redirection")
    
    # Test 2: Accès avec utilisateur normal
    print("\n2. Test accès avec utilisateur normal...")
    # Créer un utilisateur normal
    normal_user, created = User.objects.get_or_create(
        username='test_user',
        defaults={'email': 'test@example.com'}
    )
    normal_user.set_password('test123')
    normal_user.save()
    
    # Se connecter
    client.login(username='test_user', password='test123')
    response = client.get('/dashboard/admin/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 302:
        print(f"   Redirection vers: {response.url}")
        if 'home' in response.url:
            print("   ✅ Redirection vers home correcte (pas admin)")
        else:
            print("   ❌ Mauvaise redirection")
    else:
        print("   ❌ Pas de redirection")
    
    # Test 3: Accès avec utilisateur admin
    print("\n3. Test accès avec utilisateur admin...")
    # Utiliser marie_client qui est maintenant admin
    client.login(username='marie_client', password='password123')
    response = client.get('/dashboard/admin/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Accès autorisé au dashboard admin")
    else:
        print(f"   ❌ Accès refusé: {response.status_code}")
    
    # Nettoyer
    if created:
        normal_user.delete()
    
    print("\n" + "=" * 50)
    print("✅ Tests de sécurité terminés!")

if __name__ == '__main__':
    test_admin_security() 