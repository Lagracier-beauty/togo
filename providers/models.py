from django.db import models
from django.contrib.auth.models import User

class Provider(models.Model):
    """Modèle pour les prestataires de services"""
    SERVICE_TYPES = [
        ('livraison', 'Livraison'),
        ('transport', 'Transport'),
        ('menage', 'Ménage'),
        ('bricolage', 'Bricolage'),
        ('autre', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
        ('suspended', 'Suspendu'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_services = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_service_type_display()}"

class ProviderDocument(models.Model):
    """Documents justificatifs des prestataires"""
    DOCUMENT_TYPES = [
        ('cni', 'Carte Nationale d\'Identité'),
        ('passport', 'Passeport'),
        ('license', 'Permis de conduire'),
        ('certificate', 'Certificat de formation'),
        ('other', 'Autre'),
    ]

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='provider_documents/')
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider.user.username} - {self.get_document_type_display()}"

class ProviderZone(models.Model):
    """Zones d'intervention des prestataires"""
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='zones')
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider.user.username} - {self.city}"
