from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Property(models.Model):
    """
    Modelo que representa una casa o apartamento completo.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, default='La Habana')
    province = models.CharField(max_length=100, blank=True)
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    max_guests = models.PositiveIntegerField(default=1)
    services = models.JSONField(
        default=list,
        blank=True,
        help_text='Lista de servicios disponibles, ej: ["wifi", "aire acondicionado", "cocina"]'
    )
    # Relación con el propietario (puede ser admin u owner)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties',
        limit_choices_to={'role__in': ['admin', 'owner']}
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'propiedad'
        verbose_name_plural = 'propiedades'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Room(models.Model):
    """
    Habitación individual dentro de una propiedad.
    """
    ROOM_TYPES = [
        ('single', 'Individual'),
        ('double', 'Doble'),
        ('triple', 'Triple'),
        ('suite', 'Suite'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='double')
    capacity = models.PositiveIntegerField(default=2)
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    description = models.TextField(blank=True)
    amenities = models.JSONField(
        default=list,
        blank=True,
        help_text='Lista de comodidades de la habitación'
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'habitación'
        verbose_name_plural = 'habitaciones'
        ordering = ['property', 'room_number']
        unique_together = ['property', 'room_number']  # No repetir número en la misma propiedad

    def __str__(self):
        return f'{self.property.name} - Hab. {self.room_number}'