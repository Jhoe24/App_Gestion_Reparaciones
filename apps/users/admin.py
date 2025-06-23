# =====================================================
# ARCHIVO: apps/users/admin.py
# =====================================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LogAcceso


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Administración personalizada de usuarios"""
    
    list_display = ('username', 'email', 'get_full_name', 'cedula', 'rol', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cedula')
    ordering = ('username',)
    
    fieldsets = list(UserAdmin.fieldsets or ()) + [
        ('Información Adicional', {
            'fields': ('cedula', 'telefono', 'cargo', 'rol', 'activo')
        }),
    ]
    
    add_fieldsets = list(UserAdmin.add_fieldsets or ()) + [
        ('Información Adicional', {
            'fields': ('email', 'first_name', 'last_name', 'cedula', 'telefono', 'cargo', 'rol')
        }),
    ]


@admin.register(LogAcceso)
class LogAccesoAdmin(admin.ModelAdmin):
    """Administración de logs de acceso"""
    
    list_display = ('usuario', 'accion', 'fecha_hora', 'direccion_ip')
    list_filter = ('accion', 'fecha_hora')
    search_fields = ('usuario__username', 'direccion_ip')
    readonly_fields = ('usuario', 'fecha_hora', 'accion', 'direccion_ip', 'user_agent')
    ordering = ('-fecha_hora',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
