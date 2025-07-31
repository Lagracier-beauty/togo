from django import forms
from django.contrib.auth.models import User
from .models import Provider, ProviderDocument, ProviderZone

class ProviderRegistrationForm(forms.ModelForm):
    """Formulaire d'inscription prestataire"""
    # Champs utilisateur de base
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True)
    
    # Zones d'intervention
    zones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Listez les quartiers ou zones où vous intervenez (séparés par des virgules)",
        required=True
    )
    
    # Acceptation des conditions
    accept_terms = forms.BooleanField(required=True)

    class Meta:
        model = Provider
        fields = [
            'service_type', 'description', 'experience_years', 'hourly_rate', 'zones'
        ]
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': 0}),
            'zones': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Styling des champs utilisateur
        self.fields['first_name'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Prénom'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Nom de famille'})
        self.fields['email'].widget.attrs.update({'class': 'form-input', 'placeholder': 'votre@email.com'})
        self.fields['phone'].widget.attrs.update({'class': 'form-input', 'placeholder': '+228 XX XX XX XX'})
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Nom d\'utilisateur'})
        self.fields['password'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Mot de passe'})
        self.fields['password_confirm'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirmer le mot de passe'})
        self.fields['accept_terms'].widget.attrs.update({'class': 'form-checkbox'})

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        
        return password_confirm

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur existe déjà.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def save(self, commit=True):
        if commit:
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            
            # Mettre à jour le profil utilisateur
            user.profile.phone = self.cleaned_data['phone']
            user.profile.save()
            
            # Créer le profil prestataire
            provider = super().save(commit=False)
            provider.user = user
            provider.status = 'pending'  # En attente de validation
            provider.save()
            
            # Créer les zones d'intervention
            zones_text = self.cleaned_data.get('zones', '')
            if zones_text:
                zones_list = [zone.strip() for zone in zones_text.split(',') if zone.strip()]
                for zone_name in zones_list:
                    ProviderZone.objects.create(
                        provider=provider,
                        city=zone_name
                    )
            
            return provider
        
        return super().save(commit=False)

class ProviderProfileForm(forms.ModelForm):
    """Formulaire de modification du profil prestataire"""
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Provider
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'service_type', 'description', 'experience_years', 'hourly_rate',
            'is_available'
        ]
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': 0}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        provider = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        if provider and provider.user:
            self.fields['first_name'].initial = provider.user.first_name
            self.fields['last_name'].initial = provider.user.last_name
            self.fields['email'].initial = provider.user.email
            self.fields['phone'].initial = provider.user.profile.phone
            
        # Styling
        self.fields['first_name'].widget.attrs.update({'class': 'form-input'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-input'})
        self.fields['email'].widget.attrs.update({'class': 'form-input'})
        self.fields['phone'].widget.attrs.update({'class': 'form-input'})

    def save(self, commit=True):
        provider = super().save(commit=False)
        
        if commit:
            # Sauvegarder les changements sur l'utilisateur
            user = provider.user
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.email = self.cleaned_data.get('email', '')
            user.save()
            
            # Mettre à jour le téléphone dans le profil utilisateur
            user.profile.phone = self.cleaned_data.get('phone', '')
            user.profile.save()
            
            provider.save()
        
        return provider

class ProviderDocumentForm(forms.ModelForm):
    """Formulaire pour les documents justificatifs"""
    
    class Meta:
        model = ProviderDocument
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-input'}),
            'file': forms.FileInput(attrs={'class': 'form-input'}),
        }

class ProviderZoneForm(forms.ModelForm):
    """Formulaire pour les zones d'intervention"""
    
    class Meta:
        model = ProviderZone
        fields = ['city', 'neighborhood', 'is_active']
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ville ou quartier'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Secteur (optionnel)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        } 