#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'togo_service.settings')
django.setup()

from django.contrib.auth.models import User

def make_admin(username):
    """Donne les droits d'administrateur à un utilisateur"""
    try:
        user = User.objects.get(username=username)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f'✅ Utilisateur {username} est maintenant administrateur!')
        print(f'   - is_staff: {user.is_staff}')
        print(f'   - is_superuser: {user.is_superuser}')
        print(f'   - Peut accéder au dashboard admin: /dashboard/admin/')
    except User.DoesNotExist:
        print(f'❌ Utilisateur {username} n\'existe pas!')
        print('Utilisateurs disponibles:')
        for u in User.objects.all():
            print(f'   - {u.username} ({u.email})')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = 'marie_client'  # Utilisateur par défaut
    
    make_admin(username) 