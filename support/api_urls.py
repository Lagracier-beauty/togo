from django.urls import path
from . import api_views

urlpatterns = [
    path('faq/', api_views.FAQListAPIView.as_view(), name='api_faq_list'),
    path('contact/', api_views.ContactAPIView.as_view(), name='api_contact'),
] 