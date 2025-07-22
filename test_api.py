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

def test_register_fail_email_exists():
    """Test d'échec d'inscription avec email déjà utilisé"""
    print("\n=== Test d'inscription avec email déjà utilisé ===")
    url = f"{API_BASE}/auth/register/"
    data = {
        "username": "testuserexists",
        "email": "testuserexists@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test123456",
        "password_confirm": "test123456",
        "phone": "+22890123456"
    }
    headers = {"Content-Type": "application/json"}
    # Première inscription (doit réussir)
    requests.post(url, json=data, headers=headers)
    # Deuxième inscription (doit échouer)
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 400, "L'inscription avec un email déjà utilisé devrait échouer."

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

def test_login_fail_bad_password():
    """Test d'échec de connexion avec mauvais mot de passe"""
    print("\n=== Test de connexion avec mauvais mot de passe ===")
    url = f"{API_BASE}/auth/login/"
    data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 400, "La connexion avec un mauvais mot de passe devrait échouer."

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

def test_change_password(token):
    """Test du changement de mot de passe"""
    print("\n=== Test du changement de mot de passe ===")
    url = f"{API_BASE}/auth/change-password/"
    data = {
        "old_password": "test123456",
        "new_password": "newpass123456",
        "new_password_confirm": "newpass123456"
    }
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Le changement de mot de passe devrait réussir."
    # Vérifier qu'on peut se connecter avec le nouveau mot de passe
    login_data = {"username": "testuser", "password": "newpass123456"}
    login_resp = requests.post(f"{API_BASE}/auth/login/", json=login_data, headers={"Content-Type": "application/json"})
    print(f"Login with new password status: {login_resp.status_code}")
    assert login_resp.status_code == 200, "Connexion avec le nouveau mot de passe devrait réussir."

def test_logout(token):
    """Test de la déconnexion"""
    print("\n=== Test de déconnexion ===")
    url = f"{API_BASE}/auth/logout/"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "La déconnexion devrait réussir."

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
        
        # Test 6: Changement de mot de passe
        test_change_password(token)
        
        # Test 7: Déconnexion
        test_logout(token)
        
        print("\n🎉 Tests terminés avec succès!")
    else:
        print("\n❌ Impossible d'obtenir un token. Vérifiez que le serveur Django fonctionne.")
    
    # Tests d'échec
    test_register_fail_email_exists()
    test_login_fail_bad_password()

if __name__ == "__main__":
    main() 