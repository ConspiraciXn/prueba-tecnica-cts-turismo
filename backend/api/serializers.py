from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from api.models import ParticipantProfile

User = get_user_model()

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
        normalized_rut = value.strip().upper()
        if ParticipantProfile.objects.filter(rut__iexact=normalized_rut).exists():
            raise serializers.ValidationError('Este RUT ya está registrado en el sorteo.')
        return normalized_rut

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
            profile.phone = validated_data['phone'].strip()
            profile.address = validated_data['address'].strip()
            profile.save(update_fields=['rut', 'phone', 'address'])

        return user
