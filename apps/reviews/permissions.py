from rest_framework.permissions import BasePermission

class IsGuestForReview(BasePermission):
    """
    Permite que un huésped solo modifique sus propias opiniones.
    Admin/owner pueden gestionar todas.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ['admin', 'owner']:
            return True
        return obj.booking.guest == request.user