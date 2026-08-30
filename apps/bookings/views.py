from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingListSerializer, BookingDetailSerializer, BookingCreateSerializer
from .filters import BookingFilter
from .permissions import IsBookingOwnerOrAdminOrStaff

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet para reservas.
    - Usuarios autenticados pueden listar (según su rol y filtros).
    - POST: un huésped puede crear su propia reserva.
    - PUT/PATCH/DELETE: solo dueño, admin u owner de la propiedad.
    """
    queryset = Booking.objects.select_related('guest', 'room', 'property__owner').all()
    filterset_class = BookingFilter
    search_fields = ['guest__email', 'property__name', 'room__room_number']
    ordering_fields = ['check_in', 'check_out', 'total_price', 'created_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated, IsBookingOwnerOrAdminOrStaff]

    def get_serializer_class(self):
        if self.action == 'list':
            return BookingListSerializer
        elif self.action == 'create':
            return BookingCreateSerializer
        return BookingDetailSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        # Filtrar según rol
        if user.role == 'guest':
            # Los huéspedes solo ven sus propias reservas
            return qs.filter(guest=user)
        elif user.role == 'owner':
            # Los propietarios ven reservas de sus propiedades
            return qs.filter(
                models.Q(property__owner=user) | models.Q(room__property__owner=user)
            )
        elif user.role == 'staff':
            # Staff ve todas (por ahora) - se podría limitar por tareas
            return qs
        # Admin ve todas
        return qs

    def perform_create(self, serializer):
        # Asignar huésped automáticamente
        serializer.save(guest=self.request.user)