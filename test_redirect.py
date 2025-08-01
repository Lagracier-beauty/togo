#!/usr/bin/env python
"""
Script de test pour vérifier la redirection selon le type d'utilisateur
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'togo_service.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def test_user_redirects():
    """Teste les redirections selon le type d'utilisateur"""
    
    print("🧪 Test des redirections utilisateur...")
    
    # Créer un utilisateur normal
    normal_user, created = User.objects.get_or_create(
        username='test_client',
        defaults={
            'email': 'client@test.com',
            'password': make_password('test123'),
            'first_name': 'Test',
            'last_name': 'Client',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True
        }
    )
    
    if created:
        print("✅ Utilisateur client créé")
    else:
        print("ℹ️ Utilisateur client existe déjà")
    
    # Créer un utilisateur admin
    admin_user, created = User.objects.get_or_create(
        username='test_admin',
        defaults={
            'email': 'admin@test.com',
            'password': make_password('test123'),
            'first_name': 'Test',
            'last_name': 'Admin',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        }
    )
    
    if created:
        print("✅ Utilisateur admin créé")
    else:
        print("ℹ️ Utilisateur admin existe déjà")
    
    print("\n🔑 Identifiants de test :")
    print("👤 Client normal : test_client / test123")
    print("👨‍💼 Admin : test_admin / test123")
    
    print("\n🎯 Comportement attendu :")
    print("1. Client normal → Page d'accueil (/)")
    print("2. Admin → Dashboard admin (/dashboard/admin/)")
    print("3. Avec paramètre 'next' → Page demandée")
    
    print("\n🔗 URLs de test :")
    print("- Login : http://127.0.0.1:8000/users/login/")
    print("- Dashboard admin : http://127.0.0.1:8000/dashboard/admin/")
    print("- Page d'accueil : http://127.0.0.1:8000/")

if __name__ == '__main__':
    test_user_redirects() 