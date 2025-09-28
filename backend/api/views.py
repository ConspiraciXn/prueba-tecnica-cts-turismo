from rest_framework import status
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.decorators import api_view
from api.serializers import EmailVerificationLinkSerializer, EmailVerificationSerializer, ParticipantRegistrationSerializer
from api.utils.responses import error_response, success_response
from api.utils.email import send_verification_email


# Participants
@api_view(['POST'])
def register_participant(request):

    serializer = ParticipantRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        
        user = serializer.save()

        # Generate verification link and send email
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = f"{settings.FRONTEND_BASE_URL.rstrip('/')}/email-verification?uid={uidb64}&token={token}"
        send_verification_email(user, verification_link)

        data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'rut': user.participant_profile.rut,
        }

        return success_response(
            data=data,
            message='Revisa tu correo para verificar tu cuenta y completar tu registro.',
            status_code=status.HTTP_201_CREATED,
        )

    return error_response(
        message='Hay errores en el formulario de registro.',
        errors=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST,
    )

@api_view(['POST'])
def validate_verification_link(request):

    serializer = EmailVerificationLinkSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.validated_data['user']
        profile = user.participant_profile

        data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'rut': profile.rut,
            'phone': profile.phone,
            'address': profile.address,
        }

        return success_response(
            data=data,
            message='El enlace es válido. Crea tu contraseña para activar la cuenta.',
        )

    return error_response(
        message='El enlace de verificación no es válido o ha expirado.',
        errors=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST,
    )

@api_view(['POST'])
def verify_participant_email(request):

    serializer = EmailVerificationSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.save()
        profile = user.participant_profile

        data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'rut': profile.rut,
            'phone': profile.phone,
            'address': profile.address,
        }

        return success_response(
            data=data,
            message='Tu cuenta ha sido activada. Ya te encuentras participando en el sorteo.',
        )

    return error_response(
        message='No pudimos activar tu cuenta. Revisa los datos ingresados.',
        errors=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST,
    )


# Admins
