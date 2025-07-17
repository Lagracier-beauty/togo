from django.urls import path
from . import api_views

urlpatterns = [
    path('auth/login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('auth/register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('auth/logout/', api_views.LogoutAPIView.as_view(), name='api_logout'),
    path('auth/change-password/', api_views.ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('profile/', api_views.UserProfileAPIView.as_view(), name='api_profile'),
    path('orders/', api_views.UserOrdersAPIView.as_view(), name='api_user_orders'),
    path('addresses/', api_views.UserAddressListAPIView.as_view(), name='api_addresses'),
    path('addresses/<int:pk>/', api_views.UserAddressDetailAPIView.as_view(), name='api_address_detail'),
    path('stats/', api_views.user_stats, name='api_user_stats'),
] 