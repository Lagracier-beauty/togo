# 📝 TODO - Complétion de l’application Tog-Services

## 1. Modélisation des données

- [x] **User & Profile**
  - Modèle `UserProfile` (étendu)
  - Modèle `UserAddress`
- [x] **Provider**
  - Modèle `Provider` (prestataire)
  - Modèle `ProviderDocument` (justificatifs)
  - Modèle `ProviderZone` (zones d’intervention)
- [ ] **Service**
  - **À faire** : Créer un modèle `Service` (catégorie, description, prix, etc.)
- [ ] **Order**
  - **À faire** : Créer un modèle `Order` (commande, statut, user, provider, service, prix, date, etc.)
- [ ] **Payment**
  - **À faire** : Créer un modèle `Payment` (commande, montant, statut, méthode, date, etc.)
- [ ] **Support**
  - **À faire** : Créer un modèle pour les tickets/support/FAQ si besoin
- [ ] **Dashboard**
  - **À faire** : Créer des modèles pour les statistiques/rapports si besoin

---

## 2. APIs REST

- [x] **User**
  - Authentification (login, register, logout, change-password)
  - Profil utilisateur (GET/PUT)
  - Adresses utilisateur (CRUD)
  - Statistiques utilisateur (fictif)
  - Commandes utilisateur (fictif)
- [ ] **Provider**
  - [ ] Enregistrement prestataire (POST) – **à implémenter**
  - [ ] Profil prestataire (GET/PUT) – **à implémenter**
  - [ ] Commandes prestataire (GET) – **à implémenter**
  - [ ] Liste des prestataires (GET) – **à implémenter**
- [ ] **Service**
  - [ ] Liste des services (GET) – **à implémenter**
  - [ ] Détail d’un service (GET) – **à implémenter**
  - [ ] Création/modification/suppression de service (si admin/provider) – **à implémenter**
- [ ] **Order**
  - [ ] Création de commande (POST) – **à implémenter**
  - [ ] Suivi/gestion des commandes (GET/PUT) – **à implémenter**
- [ ] **Payment**
  - [ ] Paiement d’une commande (POST) – **à implémenter**
  - [ ] Historique des paiements (GET) – **à implémenter**
- [ ] **Support**
  - [ ] FAQ (GET) – **à implémenter**
  - [ ] Contact/support (POST) – **à implémenter**

---

## 3. Vues Web (Django)

- [x] **Pages principales**
  - Accueil, login, inscription, dashboard utilisateur, profil, commandes, recherche de services
- [x] **Prestataire**
  - Inscription, dashboard, profil, commandes, liste des prestataires
- [x] **Admin**
  - Dashboard admin (statistiques fictives)
- [x] **Support**
  - Page support/FAQ
- [ ] **Services**
  - [ ] Affichage dynamique des services depuis la base (actuellement statique)
- [ ] **Commandes**
  - [ ] Création et gestion des commandes côté utilisateur et prestataire
- [ ] **Paiement**
  - [ ] Intégration du paiement (Mobile Money, carte, etc.)
- [ ] **Notifications**
  - [ ] Système de notifications (email, in-app, etc.)

---

## 4. Divers

- [ ] **Tests unitaires et d’intégration**
  - Couvrir les APIs, modèles, vues principales
- [ ] **Sécurité**
  - Validation des permissions (accès API, dashboard, etc.)
  - Sécurisation des endpoints sensibles
- [ ] **UX/UI**
  - Améliorer les formulaires, feedback utilisateur, responsive, etc.
- [ ] **Déploiement**
  - Préparer la configuration pour la production (ALLOWED_HOSTS, DEBUG, etc.)

---

## 5. Suggestions d’extensions

- [ ] **Avis & Notations**
  - Permettre aux utilisateurs de noter les prestataires/services
- [ ] **Gestion des disponibilités**
  - Calendrier de disponibilité pour les prestataires
- [ ] **Multi-langue**
  - Ajouter l’anglais en plus du français

---

**Résumé des manques critiques :**
- Les modèles de base pour Service, Order, Payment, Support, Dashboard sont absents.
- Les APIs REST pour services, commandes, paiements, support sont à implémenter.
- Les vues web affichent des données statiques ou fictives, il faut les connecter à la base.
- Les tests, la sécurité et l’UX sont à renforcer. 