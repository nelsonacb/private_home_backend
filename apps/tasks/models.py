from django.db import models
from django.conf import settings
from apps.bookings.models import Booking
from apps.properties.models import Room

class Task(models.Model):
    """
    Tarea asignada a un miembro del personal.
    Puede estar vinculada a una reserva o a una habitación (limpieza, reparación, etc.).
    """
    class TaskType(models.TextChoices):
        CLEANING = 'cleaning', 'Limpieza'
        MAINTENANCE = 'maintenance', 'Mantenimiento'
        CHECKIN_PREP = 'checkin_prep', 'Preparación check-in'
        CHECKOUT_PREP = 'checkout_prep', 'Preparación check-out'
        OTHER = 'other', 'Otra'

    class TaskStatus(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        IN_PROGRESS = 'in_progress', 'En progreso'
        COMPLETED = 'completed', 'Completada'
        CANCELLED = 'cancelled', 'Cancelada'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=30, choices=TaskType.choices, default=TaskType.OTHER)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.PENDING)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        limit_choices_to={'role': 'staff'}
    )
    booking = models.ForeignKey(
        Booking,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'tarea'
        verbose_name_plural = 'tareas'
        ordering = ['due_date', '-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        # Validar que al menos booking o room estén presentes
        if not self.booking and not self.room:
            from django.core.exceptions import ValidationError
            raise ValidationError('Debe especificar una reserva o una habitación para la tarea.')

    def save(self, *args, **kwargs):
        # Si se marca completada y no tiene completed_at, se asigna ahora
        if self.status == self.TaskStatus.COMPLETED and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
        # Si se cambia a otro estado distinto de completada, limpiar completed_at
        elif self.status != self.TaskStatus.COMPLETED and self.completed_at:
            self.completed_at = None
        self.full_clean()
        super().save(*args, **kwargs)