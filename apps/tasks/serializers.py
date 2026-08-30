from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serializer para tareas."""
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)
    booking_id = serializers.IntegerField(source='booking.id', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    task_type_display = serializers.CharField(source='get_task_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'task_type', 'task_type_display',
            'status', 'status_display', 'assigned_to', 'assigned_to_email',
            'booking', 'booking_id', 'room', 'room_number',
            'due_date', 'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'completed_at', 'created_at', 'updated_at']

    def validate(self, data):
        request = self.context.get('request')
        if request and request.user.role == 'staff':
            allowed_fields = {'status'}
            if set(data.keys()) - allowed_fields:
                raise serializers.ValidationError("El personal solo puede actualizar el estado de la tarea.")
        return data