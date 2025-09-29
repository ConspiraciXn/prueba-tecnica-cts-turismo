from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import ParticipantProfile

User = get_user_model()


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, ALLOWED_HOSTS=['testserver', 'localhost'])
class ParticipantRegistrationTests(APITestCase):
    def setUp(self):
        self.url = reverse('api-participant-register')

    @patch('api.views.send_verification_email_task.delay')
    def test_register_participant_success(self, mock_delay):
        payload = {
            'first_name': 'Ana',
            'last_name': 'Pérez',
            'email': 'ana@example.com',
            'rut': '12.345.678-9',
            'phone': '+56 9 1234 5678',
            'address': 'Av. Siempre Viva 742',
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'OK')
        self.assertTrue(User.objects.filter(email='ana@example.com').exists())
        mock_delay.assert_called_once()

    def test_register_duplicate_email(self):
        User.objects.create_user(
            username='ana@example.com',
            email='ana@example.com',
            first_name='Ana',
            last_name='Pérez',
        )

        payload = {
            'first_name': 'Ana',
            'last_name': 'Pérez',
            'email': 'ana@example.com',
            'rut': '12.345.678-9',
            'phone': '+56 9 1234 5678',
            'address': 'Av. Siempre Viva 742',
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'ERROR')


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, ALLOWED_HOSTS=['testserver', 'localhost'])
class EmailVerificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            first_name='Test',
            last_name='User',
        )
        self.user.set_unusable_password()
        self.user.is_active = False
        self.user.save()
        ParticipantProfile.objects.get_or_create(user=self.user)

        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_validate_verification_link(self):
        url = reverse('api-participant-verify-email-validate')
        payload = {'uid': self.uid, 'token': self.token}

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'OK')

    def test_verify_participant_email(self):
        url = reverse('api-participant-verify-email')
        payload = {
            'uid': self.uid,
            'token': self.token,
            'password': 'ClaveSegura123',
            'confirm_password': 'ClaveSegura123',
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.check_password('ClaveSegura123'))


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, ALLOWED_HOSTS=['testserver', 'localhost'])
class AdminEndpointsTests(APITestCase):
    def setUp(self):
        self.admin_password = 'AdminClave123'
        self.admin = User.objects.create_superuser(
            username='admin@example.com',
            email='admin@example.com',
            password=self.admin_password,
        )

    def authenticate(self):
        url = reverse('api-admin-login')
        response = self.client.post(
            url,
            {'email': 'admin@example.com', 'password': self.admin_password},
            format='json',
        )
        token = response.data['data']['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_admin_login(self):
        url = reverse('api-admin-login')
        response = self.client.post(
            url,
            {'email': 'admin@example.com', 'password': self.admin_password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data['data'])

    def test_admin_participant_list_filters(self):
        self.authenticate()

        active_user = User.objects.create_user(
            username='ana@example.com',
            email='ana@example.com',
            first_name='Ana',
            last_name='Pérez',
        )
        active_user.is_active = True
        active_user.save()
        active_profile = ParticipantProfile.objects.get(user=active_user)
        active_profile.rut = '12.345.678-9'
        active_profile.save()

        inactive_user = User.objects.create_user(
            username='carlos@example.com',
            email='carlos@example.com',
            first_name='Carlos',
            last_name='Ruiz',
        )
        inactive_user.is_active = False
        inactive_user.save()
        ParticipantProfile.objects.get(user=inactive_user)

        url = reverse('api-admin-participant-list') + '?verified=true'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['count'], 1)
        self.assertEqual(response.data['data']['results'][0]['email'], 'ana@example.com')

    @patch('api.views.send_winner_notification_email_task.delay')
    def test_admin_draw_winner(self, mock_delay):
        self.authenticate()

        verified_user = User.objects.create_user(
            username='verificado@example.com',
            email='verificado@example.com',
            first_name='Vero',
            last_name='González',
        )
        verified_user.is_active = True
        verified_user.save()
        ParticipantProfile.objects.get(user=verified_user)

        url = reverse('api-admin-draw-winner')
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'verificado@example.com')
        mock_delay.assert_called_once_with(verified_user.id)
