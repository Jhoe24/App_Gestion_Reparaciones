# =====================================================
# ARCHIVO: apps/users/admin.py
# =====================================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LogAcceso

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'cedula', 'telefono')}),
        ('Información del Cargo y Rol', {'fields': ('cargo', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Verificación', {'fields': ('is_email_verified', 'is_verified')}),
        ('Estado', {'fields': ('activo',)}),
        ('Fechas Importantes', {'fields': ('last_login', 'fecha_creacion', 'fecha_actualizacion'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'last_login')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'cedula', 'telefono', 'cargo', 'rol', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'cedula', 'telefono', 'cargo', 'rol', 'is_email_verified', 'is_verified', 'activo', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'rol', 'cargo', 'activo')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'cedula')
    ordering = ('last_name', 'first_name')

@admin.register(LogAcceso)
class LogAccesoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha_hora', 'direccion_ip')
    list_filter = ('accion', 'fecha_hora')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'direccion_ip')
    readonly_fields = ('fecha_hora',)


# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     """Administración personalizada de usuarios"""
    
#     list_display = ('username', 'email', 'get_full_name', 'cedula', 'rol', 'is_active', 'date_joined')
#     list_filter = ('rol', 'is_active', 'is_staff', 'date_joined')
#     search_fields = ('username', 'email', 'first_name', 'last_name', 'cedula')
#     ordering = ('username',)
    
#     fieldsets = list(UserAdmin.fieldsets or ()) + [
#         ('Información Adicional', {
#             'fields': ('cedula', 'telefono', 'cargo', 'rol', 'activo')
#         }),
#     ]
    
#     add_fieldsets = list(UserAdmin.add_fieldsets or ()) + [
#         ('Información Adicional', {
#             'fields': ('email', 'first_name', 'last_name', 'cedula', 'telefono', 'cargo', 'rol')
#         }),
#     ]


# @admin.register(LogAcceso)
# class LogAccesoAdmin(admin.ModelAdmin):
#     """Administración de logs de acceso"""
    
#     list_display = ('usuario', 'accion', 'fecha_hora', 'direccion_ip')
#     list_filter = ('accion', 'fecha_hora')
#     search_fields = ('usuario__username', 'direccion_ip')
#     readonly_fields = ('usuario', 'fecha_hora', 'accion', 'direccion_ip', 'user_agent')
#     ordering = ('-fecha_hora',)
    
#     def has_add_permission(self, request):
#         return False
    
#     def has_change_permission(self, request, obj=None):
#         return False
