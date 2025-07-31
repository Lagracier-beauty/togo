#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'togo_service.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

def create_marie_user():
    """Crée l'utilisateur marie_client"""
    
    # Créer l'utilisateur
    user, created = User.objects.get_or_create(
        username='marie_client',
        defaults={
            'first_name': 'Marie',
            'last_name': 'Dupont',
            'email': 'marie@example.com',
        }
    )
    
    if created:
        user.set_password('password123')
        user.save()
        print(f'Utilisateur créé: {user.username}')
    else:
        user.set_password('password123')
        user.save()
        print(f'Mot de passe mis à jour pour: {user.username}')
    
    # Créer le profil utilisateur
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'city': 'Lomé',
            'phone': '+22890123456',
            'user_type': 'client'
        }
    )
    
    if created:
        print(f'Profil créé pour: {user.username}')
    else:
        print(f'Profil existant pour: {user.username}')
    
    print(f'\nUtilisateur disponible:')
    print(f'Username: {user.username}')
    print(f'Email: {user.email}')
    print(f'Password: password123')
    print(f'Nom complet: {user.get_full_name()}')

if __name__ == '__main__':
    create_marie_user() 