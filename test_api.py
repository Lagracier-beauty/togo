#!/usr/bin/env python3
"""
Script de test pour les APIs REST de Tog-Services
"""
import requests
import json
import time

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api"

def test_register():
    """Test de l'inscription"""
    print("=== Test d'inscription ===")
    
    # Utiliser un timestamp pour un nom unique
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    
    url = f"{API_BASE}/auth/register/"
    data = {
        "username": username,
        "email": f"{username}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test123456",
        "password_confirm": "test123456",
        "phone": "+22890123456"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            return response.json().get('token')
        return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def test_login():
    """Test de la connexion"""
    print("\n=== Test de connexion ===")
    
    url = f"{API_BASE}/auth/login/"
    data = {
        "username": "testuser",
        "password": "test123456"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            return response.json().get('token')
        return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def test_profile(token):
    """Test du profil utilisateur"""
    print("\n=== Test du profil utilisateur ===")
    
    url = f"{API_BASE}/profile/"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Erreur: {e}")

def test_orders(token):
    """Test des commandes"""
    print("\n=== Test des commandes ===")
    
    url = f"{API_BASE}/orders/"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Erreur: {e}")

def test_stats(token):
    """Test des statistiques"""
    print("\n=== Test des statistiques ===")
    
    url = f"{API_BASE}/stats/"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Erreur: {e}")

def main():
    """Fonction principale de test"""
    print("🚀 Test des APIs REST de Tog-Services")
    print("=" * 50)
    
    # Test 1: Inscription
    token = test_register()
    
    if not token:
        # Test 2: Connexion (si l'inscription échoue)
        token = test_login()
    
    if token:
        print(f"\n✅ Token obtenu: {token[:20]}...")
        
        # Test 3: Profil
        test_profile(token)
        
        # Test 4: Commandes
        test_orders(token)
        
        # Test 5: Statistiques
        test_stats(token)
        
        print("\n🎉 Tests terminés avec succès!")
    else:
        print("\n❌ Impossible d'obtenir un token. Vérifiez que le serveur Django fonctionne.")

if __name__ == "__main__":
    main() 