from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ParticipantProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='participant_profile',
    )
    rut = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de participante'
        verbose_name_plural = 'Perfiles de participantes'

    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"


# Signal to create a participan profile when a new django User is created.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_participant_profile(sender, instance, created, **kwargs):
    if created:
        ParticipantProfile.objects.create(user=instance)
