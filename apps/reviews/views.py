from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from .filters import ReviewFilter
from .permissions import IsGuestForReview

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet para opiniones.
    - Cualquier usuario autenticado puede ver opiniones.
    - Crear: solo huéspedes (o admin/owner en nombre de un huésped).
    - Actualizar/eliminar: el huésped autor o admin/owner.
    """
    queryset = Review.objects.select_related('booking__guest', 'property', 'room').all()
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter
    search_fields = ['comment', 'booking__guest__email', 'property__name', 'room__room_number']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create']:
            # Solo huéspedes, admin/owner
            permission_classes = [permissions.IsAuthenticated]
        else:  # update, partial_update, destroy
            permission_classes = [permissions.IsAuthenticated, IsGuestForReview]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Los huéspedes solo pueden ver sus propias opiniones si así lo deseamos,
        # pero aquí permitimos ver todas (o se podría filtrar)
        return self.queryset

    def perform_create(self, serializer):
        # Asignar automáticamente al huésped si el usuario es guest
        if self.request.user.role == 'guest':
            booking = serializer.validated_data.get('booking')
            # Verificar que la reserva pertenece al usuario
            if booking.guest != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("No puedes opinar sobre una reserva que no es tuya.")
            serializer.save()
        else:
            serializer.save()