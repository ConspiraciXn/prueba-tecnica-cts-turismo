from rest_framework import status
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from api.models import ParticipantProfile
from api.serializers import AdminLoginSerializer, EmailVerificationLinkSerializer, EmailVerificationSerializer, ParticipantRegistrationSerializer
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
            message='¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.',
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
@api_view(['POST'])
def admin_login(request):

    serializer = AdminLoginSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        data = {
            'token': token.key,
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        return success_response(
            data=data,
            message='Inicio de sesión exitoso.',
        )

    return error_response(
        message='No pudimos iniciar sesión con las credenciales proporcionadas.',
        errors=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST,
    )

@api_view(['GET'])
def admin_participant_list(request):

    admin_user = request.user

    if not admin_user.is_authenticated:
        return error_response(
            message='No autorizado.',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if not admin_user.is_superuser:
        return error_response(
            message='No tienes permisos para acceder a esta información.',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    search = request.query_params.get('search', '').strip()
    verified = request.query_params.get('verified', '').lower()

    participants = ParticipantProfile.objects.select_related('user')

    if search:
        participants = participants.filter(
            Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__email__icontains=search)
            | Q(rut__icontains=search)
        )

    if verified in ['true', 'false']:
        is_active = verified == 'true'
        participants = participants.filter(user__is_active=is_active)

    participants = participants.order_by('-created_at')

    results = []
    for profile in participants:
        user = profile.user
        results.append({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'rut': profile.rut,
            'verified': user.is_active,
            'registered_at': profile.created_at.isoformat() if profile.created_at else None,
        })

    return success_response(
        data={
            'results': results,
            'count': len(results),
        },
        message='Listado de participantes recuperado correctamente.',
    )
