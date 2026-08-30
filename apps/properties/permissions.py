from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.properties.models import Property, Room
from apps.users.permissions import IsAdminOrOwner, IsAdmin, IsOwner

class IsPropertyOwner(BasePermission):
    """
    Permite acceso solo al propietario de la propiedad o admin.
    Útil para acciones de escritura sobre Property y Room.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        # obj puede ser Property o Room
        if isinstance(obj, Property):
            return request.user == obj.owner or request.user.role == 'admin'
        elif isinstance(obj, Room):
            return request.user == obj.property.owner or request.user.role == 'admin'
        return False

class IsPropertyOwnerOrReadOnly(BasePermission):
    """
    Permite lectura a cualquier usuario autenticado, escritura solo al dueño o admin.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (request.user.role in ['admin', 'owner'])

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        if isinstance(obj, Property):
            return request.user == obj.owner or request.user.role == 'admin'
        elif isinstance(obj, Room):
            return request.user == obj.property.owner or request.user.role == 'admin'
        return False