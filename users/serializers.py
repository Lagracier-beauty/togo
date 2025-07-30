from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile, UserAddress

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil utilisateur"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'is_verified', 'created_at', 'updated_at']

class UserAddressSerializer(serializers.ModelSerializer):
    """Serializer pour les adresses utilisateur"""
    class Meta:
        model = UserAddress
        fields = ['id', 'name', 'address', 'city', 'is_default', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    """Serializer pour l'utilisateur avec profil"""
    profile = UserProfileSerializer(read_only=True)
    addresses = UserAddressSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'addresses']
        read_only_fields = ['id']

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription utilisateur"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'phone']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        password_confirm = validated_data.pop('password_confirm')
        phone = validated_data.pop('phone', None)
        
        user = User.objects.create_user(**validated_data)
        
        # Mettre à jour le profil avec le téléphone
        if phone:
            user.profile.phone = phone
            user.profile.save()
        
        return user

class LoginSerializer(serializers.Serializer):
    """Serializer pour la connexion"""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Identifiants invalides.')
            if not user.is_active:
                raise serializers.ValidationError('Compte désactivé.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Nom d\'utilisateur et mot de passe requis.')
        
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour changer le mot de passe"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value

class UpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour le profil"""
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'first_name', 'last_name', 'email']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        
        # Mettre à jour les données utilisateur
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        
        # Mettre à jour le profil
        return super().update(instance, validated_data) 