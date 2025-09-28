from django.urls import path
from api import views

urlpatterns = [

    # Participants
    path('participants/verify-email/validate/', views.validate_verification_link, name='api-participant-verify-email-validate'),
    path('participants/register/', views.register_participant, name='api-participant-register'),
    path('participants/verify-email/', views.verify_participant_email, name='api-participant-verify-email'),

    # Admin
    path('admin/login/', views.admin_login, name='api-admin-login'),
    
]
