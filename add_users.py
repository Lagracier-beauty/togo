import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'togo_service.settings')
django.setup()

from django.contrib.auth.models import User

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

password = 'password123'
created_count = 0

print("🔧 Création des utilisateurs manquants...")

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
        print(f"✅ Créé: {username}")
        created_count += 1
    else:
        print(f"ℹ️ Existe déjà: {username}")

print(f"\n📊 {created_count} nouveaux utilisateurs créés")

print("\n🔑 IDENTIFIANTS POUR SE CONNECTER :")
print("👑 ADMINS (→ Dashboard Admin) :")
print("  - admin / admin123")
print("  - marie_client / password123")
print("  - test_admin / test123")
print("\n👤 CLIENTS (→ Page d'Accueil) :")
for username, _, _, _ in clients:
    print(f"  - {username} / password123") 