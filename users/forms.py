from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import UserProfile, UserAddress

class CustomUserCreationForm(UserCreationForm):
    """Formulaire d'inscription personnalisé"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=True)
    user_type = forms.ChoiceField(
        choices=[
            ('client', 'Client'),
            ('provider', 'Prestataire')
        ],
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'user_type', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Nom d\'utilisateur'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'votre@email.com'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Prénom'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Nom de famille'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '+228 XX XX XX XX'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirmer le mot de passe'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Créer le profil utilisateur
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data['phone'],
                    'is_premium': self.cleaned_data['user_type'] == 'provider',  # Temporaire pour les prestataires
                }
            )
            
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """Formulaire de connexion personnalisé qui accepte email ou username"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Email ou nom d\'utilisateur'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Mot de passe'
        })
        # Changer le label pour indiquer qu'on peut utiliser l'email
        self.fields['username'].label = 'Email ou nom d\'utilisateur'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            # D'abord essayer avec le username/email tel quel
            self.user_cache = authenticate(
                self.request, 
                username=username, 
                password=password
            )
            
            # Si ça ne marche pas et que ça ressemble à un email, essayer de trouver le user par email
            if self.user_cache is None and '@' in username:
                try:
                    user_obj = User.objects.get(email=username)
                    self.user_cache = authenticate(
                        self.request, 
                        username=user_obj.username, 
                        password=password
                    )
                except User.DoesNotExist:
                    pass
            
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class UserProfileForm(forms.ModelForm):
    """Formulaire de profil utilisateur"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Mettre à jour l'utilisateur
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
            profile.save()
        return profile

class UserAddressForm(forms.ModelForm):
    """Formulaire d'adresse utilisateur"""
    class Meta:
        model = UserAddress
        fields = ['type', 'name', 'address', 'city', 'postal_code', 'is_default'] 