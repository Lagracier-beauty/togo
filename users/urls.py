from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Page de test
    path('test/', views.test_page, name='test'),
    

    
    # Authentification
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('force-logout/', views.force_logout, name='force_logout'),
] 