import re

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import ParticipantProfile

User = get_user_model()

RUT_PATTERN = re.compile(r'^(?:\d{1}|\d{2})\.\d{3}\.\d{3}-[\dK]$')
PHONE_PATTERN = re.compile(r'^\+56 9 \d{4} \d{4}$')


def format_rut(value):
    cleaned = re.sub(r'[^0-9kK]', '', value).upper()
    if not cleaned:
        return ''

    cleaned = cleaned[:9]

    if len(cleaned) <= 1:
        return cleaned

    body, dv = cleaned[:-1], cleaned[-1]
    reversed_body = body[::-1]
    chunks = [reversed_body[i : i + 3][::-1] for i in range(0, len(reversed_body), 3)]
    formatted_body = '.'.join(reversed(chunks))
    return f'{formatted_body}-{dv}'


def format_phone(value):
    digits = re.sub(r'\D', '', value)

    if digits.startswith('569'):
        digits = digits[3:]
    elif digits.startswith('56'):
        digits = digits[2:]
    elif digits.startswith('9'):
        digits = digits[1:]

    digits = digits[:8]

    first_block = digits[:4]
    second_block = digits[4:]

    formatted = '+56 9'
    if first_block:
        formatted += f' {first_block}'
    if second_block:
        formatted += f' {second_block}'

    return formatted


class ParticipantRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    rut = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=32)
    address = serializers.CharField(max_length=255)

    def validate_email(self, value):
        normalized_email = value.strip().lower()
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError('Este correo ya está registrado en el sorteo.')
        return normalized_email

    def validate_rut(self, value):
        formatted_rut = format_rut(value)
        if not RUT_PATTERN.match(formatted_rut):
            raise serializers.ValidationError('Ingresa un RUT válido (formato 12.345.678-9).')
        if ParticipantProfile.objects.filter(rut__iexact=formatted_rut).exists():
            raise serializers.ValidationError('Este RUT ya está registrado en el sorteo.')
        return formatted_rut

    def validate_phone(self, value):
        formatted_phone = format_phone(value)
        if not PHONE_PATTERN.match(formatted_phone):
            raise serializers.ValidationError('Ingresa un teléfono válido (formato +56 9 1234 5678).')
        return formatted_phone

    def validate_address(self, value):
        normalized_address = value.strip()
        if not normalized_address:
            raise serializers.ValidationError('Ingresa una dirección válida.')
        return normalized_address

    def create(self, validated_data):
        with transaction.atomic():
            email = validated_data['email']

            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=validated_data['first_name'].strip(),
                last_name=validated_data['last_name'].strip(),
            )
            user.set_unusable_password()
            user.save(update_fields=['password'])

            profile, _ = ParticipantProfile.objects.get_or_create(user=user)
            profile.rut = validated_data['rut']
            profile.phone = validated_data['phone']
            profile.address = validated_data['address']
            profile.save(update_fields=['rut', 'phone', 'address'])

        return user
