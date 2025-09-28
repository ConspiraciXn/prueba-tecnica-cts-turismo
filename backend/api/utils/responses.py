from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, message='Solicitud procesada correctamente.', *, status_code=status.HTTP_200_OK):

    payload = {
        'status': 'OK',
        'message': message,
    }

    if data is not None:
        payload['data'] = data

    return Response(payload, status=status_code)

def error_response(message, errors=None, *, status_code=status.HTTP_400_BAD_REQUEST):
    payload = {
        'status': 'ERROR',
        'message': message,
    }

    if errors is not None:
        payload['errors'] = errors

    return Response(payload, status=status_code)
