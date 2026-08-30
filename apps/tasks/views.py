from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter
from .permissions import IsAdminOrOwnerForTasks, IsStaffForTasks

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet para tareas.
    - Admin/owner: CRUD completo.
    - Staff: solo puede listar tareas asignadas a él y actualizar el estado.
    """
    queryset = Task.objects.select_related('assigned_to', 'booking', 'room').all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    search_fields = ['title', 'description', 'assigned_to__email', 'room__room_number']
    ordering_fields = ['due_date', 'created_at', 'status']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Staff puede ver sus tareas, admin/owner todas
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'destroy']:
            # Solo admin/owner pueden crear o eliminar
            permission_classes = [IsAdminOrOwnerForTasks]
        elif self.action in ['update', 'partial_update']:
            # Admin/owner o el staff asignado (solo cambiar estado)
            permission_classes = [IsAdminOrOwnerForTasks | IsStaffForTasks]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'staff':
            return self.queryset.filter(assigned_to=user)
        return self.queryset

    def perform_create(self, serializer):
        # Solo admin/owner llegan aquí; podrían asignar a un staff
        serializer.save()