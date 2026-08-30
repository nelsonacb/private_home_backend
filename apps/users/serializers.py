from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile, Role

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil del usuario."""
    class Meta:
        model = Profile
        fields = [
            'id', 'avatar', 'bio', 'business_name', 'position',
            'salary', 'passport_number', 'nationality',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para el usuario (sin datos sensibles)."""
    full_name = serializers.SerializerMethodField()
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'role', 'profile', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return obj.get_full_name()

class UserDetailSerializer(UserSerializer):
    """Serializer extendido para vista de detalle (incluye más campos)."""
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['date_of_birth', 'address', 'is_active']

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuarios (huéspedes por defecto)."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=Role.choices, default=Role.GUEST, required=False)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2', 'first_name', 'last_name',
            'phone', 'address', 'date_of_birth', 'role'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        # Por seguridad, solo permitir registro como huésped o staff si el que registra es admin.
        # En una vista pública, forzamos rol guest.
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role in ['admin', 'owner']:
            # Los admins/owners pueden crear usuarios con otros roles
            role = validated_data.pop('role', Role.GUEST)
        else:
            # Registro público: siempre guest
            validated_data.pop('role', None)
            role = Role.GUEST

        user = User.objects.create_user(role=role, **validated_data)
        Profile.objects.create(user=user)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar contraseña."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value

    def validate_new_password(self, value):
        # Validación adicional: no igual a la anterior
        user = self.context['request'].user
        if user.check_password(value):
            raise serializers.ValidationError("La nueva contraseña debe ser diferente a la actual.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user