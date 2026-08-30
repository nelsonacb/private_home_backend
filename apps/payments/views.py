from rest_framework import viewsets, permissions
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter
from .permissions import IsPaymentOwnerOrAdmin

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para pagos.
    - Admin/owner: CRUD completo.
    - Huésped: solo puede ver los pagos de sus propias reservas.
    - Staff: sin acceso (no lo incluimos aquí).
    """
    queryset = Payment.objects.select_related('booking__guest').all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
    search_fields = ['reference', 'booking__guest__email']
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']

    def get_permissions(self):
        if self.action in ['list', 'create']:
            # Solo admin/owner pueden listar todos o crear pagos
            permission_classes = [permissions.IsAuthenticated, IsPaymentOwnerOrAdmin]
        else:
            # Para retrieve/update/delete, aplicar permiso de objeto
            permission_classes = [permissions.IsAuthenticated, IsPaymentOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'guest':
            # Un huésped solo ve pagos de sus reservas
            return self.queryset.filter(booking__guest=user)
        return self.queryset