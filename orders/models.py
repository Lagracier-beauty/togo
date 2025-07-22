from django.db import models
from django.contrib.auth.models import User
from providers.models import Provider

class Order(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    SERVICE_CHOICES = [
        ('livraison', 'Livraison'),
        ('courses', 'Courses & Livraison'),
        ('transport', 'Transport'),
        ('menage', 'Ménage'),
        ('bricolage', 'Bricolage'),
        ('autre', 'Autre'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='orders')
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.TextField(blank=True, null=True)
    scheduled_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Commande {self.id} - {self.user.username} -> {self.provider.user.username} ({self.get_service_type_display()})"
