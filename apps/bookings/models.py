from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from jsonschema import ValidationError
from apps.properties.models import Property, Room

class Booking(models.Model):
    """
    Modelo que representa una reserva.
    Puede ser de una habitación específica (room) o de una propiedad completa (property).
    """
    class BookingStatus(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        CONFIRMED = 'confirmed', 'Confirmada'
        CHECKED_IN = 'checked_in', 'Check-in'
        CHECKED_OUT = 'checked_out', 'Check-out'
        CANCELLED = 'cancelled', 'Cancelada'

    # Relación con el huésped (usuario con rol guest)
    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': 'guest'}
    )
    # La reserva puede ser para una habitación específica o para toda la propiedad
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        ordering = ['-created_at']

    def __str__(self):
        return f'Reserva {self.id} - {self.guest.email}'

    def clean(self):
        # Validar que check_out > check_in
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError('La fecha de salida debe ser posterior a la de entrada.')
        # Validar que al menos se especifique room o property (no ambos o ninguno)
        if not self.room and not self.property:
            raise ValidationError('Debe especificar una habitación o una propiedad.')
        if self.room and self.property:
            raise ValidationError('Debe especificar solo una habitación o una propiedad, no ambas.')

    def save(self, *args, **kwargs):
        # Calcular total_price automáticamente si no se proporciona
        if not self.total_price:
            nights = (self.check_out - self.check_in).days
            if self.room:
                self.total_price = self.room.price_per_night * nights
            elif self.property:
                self.total_price = self.property.price_per_night * nights
        super().save(*args, **kwargs)