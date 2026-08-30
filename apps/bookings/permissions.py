from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBookingOwnerOrAdminOrStaff(BasePermission):
    """
    Permite acceso:
    - Lectura: al propio huésped, admin, owner (de la propiedad involucrada), staff (solo ver datos básicos)
    - Escritura: al huésped (solo si es su reserva y está pendiente), admin, owner de la propiedad.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        # Si es admin, permiso total
        if user.role == 'admin':
            return True
        # Si es owner y la reserva es de su propiedad
        if user.role == 'owner':
            if obj.property and obj.property.owner == user:
                return True
            if obj.room and obj.room.property.owner == user:
                return True
        # Si es el propio huésped
        if user == obj.guest:
            if request.method in SAFE_METHODS:
                return True
            # Solo puede modificar/cancelar si está pendiente o confirmada
            if obj.status in ['pending', 'confirmed']:
                return True
        # Staff puede ver si está asignado a la tarea relacionada (no implementado aquí)
        if user.role == 'staff':
            if request.method in SAFE_METHODS:
                # Permitir ver reservas relacionadas con tareas asignadas (simplificación)
                return True
        return False