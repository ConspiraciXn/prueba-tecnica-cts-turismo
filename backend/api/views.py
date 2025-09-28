from rest_framework import status
from rest_framework.decorators import api_view
from api.serializers import ParticipantRegistrationSerializer
from api.utils.responses import error_response, success_response


# Participants
@api_view(['POST'])
def register_participant(request):

    serializer = ParticipantRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        
        user = serializer.save()
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


# Admins