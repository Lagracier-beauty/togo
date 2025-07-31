from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile
from providers.models import Provider

class Command(BaseCommand):
    help = 'Crée les utilisateurs de test mentionnés dans le README'

    def handle(self, *args, **options):
        # Utilisateurs clients
        clients_data = [
            {
                'username': 'marie_client',
                'first_name': 'Marie',
                'last_name': 'Dupont',
                'email': 'marie@example.com',
                'password': 'password123',
                'city': 'Lomé',
                'phone': '+22890123456'
            },
            {
                'username': 'jean_client',
                'first_name': 'Jean',
                'last_name': 'Martin',
                'email': 'jean@example.com',
                'password': 'password123',
                'city': 'Kara',
                'phone': '+22890123457'
            },
            {
                'username': 'sophie_client',
                'first_name': 'Sophie',
                'last_name': 'Bernard',
                'email': 'sophie@example.com',
                'password': 'password123',
                'city': 'Sokodé',
                'phone': '+22890123458'
            }
        ]

        # Utilisateurs prestataires
        providers_data = [
            {
                'username': 'pierre_provider',
                'first_name': 'Pierre',
                'last_name': 'Durand',
                'email': 'pierre@example.com',
                'password': 'password123',
                'city': 'Lomé',
                'phone': '+22890123459',
                'service_type': 'transport',
                'description': 'Chauffeur professionnel avec 5 ans d\'expérience',
                'hourly_rate': 30.0
            },
            {
                'username': 'marie_provider',
                'first_name': 'Marie',
                'last_name': 'Leroy',
                'email': 'marie.provider@example.com',
                'password': 'password123',
                'city': 'Kpalimé',
                'phone': '+22890123460',
                'service_type': 'menage',
                'description': 'Femme de ménage professionnelle',
                'hourly_rate': 25.0
            },
            {
                'username': 'paul_provider',
                'first_name': 'Paul',
                'last_name': 'Moreau',
                'email': 'paul@example.com',
                'password': 'password123',
                'city': 'Kara',
                'phone': '+22890123461',
                'service_type': 'livraison',
                'description': 'Livreur expérimenté',
                'hourly_rate': 20.0
            }
        ]

        # Créer les clients
        for client_data in clients_data:
            user, created = User.objects.get_or_create(
                username=client_data['username'],
                defaults={
                    'first_name': client_data['first_name'],
                    'last_name': client_data['last_name'],
                    'email': client_data['email'],
                }
            )
            
            if created:
                user.set_password(client_data['password'])
                user.save()
                self.stdout.write(f'Client créé: {user.username}')
            else:
                # Mettre à jour le mot de passe si l'utilisateur existe déjà
                user.set_password(client_data['password'])
                user.save()
                self.stdout.write(f'Mot de passe mis à jour pour: {user.username}')

            # Créer le profil utilisateur
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'city': client_data['city'],
                    'phone': client_data['phone'],
                    'user_type': 'client'
                }
            )
            if created:
                self.stdout.write(f'Profil client créé pour: {user.username}')

        # Créer les prestataires
        for provider_data in providers_data:
            user, created = User.objects.get_or_create(
                username=provider_data['username'],
                defaults={
                    'first_name': provider_data['first_name'],
                    'last_name': provider_data['last_name'],
                    'email': provider_data['email'],
                }
            )
            
            if created:
                user.set_password(provider_data['password'])
                user.save()
                self.stdout.write(f'Prestataire créé: {user.username}')
            else:
                # Mettre à jour le mot de passe si l'utilisateur existe déjà
                user.set_password(provider_data['password'])
                user.save()
                self.stdout.write(f'Mot de passe mis à jour pour: {user.username}')

            # Créer le profil utilisateur
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'city': provider_data['city'],
                    'phone': provider_data['phone'],
                    'user_type': 'provider'
                }
            )
            if created:
                self.stdout.write(f'Profil prestataire créé pour: {user.username}')

            # Créer le profil prestataire
            provider, created = Provider.objects.get_or_create(
                user=user,
                defaults={
                    'service_type': provider_data['service_type'],
                    'description': provider_data['description'],
                    'hourly_rate': provider_data['hourly_rate'],
                    'status': 'approved',
                    'is_available': True,
                    'experience_years': 3
                }
            )
            if created:
                self.stdout.write(f'Profil Provider créé pour: {user.username}')

        self.stdout.write(self.style.SUCCESS('Tous les utilisateurs de test ont été créés avec succès!'))
        self.stdout.write('\nUtilisateurs disponibles:')
        self.stdout.write('CLIENTS (password: password123):')
        for client in clients_data:
            self.stdout.write(f'  {client["username"]} - {client["first_name"]} {client["last_name"]} - {client["email"]}')
        
        self.stdout.write('\nPRESTATAIRES (password: password123):')
        for provider in providers_data:
            self.stdout.write(f'  {provider["username"]} - {provider["first_name"]} {provider["last_name"]} - {provider["email"]}') 