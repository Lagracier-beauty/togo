#!/usr/bin/env python
"""
Script pour créer un superuser admin pour Tog-Services
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'togo_service.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def create_admin_user():
    """Crée un superuser admin"""
    
    # Identifiants admin
    username = 'admin'
    email = 'admin@togservices.com'
    password = 'admin123'
    
    try:
        # Vérifier si l'utilisateur existe déjà
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'password': make_password(password),
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
                'first_name': 'Admin',
                'last_name': 'Tog-Services'
            }
        )
        
        if created:
            print("✅ Superuser admin créé avec succès !")
            print(f"👤 Username: {username}")
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
            print("\n🔗 URLs de test:")
            print(f"   - Admin Django: http://127.0.0.1:8000/admin/")
            print(f"   - Dashboard Admin: http://127.0.0.1:8000/dashboard/admin/")
            print(f"   - Login: http://127.0.0.1:8000/users/login/")
        else:
            # Mettre à jour le mot de passe si l'utilisateur existe
            user.password = make_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            print("✅ Superuser admin mis à jour !")
            print(f"👤 Username: {username}")
            print(f"🔑 Password: {password}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🚀 Création du superuser admin pour Tog-Services...")
    success = create_admin_user()
    
    if success:
        print("\n🎯 Test de sécurité:")
        print("1. Allez sur http://127.0.0.1:8000/dashboard/admin/ (sans être connecté)")
        print("2. Vous devriez être redirigé vers http://127.0.0.1:8000/users/login/")
        print("3. Connectez-vous avec les identifiants ci-dessus")
        print("4. Vous devriez accéder au dashboard admin")
    else:
        print("❌ Échec de la création du superuser")
        sys.exit(1) 