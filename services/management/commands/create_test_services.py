from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import ServiceCategory, Service
from providers.models import Provider
from users.models import UserProfile

class Command(BaseCommand):
    help = 'Crée des données de test pour les services'

    def handle(self, *args, **options):
        # Créer des catégories de services
        categories_data = [
            {'name': 'Transport', 'description': 'Services de transport', 'icon': 'fa-car', 'color': '#007bff', 'order': 1},
            {'name': 'Livraison', 'description': 'Services de livraison', 'icon': 'fa-truck', 'color': '#28a745', 'order': 2},
            {'name': 'Ménage', 'description': 'Services de ménage', 'icon': 'fa-broom', 'color': '#ffc107', 'order': 3},
            {'name': 'Bricolage', 'description': 'Services de bricolage', 'icon': 'fa-tools', 'color': '#dc3545', 'order': 4},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Catégorie créée: {category.name}')
        
        # Créer des utilisateurs de test si ils n'existent pas
        users_data = [
            {'username': 'prestataire1', 'first_name': 'Jean', 'last_name': 'Dupont', 'email': 'jean@test.com'},
            {'username': 'prestataire2', 'first_name': 'Marie', 'last_name': 'Martin', 'email': 'marie@test.com'},
            {'username': 'prestataire3', 'first_name': 'Pierre', 'last_name': 'Durand', 'email': 'pierre@test.com'},
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('test123')
                user.save()
                self.stdout.write(f'Utilisateur créé: {user.username}')
            users.append(user)
        
        # Créer des profils utilisateurs avec des villes
        cities = ['Lomé', 'Kara', 'Sokodé', 'Kpalimé']
        for i, user in enumerate(users):
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'city': cities[i % len(cities)]}
            )
            if created:
                self.stdout.write(f'Profil créé pour {user.username} à {profile.city}')
        
        # Créer des prestataires
        providers = []
        for user in users:
            provider, created = Provider.objects.get_or_create(
                user=user,
                defaults={
                    'service_type': 'transport' if user.username == 'prestataire1' else 'livraison' if user.username == 'prestataire2' else 'menage',
                    'status': 'approved',
                    'is_available': True,
                    'description': f'Prestataire {user.get_full_name()}',
                    'experience_years': 2,
                    'hourly_rate': 25.0,
                }
            )
            providers.append(provider)
            if created:
                self.stdout.write(f'Prestataire créé: {provider.user.get_full_name()}')
        
        # Créer des services
        services_data = [
            {'title': 'Transport en ville', 'category': 'Transport', 'pricing_type': 'fixed', 'base_price': 15.0, 'description': 'Transport rapide en ville'},
            {'title': 'Livraison de colis', 'category': 'Livraison', 'pricing_type': 'fixed', 'base_price': 30.0, 'description': 'Livraison de colis dans toute la ville'},
            {'title': 'Ménage complet', 'category': 'Ménage', 'pricing_type': 'hourly', 'base_price': 20.0, 'description': 'Service de ménage complet'},
            {'title': 'Réparation électrique', 'category': 'Bricolage', 'pricing_type': 'fixed', 'base_price': 50.0, 'description': 'Réparation d\'installations électriques'},
            {'title': 'Transport longue distance', 'category': 'Transport', 'pricing_type': 'distance', 'base_price': 100.0, 'description': 'Transport inter-villes'},
            {'title': 'Nettoyage de vitres', 'category': 'Ménage', 'pricing_type': 'fixed', 'base_price': 25.0, 'description': 'Nettoyage professionnel de vitres'},
        ]
        
        for service_data in services_data:
            category = next(cat for cat in categories if cat.name == service_data['category'])
            provider = providers[0]  # Utiliser le premier prestataire pour tous les services
            
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                provider=provider,
                defaults={
                    'category': category,
                    'pricing_type': service_data['pricing_type'],
                    'base_price': service_data['base_price'],
                    'description': service_data['description'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'Service créé: {service.title}')
        
        self.stdout.write(self.style.SUCCESS('Données de test créées avec succès!')) 