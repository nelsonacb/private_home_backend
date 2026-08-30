from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Profile
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    RegisterSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
)
from .permissions import IsAdmin, IsSelfOrAdminOrOwner, IsAdminOrOwner
from .filters import UserFilter

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    Endpoint público para registro de usuarios (huéspedes por defecto).
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'success': True,
                'message': 'Usuario registrado correctamente.',
                'user': UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(TokenObtainPairView):
    """
    Endpoint para login. Devuelve access y refresh tokens.
    """

class RefreshTokenView(TokenRefreshView):
    """
    Endpoint para refrescar el access token.
    """

class LogoutView(APIView):
    """
    Endpoint para logout. Agrega el refresh token a la blacklist.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'Refresh token es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'success': True, 'message': 'Logout exitoso.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de usuarios.
    Solo los administradores pueden listar y crear usuarios con cualquier rol.
    Los usuarios autenticados pueden ver/editar su propio perfil.
    """
    queryset = User.objects.all().select_related('profile')
    filterset_class = UserFilter
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'email']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        """
        - list/create: solo admin (o owner para crear staff/guest)
        - retrieve/update/partial_update/destroy: el propio usuario o admin/owner
        """
        if self.action in ['list', 'create']:
            permission_classes = [IsAdminOrOwner]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSelfOrAdminOrOwner]
        elif self.action == 'change_password':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Endpoint para obtener el perfil del usuario autenticado."""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def update_me(self, request):
        """Endpoint para actualizar el perfil del usuario autenticado."""
        user = request.user
        serializer = UserDetailSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsSelfOrAdminOrOwner])
    def change_password(self, request, pk=None):
        """Endpoint para cambiar contraseña de un usuario (solo para sí mismo o admin/owner)."""
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'message': 'Contraseña actualizada.'})

class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet para perfiles.
    Solo admin/owner pueden listar; un usuario puede ver/editar su propio perfil.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [IsAdminOrOwner]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSelfOrAdminOrOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]