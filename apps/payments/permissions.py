from rest_framework.permissions import BasePermission

class IsPaymentOwnerOrAdmin(BasePermission):
    """
    Permite que un huésped solo vea los pagos de sus propias reservas.
    Admin/owner pueden ver todos.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ['admin', 'owner']:
            return True
        return obj.booking.guest == request.user