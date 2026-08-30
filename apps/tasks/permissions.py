from rest_framework.permissions import BasePermission

class IsAdminOrOwnerForTasks(BasePermission):
    """
    Permite acceso total a admin/owner.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'owner']

class IsStaffForTasks(BasePermission):
    """
    Permite al staff ver y actualizar solo sus propias tareas.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        return obj.assigned_to == request.user