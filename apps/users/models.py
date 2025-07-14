# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    email_verification_token = models.CharField(max_length=64, blank=True, null=True, help_text='Token para la verificación de correo electrónico')
    """
    Modelo de usuario personalizado para el sistema de gestión de mantenimiento
    """
    # Validador para cédula 
    cedula_validator = RegexValidator(
        regex=r'^[VE]-?\d{7,8}$',
        message='La cédula debe tener el formato V-12345678 o E-12345678'
    )
    
    # Validador para teléfono
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='El número de teléfono debe contener entre 9 y 15 dígitos'
    )
    
    # Campos adicionales
    cedula = models.CharField(
        max_length=20, 
        unique=True,
        validators=[cedula_validator],
        help_text='Formato: V-12345678 o E-12345678'
    )
    
    telefono = models.CharField(
        max_length=20,
        validators=[phone_validator],
        help_text='Número de celular de contacto'
    )
    CARGO_CHOICES =  [
        ('docente', 'Docente'),
        ('coordinador', 'Coordinador'),
        ('administrativo', 'Peronal Administrativo'),
        ('tecnico', 'Tecnico'),
    ]
    
    cargo = models.CharField(
        max_length=50,
        choices=CARGO_CHOICES,
        default='Docente',
        help_text='Seleccione el cargo o función que desempeña el usuario'
    )
    
    # Roles del sistema
    ROLES = [
        ('administrador', 'Administrador'),
        ('tecnico', 'Técnico'),
        ('usuario', 'Usuario'),
    ]
    
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='usuario',
        help_text='Rol del usuario en el sistema'
    )
    
    # Verificación de correo
    is_email_verified = models.BooleanField(default=False, help_text='Indica si el usuario ha verificado su correo electrónico')
    is_verified = models.BooleanField(default=False, help_text='Indica si el usuario ha verificado su email (usado en login y registro)')
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.cedula}) - {self.get_rol_display()}"
    
    def get_full_name(self):
        """Devuelve el nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_rol_display(self):
        """Devuelve el valor legible por humanos para el campo rol."""
        return dict(self.ROLES).get(self.rol, self.rol)

 
    @property
    def is_administrador(self):
        return self.rol == 'administrador'
    
    @property
    def is_tecnico(self):
        return self.rol == 'tecnico'
    
    @property
    def is_usuario_regular(self):
        return self.rol == 'usuario'


class LogAcceso(models.Model):
    """
    Modelo para registrar los accesos al sistema
    """
    ACCIONES = [
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('failed_login', 'Intento fallido de login'),
        ('password_change', 'Cambio de contraseña'),
        ('password_reset', 'Recuperación de contraseña'),
    ]
    
    usuario = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='logs_acceso'
    )
    
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
    accion = models.CharField(
        max_length=20,
        choices=ACCIONES
    )
    
    direccion_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    def get_accion_display(self):
        """Devuelve el valor legible por humanos para el campo accion."""
        return dict(self.ACCIONES).get(self.accion, self.accion)
    
    class Meta:
        db_table = 'registros_acceso'
        verbose_name = 'Log de Acceso'
        verbose_name_plural = 'Logs de Acceso'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        usuario_str = self.usuario.username if self.usuario else 'Usuario desconocido'
        return f"{usuario_str} - {self.get_accion_display()} - {self.fecha_hora}"