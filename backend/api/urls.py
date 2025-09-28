from django.urls import path
from api import views

urlpatterns = [

    # Participants
    path('participants/register/', views.register_participant, name='api-participant-register'),

    # Admin
]
