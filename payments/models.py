from django.db import models
from django.contrib.auth.models import User
from orders.models import Order
from providers.models import Provider

class PaymentMethod(models.Model):
    """Méthodes de paiement disponibles"""
    PAYMENT_TYPES = [
        ('mobile_money', 'Mobile Money'),
        ('credit_card', 'Carte de crédit'),
        ('debit_card', 'Carte de débit'),
        ('bank_transfer', 'Virement bancaire'),
        ('cash', 'Espèces'),
    ]

    PROVIDERS = [
        ('tmoney', 'T-Money'),
        ('flooz', 'Flooz'),
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
    ]

    name = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    provider = models.CharField(max_length=20, choices=PROVIDERS)
    is_active = models.BooleanField(default=True)
    processing_fee_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    processing_fee_fixed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    icon = models.CharField(max_length=50, help_text="Font Awesome class")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserPaymentMethod(models.Model):
    """Méthodes de paiement enregistrées par les utilisateurs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100, help_text="Numéro de téléphone, carte, etc.")
    account_name = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'payment_method', 'account_number']

    def __str__(self):
        return f"{self.user.username} - {self.payment_method.name}"

class Transaction(models.Model):
    """Transactions financières"""
    TRANSACTION_TYPES = [
        ('payment', 'Paiement client'),
        ('commission', 'Commission plateforme'),
        ('payout', 'Paiement prestataire'),
        ('refund', 'Remboursement'),
        ('withdrawal', 'Retrait'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En cours'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('cancelled', 'Annulé'),
        ('refunded', 'Remboursé'),
    ]

    # Relations
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    # Transaction details
    transaction_id = models.CharField(max_length=100, unique=True, editable=False)
    external_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Montants
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    platform_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Métadonnées
    description = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    failure_reason = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.amount}€"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            import uuid
            self.transaction_id = f"TXN{uuid.uuid4().hex[:10].upper()}"
        
        # Calculer le montant net
        self.net_amount = self.amount - self.processing_fee - self.platform_commission
        super().save(*args, **kwargs)

class ProviderEarnings(models.Model):
    """Revenus des prestataires"""
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='earnings')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='provider_earnings')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='provider_earnings')
    
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_commission = models.DecimalField(max_digits=10, decimal_places=2)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Revenus {self.provider.user.username} - {self.net_amount}€"

class WithdrawalRequest(models.Model):
    """Demandes de retrait des prestataires"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
        ('completed', 'Complété'),
    ]

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='withdrawal_requests')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        return f"Retrait {self.provider.user.username} - {self.amount}€"
