from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Property, Room
from .serializers import PropertyListSerializer, PropertyDetailSerializer, RoomSerializer
from .filters import PropertyFilter, RoomFilter
from .permissions import IsPropertyOwnerOrReadOnly

class PropertyViewSet(viewsets.ModelViewSet):
    """
    ViewSet para propiedades.
    - Cualquier usuario autenticado puede ver (GET).
    - Solo admin/owner pueden crear, actualizar o eliminar.
    - El propietario solo puede gestionar sus propias propiedades.
    """
    queryset = Property.objects.select_related('owner').prefetch_related('rooms').all()
    filterset_class = PropertyFilter
    search_fields = ['name', 'description', 'address', 'city', 'province']
    ordering_fields = ['price_per_night', 'created_at', 'name']
    ordering = ['-created_at']
    permission_classes = [IsPropertyOwnerOrReadOnly]  # Requiere autenticación para todo

    def get_serializer_class(self):
        if self.action == 'list':
            return PropertyListSerializer
        return PropertyDetailSerializer

    def perform_create(self, serializer):
        # Asignar automáticamente el propietario como el usuario autenticado
        serializer.save(owner=self.request.user)

class RoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet para habitaciones.
    - Usuarios autenticados pueden ver habitaciones disponibles.
    - Solo el dueño de la propiedad o admin pueden crear/editar/eliminar.
    """
    queryset = Room.objects.select_related('property__owner').all()
    serializer_class = RoomSerializer
    filterset_class = RoomFilter
    search_fields = ['room_number', 'property__name', 'room_type']
    ordering_fields = ['price_per_night', 'capacity', 'room_number']
    ordering = ['property__name', 'room_number']
    permission_classes = [IsPropertyOwnerOrReadOnly]