from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    """Profil étendu pour les utilisateurs clients"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    phone_verification_code = models.CharField(max_length=6, blank=True, null=True)
    phone_verification_expires = models.DateTimeField(null=True, blank=True)
    
    # Profile info
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Homme'),
        ('female', 'Femme'),
        ('other', 'Autre')
    ], blank=True, null=True)
    
    # Location
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=50, default='Togo')
    
    # Current location (for real-time services)
    current_latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    location_updated_at = models.DateTimeField(null=True, blank=True)
    
    # Preferences
    preferred_language = models.CharField(max_length=10, choices=[
        ('fr', 'Français'),
        ('en', 'English'),
        ('ee', 'Ewé')
    ], default='fr')
    preferred_currency = models.CharField(max_length=5, default='XOF')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    
    # Account status
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    premium_expires = models.DateTimeField(null=True, blank=True)
    
    # Social auth
    google_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Statistics
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_rating_given = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

    @property
    def is_location_available(self):
        return self.current_latitude and self.current_longitude

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Créer automatiquement un profil utilisateur quand un utilisateur est créé"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarder le profil utilisateur"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

class UserAddress(models.Model):
    """Adresses favorites des utilisateurs"""
    ADDRESS_TYPES = [
        ('home', 'Domicile'),
        ('work', 'Bureau'),
        ('other', 'Autre'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='other')
    name = models.CharField(max_length=100)  # ex: "Maison", "Bureau"
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "User addresses"

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Notification(models.Model):
    """Système de notifications"""
    NOTIFICATION_TYPES = [
        ('order_status', 'Statut commande'),
        ('payment', 'Paiement'),
        ('message', 'Message'),
        ('promotion', 'Promotion'),
        ('system', 'Système'),
        ('reminder', 'Rappel'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # Related objects
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_sent_email = models.BooleanField(default=False)
    is_sent_sms = models.BooleanField(default=False)
    is_sent_push = models.BooleanField(default=False)
    
    # Scheduling
    send_at = models.DateTimeField(null=True, blank=True, help_text="Programmer l'envoi")
    
    # Metadata
    data = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class UserSession(models.Model):
    """Sessions utilisateur pour le suivi"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    device_type = models.CharField(max_length=20, choices=[
        ('web', 'Web'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablette'),
        ('desktop', 'Desktop')
    ], default='web')
    device_info = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    location_city = models.CharField(max_length=100, blank=True, null=True)
    location_country = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_activity']

    def __str__(self):
        return f"Session {self.user.username} - {self.device_type}"

class Chat(models.Model):
    """Chat entre utilisateurs et prestataires"""
    CHAT_TYPES = [
        ('order', 'Commande'),
        ('support', 'Support'),
        ('general', 'Général'),
    ]

    # Participants
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_chats')
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, related_name='provider_chats')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='chats', null=True, blank=True)
    
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPES, default='order')
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_message_at']

    def __str__(self):
        return f"Chat {self.customer.username} - {self.provider.user.username}"

class ChatMessage(models.Model):
    """Messages dans les chats"""
    MESSAGE_TYPES = [
        ('text', 'Texte'),
        ('image', 'Image'),
        ('location', 'Localisation'),
        ('system', 'Système'),
    ]

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    content = models.TextField(blank=True, null=True)
    
    # For images and files
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True)
    
    # For location messages
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Message status
    is_read = models.BooleanField(default=False)
    is_system = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message de {self.sender.username} dans {self.chat}"
