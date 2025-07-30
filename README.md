# 🚀 Tog-Services - Plateforme de Services à la Demande

![Tog-Services Banner](static/images/banner.png)

## 📋 Description

**Tog-Services** est une plateforme web moderne de services à la demande spécialement conçue pour le marché togolais. Elle permet de mettre en relation les utilisateurs ayant des besoins en services quotidiens avec des prestataires locaux qualifiés et évalués.

### 🌟 Fonctionnalités Principales

#### Pour les Clients
- ✅ **Inscription simplifiée** avec vérification SMS OTP
- 🔍 **Recherche avancée** de services avec filtres géographiques
- 📍 **Géolocalisation** pour trouver les prestataires proches
- 💬 **Chat en temps réel** avec les prestataires
- 📱 **Suivi GPS** des commandes en cours
- 💳 **Paiements sécurisés** (Mobile Money, cartes bancaires)
- ⭐ **Système de notation** et d'évaluation
- 🏠 **Gestion des adresses** favorites

#### Pour les Prestataires
- 📝 **Inscription avec validation** de documents
- 📊 **Tableau de bord** avec statistiques et revenus
- 🗓️ **Gestion des disponibilités** et zones d'intervention
- 💰 **Système de retrait** vers Mobile Money
- 📈 **Suivi des performances** et évaluations clients
- 🎯 **Réception de demandes** ciblées

#### Pour les Administrateurs
- 🛠️ **Interface d'administration** complète
- 👥 **Gestion des utilisateurs** et prestataires
- 💼 **Validation des prestataires** et documents
- 💳 **Gestion des transactions** et commissions
- 📊 **Statistiques détaillées** et rapports
- 🎫 **Système de support** et litiges

### 🎨 Design et UX

- 🌓 **Mode sombre/clair** automatique
- 📱 **Design responsive** pour tous les appareils
- ⚡ **Animations fluides** et interactions modernes
- 🎭 **Interface intuitive** et ergonomique
- 🚀 **Performance optimisée** avec chargement rapide

## 🏗️ Architecture Technique

### Technologies Utilisées

#### Backend
- **Django 5.2** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de données (production)
- **SQLite** - Base de données (développement)
- **Redis** - Cache et sessions
- **Celery** - Tâches asynchrones

#### Frontend
- **HTML5/CSS3** avec variables CSS personnalisées
- **Bootstrap 5.3** - Framework CSS responsive
- **JavaScript ES6+** - Interactivité moderne
- **Font Awesome 6** - Icônes
- **Google Fonts (Inter)** - Typographie

#### Intégrations
- **APIs de géolocalisation** (Google Maps)
- **Passerelles de paiement** Mobile Money (T-Money, Flooz)
- **SMS Gateway** pour vérifications OTP
- **Services de stockage** cloud pour fichiers

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- Node.js 16+ (pour les outils de développement)
- Redis Server
- PostgreSQL (pour la production)

### Installation Locale

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/tog-services.git
cd tog-services
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration de l'environnement**
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env avec vos configurations
nano .env
```

5. **Configurer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Charger les données de test (optionnel)**
```bash
python manage.py loaddata fixtures/initial_data.json
```

7. **Démarrer le serveur de développement**
```bash
python manage.py runserver
```

8. **Démarrer Redis (dans un autre terminal)**
```bash
redis-server
```

9. **Démarrer Celery (dans un autre terminal)**
```bash
celery -A togo_service worker --loglevel=info
```

### Variables d'Environnement

Créez un fichier `.env` avec les variables suivantes :

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données
DATABASE_URL=postgres://username:password@localhost:5432/tog_services

# Redis
REDIS_URL=redis://localhost:6379/0

# APIs Externes
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
TMONEY_API_KEY=your-tmoney-api-key
FLOOZ_API_KEY=your-flooz-api-key

# SMS
SMS_API_KEY=your-sms-api-key
SMS_SENDER_ID=TOG-SERVICES

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Stockage Cloud
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=tog-services-media
```

## 📊 Structure du Projet

```
tog-services/
├── 📁 dashboard/          # Interface administrateur
├── 📁 orders/             # Gestion des commandes
├── 📁 payments/           # Système de paiement
├── 📁 providers/          # Gestion des prestataires
├── 📁 services/           # Catalogue de services
├── 📁 support/            # Support client et litiges
├── 📁 users/              # Gestion des utilisateurs
├── 📁 static/             # Fichiers statiques (CSS, JS, images)
├── 📁 templates/          # Templates HTML
├── 📁 media/              # Fichiers uploadés
├── 📁 togo_service/       # Configuration Django
├── requirements.txt       # Dépendances Python
└── manage.py             # Script de gestion Django
```

## 🔧 Configuration Avancée

### Configuration de Production

1. **Variables d'environnement de production**
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgres://username:password@db-host:5432/tog_services_prod
```

2. **Collecte des fichiers statiques**
```bash
python manage.py collectstatic --noinput
```

3. **Déploiement avec Gunicorn**
```bash
gunicorn togo_service.wsgi:application --bind 0.0.0.0:8000
```

### Configuration SSL et Sécurité

Ajoutez ces paramètres pour la production :

```python
# settings.py
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📱 API REST

L'API REST est accessible à `/api/` avec les endpoints suivants :

### Authentification
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/register/` - Inscription
- `POST /api/auth/refresh/` - Actualiser le token

### Utilisateurs
- `GET /api/users/profile/` - Profil utilisateur
- `PUT /api/users/profile/` - Mettre à jour le profil
- `GET /api/users/addresses/` - Adresses favorites

### Services
- `GET /api/services/` - Liste des services
- `GET /api/services/{id}/` - Détail d'un service
- `GET /api/services/categories/` - Catégories de services

### Commandes
- `POST /api/orders/` - Créer une commande
- `GET /api/orders/` - Mes commandes
- `GET /api/orders/{id}/` - Détail d'une commande
- `PUT /api/orders/{id}/status/` - Mettre à jour le statut

### Documentation complète de l'API
Accédez à `/api/docs/` pour la documentation interactive Swagger.

## 🧪 Tests

### Exécuter les tests
```bash
# Tous les tests
python manage.py test

# Tests d'une application spécifique
python manage.py test users

# Tests avec couverture
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Tests d'intégration
```bash
# Tests de l'API
python manage.py test api.tests

# Tests d'interface
python manage.py test functional_tests
```

## 🚀 Déploiement

### Déploiement Docker

1. **Construire l'image**
```bash
docker build -t tog-services .
```

2. **Démarrer avec Docker Compose**
```bash
docker-compose up -d
```

### Déploiement Heroku

1. **Préparer pour Heroku**
```bash
heroku create tog-services-app
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
```

2. **Déployer**
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 📈 Monitoring et Performance

### Monitoring
- **Logs** : Django logging configuré
- **Métriques** : Intégration Sentry pour le monitoring d'erreurs
- **Performance** : WhiteNoise pour les fichiers statiques

### Optimisations
- **Cache Redis** pour les sessions et données fréquentes
- **Compression** des fichiers CSS/JS
- **CDN** pour les médias (AWS CloudFront)
- **Pagination** des listes longues

## 🤝 Contribution

### Guide de Contribution

1. **Fork** le repository
2. **Créer** une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Committer** vos changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. **Pousser** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. **Créer** une Pull Request

### Standards de Code

- **PEP 8** pour Python
- **ESLint** pour JavaScript
- **Tests unitaires** obligatoires pour nouvelles fonctionnalités
- **Documentation** mise à jour

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

### Contact
- **Email** : support@tog-services.tg
- **Téléphone** : +228 XX XX XX XX
- **Documentation** : [docs.tog-services.tg](https://docs.tog-services.tg)

### Issues
Pour signaler un bug ou demander une fonctionnalité, créez une [issue sur GitHub](https://github.com/votre-username/tog-services/issues).

---

## 🎯 Roadmap

### Version 1.1 (Q2 2024)
- [ ] Application mobile iOS/Android
- [ ] Notifications push
- [ ] Chat vidéo intégré
- [ ] Système de parrainage

### Version 1.2 (Q3 2024)
- [ ] Multi-langues (Français, Anglais, Ewé)
- [ ] Analytics avancées
- [ ] API webhook pour intégrations
- [ ] Mode hors-ligne

### Version 2.0 (Q4 2024)
- [ ] Intelligence artificielle pour recommandations
- [ ] Blockchain pour transparence des transactions
- [ ] Expansion régionale (Afrique de l'Ouest)

---

**Développé avec ❤️ pour le Togo et l'Afrique** 🇹🇬

*Ensemble, révolutionnons l'accès aux services quotidiens !* 