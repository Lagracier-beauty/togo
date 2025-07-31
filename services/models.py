from django.db import models
from django.contrib.auth.models import User
from providers.models import Provider

class ServiceCategory(models.Model):
    """Catégories de services (Livraison, Transport, Ménage, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, help_text="Font Awesome class")
    color = models.CharField(max_length=7, default="#007bff", help_text="Couleur hex")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Service categories"

    def __str__(self):
        return self.name

class Service(models.Model):
    """Services spécifiques proposés par les prestataires"""
    PRICING_TYPES = [
        ('fixed', 'Prix fixe'),
        ('hourly', 'Tarif horaire'),
        ('distance', 'Prix au kilomètre'),
        ('custom', 'Devis personnalisé'),
    ]

    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    pricing_type = models.CharField(max_length=20, choices=PRICING_TYPES)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, help_text="Durée estimée en minutes")
    is_instant = models.BooleanField(default=False, help_text="Service instantané disponible")
    is_bookable = models.BooleanField(default=True, help_text="Service réservable à l'avance")
    max_advance_days = models.PositiveIntegerField(default=30, help_text="Jours max de réservation à l'avance")
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, help_text="Service mis en avant")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', 'title']

    def __str__(self):
        return f"{self.title} - {self.provider.user.get_full_name()}"

    @property
    def average_rating(self):
        """Calcule la note moyenne basée sur les évaluations des commandes"""
        ratings = self.orders.filter(rating__customer_rating__isnull=False).values_list('rating__customer_rating', flat=True)
        if ratings:
            return sum(ratings) / len(ratings)
        return 0

    @property
    def total_reviews(self):
        """Compte le nombre total d'avis clients"""
        return self.orders.filter(rating__customer_rating__isnull=False).count()

class ServiceImage(models.Model):
    """Images des services"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='service_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image de {self.service.title}"

class ServiceAvailability(models.Model):
    """Disponibilité des services par jour de la semaine"""
    WEEKDAYS = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='availability')
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['service', 'weekday']

    def __str__(self):
        return f"{self.service.title} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"
