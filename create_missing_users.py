#!/usr/bin/env python
"""
Script pour créer les utilisateurs manquants du README
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'togo_service.settings')
django.setup()

from django.contrib.auth.models import User

def create_missing_users():
    """Crée les utilisateurs manquants du README"""
    
    print("🔧 CRÉATION DES UTILISATEURS MANQUANTS DU README")
    print("=" * 60)
    
    # Liste des clients du README
    clients = [
        ('pierre_client', 'Pierre', 'Martin', 'pierre@example.com'),
        ('ama_client', 'Ama', 'Koffi', 'ama@example.com'),
        ('kofi_client', 'Kofi', 'Asante', 'kofi@example.com'),
        ('akosua_client', 'Akosua', 'Mensah', 'akosua@example.com'),
        ('kwame_client', 'Kwame', 'Tetteh', 'kwame@example.com'),
        ('efua_client', 'Efua', 'Boateng', 'efua@example.com'),
        ('yao_client', 'Yao', 'Agbemenu', 'yao@example.com'),
        ('adjoa_client', 'Adjoa', 'Nyong', 'adjoa@example.com'),
        ('kodjo_client', 'Kodjo', 'Amavi', 'kodjo@example.com'),
        ('abla_client', 'Abla', 'Senah', 'abla@example.com'),
        ('komla_client', 'Komla', 'Dossou', 'komla@example.com'),
    ]
    
    password = 'password123'  # Mot de passe du README
    
    created_count = 0
    for username, first_name, last_name, email in clients:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'is_staff': False,
                'is_superuser': False,
                'is_active': True
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            print(f"✅ Créé: {username} ({first_name} {last_name})")
            created_count += 1
        else:
            print(f"ℹ️ Existe déjà: {username} ({first_name} {last_name})")
    
    print(f"\n📊 {created_count} nouveaux utilisateurs créés")
    
    # Afficher un récapitulatif des identifiants
    print("\n🔑 IDENTIFIANTS POUR SE CONNECTER :")
    print("=" * 40)
    print("👑 ADMINS (→ Dashboard Admin) :")
    print("  - admin / admin123")
    print("  - marie_client / password123")
    print("  - test_admin / test123")
    print()
    print("👤 CLIENTS (→ Page d'Accueil) :")
    for username, first_name, last_name, _ in clients:
        print(f"  - {username} / password123")
    
    print("\n🎯 POUR VOUS CONNECTER :")
    print("- Allez sur : http://127.0.0.1:8000/users/login/")
    print("- Utilisez les identifiants ci-dessus")

if __name__ == '__main__':
    create_missing_users() 