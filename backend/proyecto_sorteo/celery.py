import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_sorteo.settings')

app = Celery('proyecto_sorteo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
