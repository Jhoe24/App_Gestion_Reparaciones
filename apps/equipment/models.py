from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Equipo(models.Model):
    """
    Modelo para representar los equipos de la universidad
    """
    
    # Validador para código institucional
    codigo_validator = RegexValidator(
        regex=r'^[A-Z]{2,4}-\d{4,8}$',
        message='El código debe tener el formato ABC-1234 (2-4 letras, guion, 4-8 números)'
    )
    
    # Tipos de equipos más comunes
    TIPOS_EQUIPO = [
        ('computadora_escritorio', 'Computadora de Escritorio'),
        ('laptop', 'Laptop'),
        ('impresora', 'Impresora'),
        ('proyector', 'Proyector'),
        ('scanner', 'Escáner'),
        ('servidor', 'Servidor'),
        ('switch', 'Switch de Red'),
        ('router', 'Router'),
        ('ups', 'UPS/Regulador'),
        ('monitor', 'Monitor'),
        ('teclado', 'Teclado'),
        ('mouse', 'Mouse'),
        ('camara', 'Cámara Web'),
        ('bocinas', 'Bocinas/Altavoces'),
        ('microfono', 'Micrófono'),
        ('tablet', 'Tablet'),
        ('disco_externo', 'Disco Duro Externo'),
        ('otro', 'Otro'),
    ]
    
    # Estados posibles del equipo
    ESTADOS_EQUIPO = [
        ('operativo', 'Operativo'),
        ('en_mantenimiento', 'En Mantenimiento'),
        ('reparado', 'Reparado'),
        ('no_reparable', 'No Reparable'),
        ('dado_de_baja', 'Dado de Baja'),
        ('en_espera', 'En Espera de Reparación'),
    ]
    
    # Ubicaciones comunes en la universidad
    UBICACIONES = [
        ('laboratorio_computo', 'Laboratorio de Cómputo'),
        ('laboratorio_redes', 'Laboratorio de Redes'),
        ('aula_clase', 'Aula de Clases'),
        ('oficina_administrativa', 'Oficina Administrativa'),
        ('biblioteca', 'Biblioteca'),
        ('auditorio', 'Auditorio'),
        ('sala_profesores', 'Sala de Profesores'),
        ('decanato', 'Decanato'),
        ('secretaria', 'Secretaría'),
        ('centro_computo', 'Centro de Cómputo'),
        ('almacen', 'Almacén'),
        ('otra', 'Otra Ubicación'),
    ]
    
    # Campos del modelo
    codigo = models.CharField(
        max_length=50,
        unique=True,
        validators=[codigo_validator],
        help_text='Código institucional del equipo (ej: LAB-0001)'
    )
    
    tipo_equipo = models.CharField(
        max_length=30,
        choices=TIPOS_EQUIPO,
        help_text='Tipo de equipo'
    )
    
    marca = models.CharField(
        max_length=50,
        help_text='Marca del equipo'
    )
    
    modelo = models.CharField(
        max_length=50,
        help_text='Modelo específico del equipo'
    )
    
    numero_serie = models.CharField(
        max_length=100,
        unique=True,
        help_text='Número de serie del fabricante'
    )
    
    ubicacion = models.CharField(
        max_length=30,
        choices=UBICACIONES,
        help_text='Ubicación habitual del equipo'
    )
    
    ubicacion_detalle = models.CharField(
        max_length=200,
        blank=True,
        help_text='Detalles específicos de la ubicación (ej: Aula 201, Escritorio 3)'
    )
    
    estado_actual = models.CharField(
        max_length=20,
        choices=ESTADOS_EQUIPO,
        default='operativo',
        help_text='Estado actual del equipo'
    )
    
    descripcion = models.TextField(
        blank=True,
        help_text='Descripción adicional del equipo'
    )
    
    especificaciones = models.JSONField(
        default=dict,
        blank=True,
        help_text='Especificaciones técnicas en formato JSON'
    )
    
    fecha_adquisicion = models.DateField(
        null=True,
        blank=True,
        help_text='Fecha de adquisición del equipo'
    )
    
    valor_adquisicion = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor de adquisición en bolívares'
    )
    
    # Relaciones
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipos_propios',
        help_text='Usuario responsable del equipo'
    )
    
    responsable_actual = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipos_responsable',
        help_text='Usuario que actualmente tiene el equipo'
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='equipos_creados'
    )
    
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'equipos'
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['tipo_equipo']),
            models.Index(fields=['estado_actual']),
            models.Index(fields=['ubicacion']),
        ]
    
    def __str__(self):
        # Usar búsqueda manual para el nombre a mostrar si get_tipo_equipo_display no es reconocido
        tipo_display = dict(self.TIPOS_EQUIPO).get(self.tipo_equipo, self.tipo_equipo)
        return f"{self.codigo} - {tipo_display} {self.marca} {self.modelo}"
    
    @property
    def nombre_completo(self):
        """Devuelve el nombre completo del equipo"""
        return f"{self.marca} {self.modelo} ({self.codigo})"
    
    @property
    def esta_operativo(self):
        """Verifica si el equipo está operativo"""
        return self.estado_actual == 'operativo'
    
    @property
    def esta_en_mantenimiento(self):
        """Verifica si el equipo está en mantenimiento"""
        return self.estado_actual in ['en_mantenimiento', 'en_espera']
    
    def cambiar_estado(self, nuevo_estado, usuario=None):
        """Cambia el estado del equipo y registra el cambio"""
        estado_anterior = self.estado_actual
        self.estado_actual = nuevo_estado
        self.save()
        
        # Crear registro de cambio de estado (se implementará en el modelo de historial)
        return f"Estado cambiado de {estado_anterior} a {nuevo_estado}"


class CambioEstadoEquipo(models.Model):
    """
    Modelo para registrar los cambios de estado de los equipos
    """
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='cambios_estado'
    )
    
    estado_anterior = models.CharField(
        max_length=20,
        choices=Equipo.ESTADOS_EQUIPO
    )
    
    estado_nuevo = models.CharField(
        max_length=20,
        choices=Equipo.ESTADOS_EQUIPO
    )
    
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    motivo = models.TextField(
        blank=True,
        help_text='Motivo del cambio de estado'
    )
    
    class Meta:
        db_table = 'cambios_estado_equipo'
        verbose_name = 'Cambio de Estado'
        verbose_name_plural = 'Cambios de Estado'
        ordering = ['-fecha_cambio']
    
    def __str__(self):
        return f"{self.equipo.codigo}: {self.estado_anterior} → {self.estado_nuevo}"