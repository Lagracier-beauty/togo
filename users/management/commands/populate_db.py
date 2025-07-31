from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile, UserAddress
from providers.models import Provider, ProviderZone
from services.models import ServiceCategory, Service
from orders.models import Order
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Peuple la base de données avec des données d\'exemple enrichies'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Début du peuplement enrichi de la base de données...'))
        
        # Créer des catégories de services
        self.create_service_categories()
        
        # Créer des utilisateurs clients (beaucoup plus)
        self.create_client_users()
        
        # Créer des prestataires (beaucoup plus)
        self.create_providers()
        
        # Créer des services (beaucoup plus)
        self.create_services()
        
        # Créer des commandes d'exemple (plus nombreuses)
        self.create_sample_orders()
        
        self.stdout.write(self.style.SUCCESS('Base de données enrichie avec succès !'))

    def create_service_categories(self):
        """Créer les catégories de services"""
        categories = [
            {
                'name': 'Livraison de Repas',
                'description': 'Livraison de repas et restauration rapide',
                'icon': 'fas fa-utensils',
                'color': '#e74c3c'
            },
            {
                'name': 'Transport',
                'description': 'Transport de personnes et marchandises',
                'icon': 'fas fa-car',
                'color': '#3498db'
            },
            {
                'name': 'Ménage',
                'description': 'Services de nettoyage et entretien',
                'icon': 'fas fa-broom',
                'color': '#2ecc71'
            },
            {
                'name': 'Bricolage',
                'description': 'Petits travaux et réparations',
                'icon': 'fas fa-tools',
                'color': '#f39c12'
            },
            {
                'name': 'Courses',
                'description': 'Courses et achats divers',
                'icon': 'fas fa-shopping-bag',
                'color': '#9b59b6'
            },
            {
                'name': 'Jardinage',
                'description': 'Entretien d\'espaces verts et jardins',
                'icon': 'fas fa-seedling',
                'color': '#27ae60'
            },
            {
                'name': 'Garde d\'enfants',
                'description': 'Services de garde et baby-sitting',
                'icon': 'fas fa-baby',
                'color': '#e67e22'
            },
            {
                'name': 'Informatique',
                'description': 'Réparation et maintenance informatique',
                'icon': 'fas fa-laptop',
                'color': '#34495e'
            },
        ]
        
        for i, cat_data in enumerate(categories):
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'order': i,
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f"Catégorie créée: {category.name}")

    def create_client_users(self):
        """Créer des utilisateurs clients"""
        clients_data = [
            # Clients existants
            {
                'username': 'marie_client',
                'first_name': 'Marie',
                'last_name': 'Dupont',
                'email': 'marie@example.com',
                'phone': '+228 90 12 34 56'
            },
            {
                'username': 'pierre_client',
                'first_name': 'Pierre',
                'last_name': 'Martin',
                'email': 'pierre@example.com',
                'phone': '+228 90 23 45 67'
            },
            {
                'username': 'ama_client',
                'first_name': 'Ama',
                'last_name': 'Koffi',
                'email': 'ama@example.com',
                'phone': '+228 90 34 56 78'
            },
            # Nouveaux clients
            {
                'username': 'kofi_client',
                'first_name': 'Kofi',
                'last_name': 'Asante',
                'email': 'kofi@example.com',
                'phone': '+228 90 45 67 89'
            },
            {
                'username': 'akosua_client',
                'first_name': 'Akosua',
                'last_name': 'Mensah',
                'email': 'akosua@example.com',
                'phone': '+228 90 56 78 90'
            },
            {
                'username': 'kwame_client',
                'first_name': 'Kwame',
                'last_name': 'Tetteh',
                'email': 'kwame@example.com',
                'phone': '+228 90 67 89 01'
            },
            {
                'username': 'efua_client',
                'first_name': 'Efua',
                'last_name': 'Boateng',
                'email': 'efua@example.com',
                'phone': '+228 90 78 90 12'
            },
            {
                'username': 'yao_client',
                'first_name': 'Yao',
                'last_name': 'Agbemenu',
                'email': 'yao@example.com',
                'phone': '+228 90 89 01 23'
            },
            {
                'username': 'adjoa_client',
                'first_name': 'Adjoa',
                'last_name': 'Nyong',
                'email': 'adjoa@example.com',
                'phone': '+228 90 90 12 34'
            },
            {
                'username': 'kodjo_client',
                'first_name': 'Kodjo',
                'last_name': 'Amavi',
                'email': 'kodjo@example.com',
                'phone': '+228 90 01 23 45'
            },
            {
                'username': 'abla_client',
                'first_name': 'Abla',
                'last_name': 'Senah',
                'email': 'abla@example.com',
                'phone': '+228 90 12 34 67'
            },
            {
                'username': 'komla_client',
                'first_name': 'Komla',
                'last_name': 'Dossou',
                'email': 'komla@example.com',
                'phone': '+228 90 23 45 78'
            }
        ]
        
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
                user.set_password('password123')
                user.save()
                
                # Mettre à jour le profil
                user.profile.phone = client_data['phone']
                user.profile.total_orders = random.randint(1, 15)
                user.profile.total_spent = Decimal(random.randint(5000, 50000))
                user.profile.average_rating_given = round(random.uniform(4.0, 5.0), 1)
                user.profile.save()
                
                self.stdout.write(f"Client créé: {user.get_full_name()}")

    def create_providers(self):
        """Créer des prestataires"""
        providers_data = [
            # Prestataires existants
            {
                'username': 'kossi_transport',
                'first_name': 'Kossi',
                'last_name': 'Adjonou',
                'email': 'kossi@example.com',
                'phone': '+228 92 11 22 33',
                'service_type': 'transport',
                'description': 'Chauffeur expérimenté avec véhicule climatisé. Service de transport fiable dans tout Lomé.',
                'experience_years': 5,
                'hourly_rate': 2500,
                'zones': ['Lomé Centre', 'Tokoin', 'Nyékonakpoé']
            },
            {
                'username': 'ama_menage',
                'first_name': 'Ama',
                'last_name': 'Dzogbetsi',
                'email': 'ama.menage@example.com',
                'phone': '+228 92 33 44 55',
                'service_type': 'menage',
                'description': 'Spécialiste du nettoyage résidentiel et commercial. Produits écologiques disponibles.',
                'experience_years': 3,
                'hourly_rate': 1500,
                'zones': ['Lomé Centre', 'Hédzranawoé', 'Adidogomé']
            },
            {
                'username': 'koku_livraison',
                'first_name': 'Koku',
                'last_name': 'Mensah',
                'email': 'koku@example.com',
                'phone': '+228 92 55 66 77',
                'service_type': 'livraison',
                'description': 'Livraison rapide de repas et colis. Moto disponible 7j/7.',
                'experience_years': 2,
                'hourly_rate': 1000,
                'zones': ['Lomé Centre', 'Bè', 'Djidjolé']
            },
            {
                'username': 'edem_bricolage',
                'first_name': 'Edem',
                'last_name': 'Akakpo',
                'email': 'edem@example.com',
                'phone': '+228 92 77 88 99',
                'service_type': 'bricolage',
                'description': 'Électricien et plombier qualifié. Interventions rapides pour vos urgences.',
                'experience_years': 8,
                'hourly_rate': 3000,
                'zones': ['Lomé Centre', 'Agbalépédogan', 'Tokoin']
            },
            # Nouveaux prestataires Transport
            {
                'username': 'koffi_taxi',
                'first_name': 'Koffi',
                'last_name': 'Ahouansou',
                'email': 'koffi.taxi@example.com',
                'phone': '+228 92 12 34 56',
                'service_type': 'transport',
                'description': 'Service de taxi moto rapide et sécurisé. Casques fournis.',
                'experience_years': 4,
                'hourly_rate': 1800,
                'zones': ['Lomé Centre', 'Bè', 'Agoe', 'Kegue']
            },
            {
                'username': 'adjoa_vtc',
                'first_name': 'Adjoa',
                'last_name': 'Kpetonou',
                'email': 'adjoa.vtc@example.com',
                'phone': '+228 92 23 45 67',
                'service_type': 'transport',
                'description': 'Conductrice professionnelle VTC. Véhicule récent et climatisé.',
                'experience_years': 6,
                'hourly_rate': 2800,
                'zones': ['Lomé Centre', 'Tokoin', 'Adidogomé', 'Hédzranawoé']
            },
            # Nouveaux prestataires Livraison
            {
                'username': 'yao_delivery',
                'first_name': 'Yao',
                'last_name': 'Gbetoglo',
                'email': 'yao.delivery@example.com',
                'phone': '+228 92 34 56 78',
                'service_type': 'livraison',
                'description': 'Livraison express de repas et courses. Service 24h/24.',
                'experience_years': 3,
                'hourly_rate': 1200,
                'zones': ['Lomé Centre', 'Tokoin', 'Nyékonakpoé', 'Djidjolé']
            },
            {
                'username': 'akosua_courses',
                'first_name': 'Akosua',
                'last_name': 'Amegbor',
                'email': 'akosua.courses@example.com',
                'phone': '+228 92 45 67 89',
                'service_type': 'autre',
                'description': 'Spécialiste des courses alimentaires et pharmaceutiques.',
                'experience_years': 2,
                'hourly_rate': 800,
                'zones': ['Lomé Centre', 'Bè', 'Agbalépédogan']
            },
            # Nouveaux prestataires Ménage
            {
                'username': 'komla_clean',
                'first_name': 'Komla',
                'last_name': 'Attiogbe',
                'email': 'komla.clean@example.com',
                'phone': '+228 92 56 78 90',
                'service_type': 'menage',
                'description': 'Équipe de nettoyage professionnel pour bureaux et maisons.',
                'experience_years': 7,
                'hourly_rate': 1800,
                'zones': ['Lomé Centre', 'Tokoin', 'Agbalépédogan', 'Adidogomé']
            },
            {
                'username': 'efua_cleaning',
                'first_name': 'Efua',
                'last_name': 'Soglo',
                'email': 'efua.cleaning@example.com',
                'phone': '+228 92 67 89 01',
                'service_type': 'menage',
                'description': 'Nettoyage écologique avec produits naturels. Spécialiste vitres.',
                'experience_years': 4,
                'hourly_rate': 1600,
                'zones': ['Lomé Centre', 'Hédzranawoé', 'Nyékonakpoé']
            },
            # Nouveaux prestataires Bricolage
            {
                'username': 'kwame_elec',
                'first_name': 'Kwame',
                'last_name': 'Houssou',
                'email': 'kwame.elec@example.com',
                'phone': '+228 92 78 90 12',
                'service_type': 'bricolage',
                'description': 'Électricien certifié. Installation et dépannage électrique.',
                'experience_years': 10,
                'hourly_rate': 3500,
                'zones': ['Lomé Centre', 'Tokoin', 'Agbalépédogan', 'Bè']
            },
            {
                'username': 'abla_plombier',
                'first_name': 'Abla',
                'last_name': 'Koudadje',
                'email': 'abla.plombier@example.com',
                'phone': '+228 92 89 01 23',
                'service_type': 'bricolage',
                'description': 'Plombière experte. Réparation et installation sanitaire.',
                'experience_years': 6,
                'hourly_rate': 2800,
                'zones': ['Lomé Centre', 'Adidogomé', 'Hédzranawoé']
            },
            # Nouveaux services spécialisés
            {
                'username': 'kodjo_jardin',
                'first_name': 'Kodjo',
                'last_name': 'Adegnon',
                'email': 'kodjo.jardin@example.com',
                'phone': '+228 92 90 12 34',
                'service_type': 'autre',
                'description': 'Jardinier paysagiste. Entretien espaces verts et jardins.',
                'experience_years': 5,
                'hourly_rate': 2000,
                'zones': ['Lomé Centre', 'Tokoin', 'Adidogomé', 'Agbalépédogan']
            },
            {
                'username': 'afi_babysit',
                'first_name': 'Afi',
                'last_name': 'Kpogo',
                'email': 'afi.babysit@example.com',
                'phone': '+228 92 01 23 45',
                'service_type': 'autre',
                'description': 'Garde d\'enfants qualifiée. Diplômée en petite enfance.',
                'experience_years': 4,
                'hourly_rate': 1500,
                'zones': ['Lomé Centre', 'Hédzranawoé', 'Nyékonakpoé']
            },
            {
                'username': 'komi_tech',
                'first_name': 'Komi',
                'last_name': 'Assigbe',
                'email': 'komi.tech@example.com',
                'phone': '+228 92 12 34 67',
                'service_type': 'autre',
                'description': 'Technicien informatique. Réparation PC, téléphones, installations.',
                'experience_years': 8,
                'hourly_rate': 2500,
                'zones': ['Lomé Centre', 'Tokoin', 'Agbalépédogan', 'Bè']
            }
        ]
        
        for provider_data in providers_data:
            # Créer l'utilisateur
            user, created = User.objects.get_or_create(
                username=provider_data['username'],
                defaults={
                    'first_name': provider_data['first_name'],
                    'last_name': provider_data['last_name'],
                    'email': provider_data['email'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                
                # Mettre à jour le profil utilisateur
                user.profile.phone = provider_data['phone']
                user.profile.save()
                
                # Créer le profil prestataire
                provider = Provider.objects.create(
                    user=user,
                    service_type=provider_data['service_type'],
                    description=provider_data['description'],
                    experience_years=provider_data['experience_years'],
                    hourly_rate=provider_data['hourly_rate'],
                    status='approved',  # Approuvé directement
                    is_available=random.choice([True, True, True, False]),  # 75% disponibles
                    rating=round(random.uniform(4.0, 4.9), 1),
                    total_services=random.randint(10, 120)
                )
                
                # Créer les zones d'intervention
                for zone_name in provider_data['zones']:
                    ProviderZone.objects.create(
                        provider=provider,
                        city=zone_name
                    )
                
                self.stdout.write(f"Prestataire créé: {user.get_full_name()} ({provider.get_service_type_display()})")

    def create_services(self):
        """Créer des services spécifiques"""
        # Récupérer les prestataires et catégories
        providers = Provider.objects.filter(status='approved')
        categories = ServiceCategory.objects.all()
        
        services_data = [
            # Services Transport
            {
                'provider_username': 'kossi_transport',
                'category_name': 'Transport',
                'title': 'Transport VTC - Lomé Centre',
                'description': 'Service de transport privé dans Lomé avec véhicule climatisé 4 places.',
                'pricing_type': 'distance',
                'base_price': 500,
                'is_instant': True,
                'featured': True
            },
            {
                'provider_username': 'koffi_taxi',
                'category_name': 'Transport',
                'title': 'Taxi Moto Express',
                'description': 'Transport rapide en moto-taxi avec casque fourni.',
                'pricing_type': 'distance',
                'base_price': 300,
                'is_instant': True,
                'featured': True
            },
            {
                'provider_username': 'adjoa_vtc',
                'category_name': 'Transport',
                'title': 'VTC Femme Conductrice',
                'description': 'Service VTC avec conductrice professionnelle pour plus de confort.',
                'pricing_type': 'distance',
                'base_price': 600,
                'is_instant': True,
                'featured': False
            },
            
            # Services Livraison
            {
                'provider_username': 'koku_livraison',
                'category_name': 'Livraison de Repas',
                'title': 'Livraison Repas Express',
                'description': 'Livraison rapide de vos repas préférés en moins de 30 minutes.',
                'pricing_type': 'fixed',
                'base_price': 800,
                'is_instant': True,
                'featured': True
            },
            {
                'provider_username': 'yao_delivery',
                'category_name': 'Livraison de Repas',
                'title': 'Livraison 24h/24',
                'description': 'Service de livraison disponible jour et nuit.',
                'pricing_type': 'fixed',
                'base_price': 1000,
                'is_instant': True,
                'featured': False
            },
            {
                'provider_username': 'akosua_courses',
                'category_name': 'Courses',
                'title': 'Courses Alimentaires',
                'description': 'Je fais vos courses alimentaires et pharmaceutiques.',
                'pricing_type': 'hourly',
                'base_price': 800,
                'is_instant': False,
                'featured': False
            },
            
            # Services Ménage
            {
                'provider_username': 'ama_menage',
                'category_name': 'Ménage',
                'title': 'Nettoyage Résidentiel',
                'description': 'Nettoyage complet de votre domicile avec produits écologiques inclus.',
                'pricing_type': 'hourly',
                'base_price': 1500,
                'is_instant': False,
                'featured': True
            },
            {
                'provider_username': 'komla_clean',
                'category_name': 'Ménage',
                'title': 'Nettoyage Professionnel Bureau',
                'description': 'Équipe de nettoyage pour bureaux et espaces commerciaux.',
                'pricing_type': 'hourly',
                'base_price': 1800,
                'is_instant': False,
                'featured': False
            },
            {
                'provider_username': 'efua_cleaning',
                'category_name': 'Ménage',
                'title': 'Nettoyage Écologique',
                'description': 'Nettoyage avec produits 100% naturels et écologiques.',
                'pricing_type': 'hourly',
                'base_price': 1600,
                'is_instant': False,
                'featured': False
            },
            
            # Services Bricolage
            {
                'provider_username': 'edem_bricolage',
                'category_name': 'Bricolage',
                'title': 'Réparations Électriques & Plomberie',
                'description': 'Installation et réparation électrique et plomberie professionnelle.',
                'pricing_type': 'custom',
                'base_price': 5000,
                'is_instant': False,
                'featured': True
            },
            {
                'provider_username': 'kwame_elec',
                'category_name': 'Bricolage',
                'title': 'Installation Électrique',
                'description': 'Électricien certifié pour toutes installations électriques.',
                'pricing_type': 'hourly',
                'base_price': 3500,
                'is_instant': False,
                'featured': False
            },
            {
                'provider_username': 'abla_plombier',
                'category_name': 'Bricolage',
                'title': 'Plomberie Expert',
                'description': 'Réparation et installation de tous équipements sanitaires.',
                'pricing_type': 'hourly',
                'base_price': 2800,
                'is_instant': False,
                'featured': False
            },
            
            # Nouveaux services spécialisés
            {
                'provider_username': 'kodjo_jardin',
                'category_name': 'Jardinage',
                'title': 'Entretien Jardin & Paysage',
                'description': 'Création et entretien d\'espaces verts, taille, plantation.',
                'pricing_type': 'hourly',
                'base_price': 2000,
                'is_instant': False,
                'featured': True
            },
            {
                'provider_username': 'afi_babysit',
                'category_name': 'Garde d\'enfants',
                'title': 'Garde d\'Enfants Qualifiée',
                'description': 'Garde d\'enfants avec diplôme petite enfance. Expérience 4 ans.',
                'pricing_type': 'hourly',
                'base_price': 1500,
                'is_instant': False,
                'featured': True
            },
            {
                'provider_username': 'komi_tech',
                'category_name': 'Informatique',
                'title': 'Réparation & Maintenance IT',
                'description': 'Réparation ordinateurs, téléphones, installation logiciels.',
                'pricing_type': 'custom',
                'base_price': 4000,
                'is_instant': False,
                'featured': True
            },
        ]
        
        for service_data in services_data:
            # Trouver le prestataire et la catégorie
            try:
                provider = Provider.objects.get(user__username=service_data['provider_username'])
                category = categories.filter(name=service_data['category_name']).first()
                
                if provider and category:
                    service, created = Service.objects.get_or_create(
                        provider=provider,
                        title=service_data['title'],
                        defaults={
                            'category': category,
                            'description': service_data['description'],
                            'pricing_type': service_data['pricing_type'],
                            'base_price': service_data['base_price'],
                            'is_instant': service_data['is_instant'],
                            'featured': service_data['featured'],
                            'is_active': True,
                        }
                    )
                    if created:
                        self.stdout.write(f"Service créé: {service.title}")
            except Provider.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Prestataire {service_data['provider_username']} non trouvé"))

    def create_sample_orders(self):
        """Créer des commandes d'exemple"""
        clients = User.objects.filter(username__endswith='_client')
        services = Service.objects.filter(is_active=True)
        
        if clients.exists() and services.exists():
            # Créer plus de commandes pour une simulation réaliste
            for i in range(25):  # 25 commandes au lieu de 5
                client = random.choice(clients)
                service = random.choice(services)
                
                # Statuts possibles avec des probabilités réalistes
                status_choices = [
                    'pending', 'pending', 'pending',  # 3/10 en attente
                    'accepted', 'accepted',           # 2/10 acceptées
                    'in_progress',                    # 1/10 en cours
                    'completed', 'completed', 'completed', 'completed'  # 4/10 terminées
                ]
                status = random.choice(status_choices)
                
                # Prix variable selon le service
                base_price = service.base_price
                if service.pricing_type == 'hourly':
                    hours = random.uniform(1, 4)
                    estimated_price = base_price * Decimal(str(hours))
                elif service.pricing_type == 'distance':
                    distance = random.uniform(2, 15)
                    estimated_price = base_price * Decimal(str(distance))
                else:
                    estimated_price = base_price
                
                order = Order.objects.create(
                    customer=client,
                    service=service,
                    provider=service.provider,
                    description=f"Commande #{i+1} pour {service.title}",
                    status=status,
                    estimated_price=estimated_price,
                    final_price=estimated_price if status == 'completed' else None,
                    pickup_address="Lomé Centre, Togo" if service.category.name == 'Transport' else None,
                    delivery_address=f"{random.choice(['Tokoin', 'Bè', 'Adidogomé', 'Hédzranawoé'])}, Lomé, Togo" if service.category.name in ['Transport', 'Livraison de Repas'] else None,
                )
                
                # Mettre à jour les statistiques du client
                if status == 'completed':
                    client.profile.total_orders += 1
                    client.profile.total_spent += estimated_price
                    client.profile.save()
                
                # Mettre à jour les statistiques du prestataire
                if status == 'completed':
                    service.provider.total_services += 1
                    service.provider.save()
                
                self.stdout.write(f"Commande créée: {order.order_number} ({status})")
        
        # Afficher les statistiques finales
        self.stdout.write(self.style.SUCCESS(f"\n=== STATISTIQUES FINALES ==="))
        self.stdout.write(f"👥 Clients: {User.objects.filter(username__endswith='_client').count()}")
        self.stdout.write(f"🔧 Prestataires: {Provider.objects.filter(status='approved').count()}")
        self.stdout.write(f"📝 Services: {Service.objects.filter(is_active=True).count()}")
        self.stdout.write(f"📦 Commandes: {Order.objects.count()}")
        self.stdout.write(f"📊 Catégories: {ServiceCategory.objects.filter(is_active=True).count()}") 