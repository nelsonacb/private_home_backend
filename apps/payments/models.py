from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from apps.bookings.models import Booking

class Payment(models.Model):
    """
    Modelo que representa un pago asociado a una reserva.
    """
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Efectivo'
        BANK_TRANSFER = 'bank_transfer', 'Transferencia bancaria'
        OTHER = 'other', 'Otro'

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    payment_date = models.DateField(auto_now_add=True)
    method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'pago'
        verbose_name_plural = 'pagos'
        ordering = ['-payment_date']

    def __str__(self):
        return f'Pago {self.id} - {self.booking} ({self.amount})'