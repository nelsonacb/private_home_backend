from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.bookings.models import Booking
from apps.properties.models import Property, Room

class Review(models.Model):
    """
    Opinión dejada por un huésped sobre una propiedad o habitación.
    """
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Reserva asociada a la opinión.'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
        help_text='Propiedad sobre la que se opina (si aplica).'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
        help_text='Habitación sobre la que se opina (si aplica).'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'opinión'
        verbose_name_plural = 'opiniones'
        ordering = ['-created_at']
        # Un huésped no puede opinar dos veces sobre la misma reserva
        unique_together = ['booking', 'property', 'room']

    def __str__(self):
        return f'Opinión {self.id} - {self.booking} ({self.rating}/5)'

    def clean(self):
        # Al menos property o room debe estar presente
        if not self.property and not self.room:
            from django.core.exceptions import ValidationError
            raise ValidationError('Debe especificar una propiedad o una habitación para la opinión.')
        # No pueden ambos estar presentes (aunque podría permitirse, lo simplificamos)
        if self.property and self.room:
            from django.core.exceptions import ValidationError
            raise ValidationError('Elija solo una propiedad o una habitación, no ambas.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)