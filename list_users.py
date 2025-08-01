#!/usr/bin/env python
"""
Script pour lister tous les utilisateurs dans la base de données
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'togo_service.settings')
django.setup()

from django.contrib.auth.models import User

def list_all_users():
    """Liste tous les utilisateurs dans la base de données"""
    
    print("👥 LISTE DES UTILISATEURS DANS LA BASE DE DONNÉES")
    print("=" * 60)
    
    users = User.objects.all().order_by('date_joined')
    
    if not users.exists():
        print("❌ Aucun utilisateur trouvé dans la base de données")
        return
    
    print(f"📊 Total : {users.count()} utilisateur(s)")
    print()
    
    for i, user in enumerate(users, 1):
        # Déterminer le type d'utilisateur
        if user.is_superuser:
            user_type = "👑 SUPER ADMIN"
        elif user.is_staff:
            user_type = "👨‍💼 ADMIN"
        else:
            user_type = "👤 CLIENT"
        
        # Statut actif/inactif
        status = "✅ ACTIF" if user.is_active else "❌ INACTIF"
        
        print(f"{i:2d}. {user_type} | {status}")
        print(f"    👤 Username: {user.username}")
        print(f"    📧 Email: {user.email}")
        print(f"    📝 Nom: {user.first_name} {user.last_name}")
        print(f"    📅 Créé le: {user.date_joined.strftime('%d/%m/%Y %H:%M')}")
        
        # Afficher le mot de passe si c'est un utilisateur de test
        if user.username in ['admin', 'test_client', 'test_admin']:
            if user.username == 'admin':
                password = 'admin123'
            else:
                password = 'test123'
            print(f"    🔑 Password: {password}")
        
        print()

def create_missing_users():
    """Crée les utilisateurs manquants du README"""
    
    print("🔧 CRÉATION DES UTILISATEURS MANQUANTS")
    print("=" * 50)
    
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
            print(f"ℹ️ Existe déjà: {username}")
    
    print(f"\n📊 {created_count} nouveaux utilisateurs créés")

if __name__ == '__main__':
    print("🚀 VÉRIFICATION DES UTILISATEURS TOG-SERVICES")
    print("=" * 60)
    
    # Lister les utilisateurs existants
    list_all_users()
    
    print("\n" + "=" * 60)
    
    # Demander si créer les utilisateurs manquants
    response = input("\n❓ Voulez-vous créer les utilisateurs manquants du README ? (o/n): ")
    
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        create_missing_users()
        
        print("\n" + "=" * 60)
        print("📋 RÉCAPITULATIF FINAL")
        print("=" * 60)
        list_all_users()
    
    print("\n🎯 POUR VOUS CONNECTER :")
    print("- Allez sur : http://127.0.0.1:8000/users/login/")
    print("- Utilisez les identifiants listés ci-dessus") 