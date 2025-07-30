from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.ServiceListAPIView.as_view(), name='api_services_list'),
    path('<int:pk>/', api_views.ServiceDetailAPIView.as_view(), name='api_service_detail'),
] 