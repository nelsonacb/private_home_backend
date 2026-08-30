from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager

# Opciones de rol
class Role(models.TextChoices):
    ADMIN = 'admin', 'Administrador'
    OWNER = 'owner', 'Propietario'
    STAFF = 'staff', 'Personal'
    GUEST = 'guest', 'Huésped'

class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado.
    Usa email como campo de identificación (USERNAME_FIELD).
    """
    email = models.EmailField('correo electrónico', unique=True)
    first_name = models.CharField('nombre', max_length=100)
    last_name = models.CharField('apellidos', max_length=100)
    phone = models.CharField('teléfono', max_length=20, blank=True)
    address = models.CharField('dirección', max_length=255, blank=True)
    date_of_birth = models.DateField('fecha de nacimiento', null=True, blank=True)
    role = models.CharField(
        'rol',
        max_length=20,
        choices=Role.choices,
        default=Role.GUEST,
        help_text='Define los permisos del usuario en el sistema.'
    )
    is_active = models.BooleanField('activo', default=True)
    is_staff = models.BooleanField('staff', default=False)
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('fecha de actualización', auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

class Profile(models.Model):
    """
    Perfil extendido del usuario con datos adicionales según rol.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='usuario'
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    # Campos para propietario
    business_name = models.CharField(max_length=200, blank=True, null=True)

    # Campos para personal
    position = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Campos para huésped
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        return f'Perfil de {self.user.email}'