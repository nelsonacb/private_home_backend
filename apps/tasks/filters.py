import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    """Filtros para tareas."""
    assigned_to_email = django_filters.CharFilter(field_name='assigned_to__email', lookup_expr='icontains')
    task_type = django_filters.ChoiceFilter(choices=Task.TaskType.choices)
    status = django_filters.ChoiceFilter(choices=Task.TaskStatus.choices)
    due_date_from = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')
    due_date_to = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')
    booking_id = django_filters.NumberFilter(field_name='booking__id')
    room_number = django_filters.CharFilter(field_name='room__room_number', lookup_expr='icontains')

    class Meta:
        model = Task
        fields = [
            'assigned_to_email', 'task_type', 'status',
            'due_date_from', 'due_date_to', 'booking_id', 'room_number'
        ]