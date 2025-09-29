from django.conf import settings
from proyecto_sorteo.celery import app
from .utils.email import send_verification_email, send_winner_notification_email


@app.task(bind=True, name='api.send_verification_email')
def send_verification_email_task(self, user_id, verification_link):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return False

    return send_verification_email(user, verification_link)

@app.task(bind=True, name='api.send_winner_notification_email')
def send_winner_notification_email_task(self, user_id):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return False

    return send_winner_notification_email(user)
