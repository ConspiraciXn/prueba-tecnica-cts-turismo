import logging
import requests
from django.conf import settings
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


# Utils functions
def mailgun_config():
    api_key = settings.MAILGUN_API_KEY
    domain = settings.MAILGUN_DOMAIN
    api_base_url = (settings.MAILGUN_API_BASE_URL or '').rstrip('/') if settings.MAILGUN_API_BASE_URL else ''
    sender = settings.MAILGUN_SENDER or (
        f'CTS Turismo <no-reply@{domain}>' if domain else 'CTS Turismo <no-reply@example.com>'
    )
    return api_key, domain, api_base_url, sender

def send_mailgun_request(*, to, subject, html):
    api_key, domain, api_base_url, sender = mailgun_config()

    if not all([api_key, domain, api_base_url]):
        logger.warning('Mailgun configuration incomplete; email not sent.')
        return False

    endpoint = f'{api_base_url}/{domain}/messages'

    try:
        response = requests.post(
            endpoint,
            auth=('api', api_key),
            data={
                'from': sender,
                'to': list(to),
                'subject': subject,
                'html': html,
            },
            timeout=10,
        )
        response.raise_for_status()
        
    except requests.RequestException as exc:
        logger.exception('Error sending email via Mailgun', exc_info=exc)
        return False

    return True

def render_email(template_name, context=None):
    return render_to_string(template_name, context or {})

def send_email(subject, recipient, template_name, context=None):
    html_content = render_email(template_name, context)
    return send_mailgun_request(to=[recipient], subject=subject, html=html_content)


# Specific email sent functions
def send_verification_email(user, verification_link):
    subject = 'Verifica tu correo - Sorteo de San Valentín'
    context = {
        'user': user,
        'verification_link': verification_link,
    }
    return send_email(subject, user.email, 'emails/verification_email.html', context)
