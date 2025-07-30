from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer, 
    UpdateProfileSerializer, ChangePasswordSerializer, UserAddressSerializer
)
from .models import UserProfile, UserAddress

class RegisterAPIView(APIView):
    """API pour l'inscription d'un nouvel utilisateur"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'success': True,
                'message': 'Inscription réussie !',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    """API pour la connexion utilisateur"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'success': True,
                'message': 'Connexion réussie !',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    """API pour la déconnexion"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            # Supprimer le token
            request.user.auth_token.delete()
        except:
            pass
        
        logout(request)
        
        return Response({
            'success': True,
            'message': 'Déconnexion réussie !'
        }, status=status.HTTP_200_OK)

class UserProfileAPIView(APIView):
    """API pour gérer le profil utilisateur"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Récupérer le profil de l'utilisateur connecté"""
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def put(self, request):
        """Mettre à jour le profil utilisateur"""
        serializer = UpdateProfileSerializer(request.user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Profil mis à jour avec succès !',
                'data': UserSerializer(request.user).data
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(APIView):
    """API pour changer le mot de passe"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Supprimer l'ancien token et en créer un nouveau
            user.auth_token.delete()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'success': True,
                'message': 'Mot de passe changé avec succès !',
                'token': token.key
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserAddressListAPIView(generics.ListCreateAPIView):
    """API pour gérer les adresses de l'utilisateur"""
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

class UserAddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API pour gérer une adresse spécifique"""
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

class UserOrdersAPIView(APIView):
    """API pour récupérer les commandes de l'utilisateur"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Pour l'instant, retourner des données fictives
        # Plus tard, nous connecterons avec le modèle Order
        orders = [
            {
                'id': 1,
                'service': 'Livraison de repas',
                'provider': 'Kossi A.',
                'date': '2024-07-03',
                'status': 'Terminé',
                'price': '2,500 FCFA'
            },
            {
                'id': 2,
                'service': 'Transport',
                'provider': 'Yawovi K.',
                'date': '2024-07-01',
                'status': 'En cours',
                'price': '1,500 FCFA'
            }
        ]
        
        return Response({
            'success': True,
            'data': orders
        })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """API pour les statistiques de l'utilisateur"""
    user = request.user
    
    # Statistiques fictives pour l'instant
    stats = {
        'total_orders': 15,
        'completed_orders': 12,
        'pending_orders': 2,
        'cancelled_orders': 1,
        'total_spent': '45,000 FCFA',
        'average_rating': 4.8
    }
    
    return Response({
        'success': True,
        'data': stats
    }) 