from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.users.serializers import User

class IsAdmin(BasePermission):
    """Permite acceso solo a usuarios con rol admin."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsOwner(BasePermission):
    """Permite acceso a propietarios."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'

class IsStaff(BasePermission):
    """Permite acceso a personal."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'staff'

class IsGuest(BasePermission):
    """Permite acceso a huéspedes."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'guest'

class IsAdminOrOwner(BasePermission):
    """Permite acceso a admin o propietario."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'owner']

class IsSelfOrAdminOrOwner(BasePermission):
    """
    Permite acceso si el usuario es él mismo, un admin o un propietario.
    Útil para endpoints de perfil de usuario.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        # obj puede ser User o Profile
        user = obj if isinstance(obj, User) else getattr(obj, 'user', None)
        if user is None:
            return False
        return request.user == user or request.user.role in ['admin', 'owner']

class IsStaffOrAdmin(BasePermission):
    """Permite acceso a staff o admin."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'staff']