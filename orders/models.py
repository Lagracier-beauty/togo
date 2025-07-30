from django.db import models
from django.contrib.auth.models import User
from services.models import Service
from providers.models import Provider

class Order(models.Model):
    """Commandes/Réservations de services"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('rejected', 'Rejeté'),
        ('in_progress', 'En cours'),
        ('on_route', 'En route'),
        ('arrived', 'Arrivé'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
        ('disputed', 'Litige'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Normale'),
        ('medium', 'Urgente'),
        ('high', 'Très urgente'),
    ]

    # Relations
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='orders')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='received_orders')

    # Informations de commande
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    
    # Description et besoins
    description = models.TextField(help_text="Description détaillée du besoin")
    special_instructions = models.TextField(blank=True, null=True)
    
    # Localisation
    pickup_address = models.TextField(null=True, blank=True)
    pickup_latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    pickup_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    delivery_address = models.TextField(null=True, blank=True)
    delivery_latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    delivery_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Planification
    scheduled_datetime = models.DateTimeField(null=True, blank=True, help_text="Quand le service doit être effectué")
    estimated_duration = models.PositiveIntegerField(null=True, blank=True, help_text="Durée estimée en minutes")
    
    # Tarification
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    additional_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Métadonnées
    customer_notes = models.TextField(blank=True, null=True)
    provider_notes = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande {self.order_number} - {self.service.title}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Générer un numéro de commande unique
            import uuid
            self.order_number = f"TOG{uuid.uuid4().hex[:8].upper()}"
        
        # Calculer le prix total
        if self.final_price:
            self.total_amount = self.final_price + self.additional_fees
        else:
            self.total_amount = self.estimated_price + self.additional_fees
            
        super().save(*args, **kwargs)

class OrderTracking(models.Model):
    """Suivi en temps réel des commandes"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking')
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    message = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Suivi {self.order.order_number} - {self.get_status_display()}"

class OrderImage(models.Model):
    """Images liées aux commandes (avant/après, problèmes, etc.)"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='order_images/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_before = models.BooleanField(default=True, help_text="Photo avant/après le service")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.order.order_number}"

class OrderRating(models.Model):
    """Évaluations des commandes"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='rating')
    customer_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    customer_comment = models.TextField(blank=True, null=True)
    provider_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    provider_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Évaluation {self.order.order_number}"
