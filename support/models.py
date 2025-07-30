from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

class FAQ(models.Model):
    """Foire aux questions"""
    CATEGORIES = [
        ('general', 'Questions générales'),
        ('account', 'Compte utilisateur'),
        ('orders', 'Commandes'),
        ('payments', 'Paiements'),
        ('providers', 'Prestataires'),
        ('technical', 'Problèmes techniques'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORIES)
    question = models.TextField()
    answer = models.TextField()
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-is_featured', 'question']
        verbose_name_plural = "FAQs"

    def __str__(self):
        return f"{self.get_category_display()} - {self.question[:50]}..."

class SupportTicket(models.Model):
    """Tickets de support client"""
    PRIORITIES = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    ]

    STATUS_CHOICES = [
        ('open', 'Ouvert'),
        ('in_progress', 'En cours'),
        ('waiting_user', 'En attente utilisateur'),
        ('waiting_provider', 'En attente prestataire'),
        ('resolved', 'Résolu'),
        ('closed', 'Fermé'),
    ]

    CATEGORIES = [
        ('general', 'Question générale'),
        ('account', 'Problème de compte'),
        ('order', 'Problème de commande'),
        ('payment', 'Problème de paiement'),
        ('provider', 'Problème avec prestataire'),
        ('technical', 'Problème technique'),
        ('dispute', 'Litige'),
        ('other', 'Autre'),
    ]

    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='support_tickets', null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')

    # Ticket info
    ticket_number = models.CharField(max_length=20, unique=True, editable=False)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    priority = models.CharField(max_length=10, choices=PRIORITIES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    # Satisfaction
    satisfaction_rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)], 
        null=True, blank=True,
        help_text="Note de satisfaction (1-5)"
    )
    satisfaction_comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket {self.ticket_number} - {self.subject}"

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            import uuid
            self.ticket_number = f"SUP{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class SupportMessage(models.Model):
    """Messages dans les tickets de support"""
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_internal = models.BooleanField(default=False, help_text="Message interne (non visible par l'utilisateur)")
    is_system = models.BooleanField(default=False, help_text="Message automatique du système")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message {self.ticket.ticket_number} - {self.sender.username}"

class SupportAttachment(models.Model):
    """Pièces jointes aux tickets de support"""
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='attachments')
    message = models.ForeignKey(SupportMessage, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    file = models.FileField(upload_to='support_attachments/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(help_text="Taille du fichier en bytes")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pièce jointe {self.filename} - {self.ticket.ticket_number}"

class Dispute(models.Model):
    """Litiges entre clients et prestataires"""
    DISPUTE_TYPES = [
        ('service_quality', 'Qualité du service'),
        ('no_show', 'Prestataire absent'),
        ('payment', 'Problème de paiement'),
        ('pricing', 'Désaccord sur le prix'),
        ('damage', 'Dommages'),
        ('behavior', 'Comportement inapproprié'),
        ('other', 'Autre'),
    ]

    STATUS_CHOICES = [
        ('open', 'Ouvert'),
        ('investigating', 'En cours d\'enquête'),
        ('mediation', 'En médiation'),
        ('resolved', 'Résolu'),
        ('closed', 'Fermé'),
    ]

    RESOLUTIONS = [
        ('refund_full', 'Remboursement intégral'),
        ('refund_partial', 'Remboursement partiel'),
        ('service_redo', 'Refaire le service'),
        ('provider_warning', 'Avertissement prestataire'),
        ('provider_suspension', 'Suspension prestataire'),
        ('no_action', 'Aucune action'),
        ('other', 'Autre résolution'),
    ]

    # Relations
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='dispute')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_disputes')
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, related_name='provider_disputes')
    mediator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mediated_disputes')

    # Dispute details
    dispute_type = models.CharField(max_length=20, choices=DISPUTE_TYPES)
    customer_description = models.TextField(help_text="Description du problème par le client")
    provider_response = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    resolution = models.CharField(max_length=20, choices=RESOLUTIONS, blank=True, null=True)
    resolution_notes = models.TextField(blank=True, null=True)

    # Financial
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    compensation_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Litige {self.order.order_number} - {self.get_dispute_type_display()}"
