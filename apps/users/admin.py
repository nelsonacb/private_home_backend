from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Profile, Role

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    """
    Configuración personalizada del admin para el modelo User.
    """
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'phone', 'address', 'date_of_birth', 'avatar')}),
        ('Roles y permisos', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'is_active', 'is_staff'),
        }),
    )

    def has_module_permission(self, request):
        # Solo superusuarios y staff pueden ver la app users en admin
        return request.user.is_superuser or request.user.is_staff

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'position', 'passport_number', 'nationality')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'business_name')
    list_filter = ('nationality', 'position')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)