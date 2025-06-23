from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Reporte(models.Model):
    """
    Modelo para los reportes de mantenimiento de equipos
    """
    
    # Estados del reporte
    ESTADOS_REPORTE = [
        ('en_espera', 'En Espera'),
        ('asignado', 'Asignado a Técnico'),
        ('en_diagnostico', 'En Diagnóstico'),
        ('en_mantenimiento', 'En Mantenimiento'),
        ('esperando_repuestos', 'Esperando Repuestos'),
        ('reparado', 'Reparado'),
        ('no_reparable', 'No Reparable'),
        ('cerrado', 'Cerrado'),
        ('cancelado', 'Cancelado'),
    ]
    
    # Prioridades del reporte
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    
    # Tipos de falla más comunes
    TIPOS_FALLA = [
        ('hardware', 'Falla de Hardware'),
        ('software', 'Falla de Software'),
        ('conectividad', 'Problemas de Conectividad'),
        ('rendimiento', 'Problemas de Rendimiento'),
        ('configuracion', 'Problemas de Configuración'),
        ('mantenimiento_preventivo', 'Mantenimiento Preventivo'),
        ('actualizacion', 'Actualización/Upgrade'),
        ('limpieza', 'Limpieza'),
        ('otro', 'Otro'),
    ]
    
    # Campos principales
    numero_reporte = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text='Número único del reporte (generado automáticamente)'
    )
    
    equipo = models.ForeignKey(
        'equipment.Equipo',
        on_delete=models.CASCADE,
        related_name='reportes',
        help_text='Equipo reportado'
    )
    
    usuario_reporta = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reportes_creados',
        help_text='Usuario que reporta la falla'
    )
    
    tecnico_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reportes_asignados',
        limit_choices_to={'rol': 'tecnico'},
        help_text='Técnico asignado para la reparación'
    )
    
    fecha_reporte = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora del reporte'
    )
    
    descripcion_falla = models.TextField(
        help_text='Descripción detallada del problema reportado'
    )
    
    tipo_falla = models.CharField(
        max_length=30,
        choices=TIPOS_FALLA,
        default='otro',
        help_text='Tipo de falla reportada'
    )
    
    estado_reporte = models.CharField(
        max_length=20,
        choices=ESTADOS_REPORTE,
        default='en_espera',
        help_text='Estado actual del reporte'
    )
    
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDADES,
        default='media',
        help_text='Prioridad del reporte'
    )
    
    # Información adicional
    condiciones_falla = models.TextField(
        blank=True,
        help_text='Condiciones en las que se presenta la falla'
    )
    
    pasos_reproducir = models.TextField(
        blank=True,
        help_text='Pasos para reproducir la falla'
    )
    
    intentos_solucion = models.TextField(
        blank=True,
        help_text='Intentos de solución realizados por el usuario'
    )
    
    observaciones = models.TextField(
        blank=True,
        help_text='Observaciones adicionales'
    )
    
    # Fechas importantes
    fecha_asignacion = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha de asignación a técnico'
    )
    
    fecha_inicio_reparacion = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha de inicio de reparación'
    )
    
    fecha_finalizacion = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha de finalización'
    )
    
    # Calificación del servicio
    calificacion_servicio = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text='Calificación del servicio (1-5 estrellas)'
    )
    
    comentario_calificacion = models.TextField(
        blank=True,
        help_text='Comentario sobre la calificación del servicio'
    )
    
    # Campos de auditoría
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'reportes'
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-fecha_reporte']
        indexes = [
            models.Index(fields=['numero_reporte']),
            models.Index(fields=['estado_reporte']),
            models.Index(fields=['prioridad']),
            models.Index(fields=['fecha_reporte']),
            models.Index(fields=['tecnico_asignado']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.numero_reporte:
            # Generar número de reporte automáticamente
            año_actual = timezone.now().year
            ultimo_numero = Reporte.objects.filter(
                numero_reporte__startswith=f'RPT-{año_actual}'
            ).count()
            self.numero_reporte = f'RPT-{año_actual}-{ultimo_numero + 1:04d}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero_reporte} - {self.equipo.codigo} ({self.get_estado_reporte_display()})"
    
    def get_estado_reporte_display(self):
        """Returns the human-readable display value for the estado_reporte field."""
        return dict(self.ESTADOS_REPORTE).get(self.estado_reporte, self.estado_reporte)
    
    @property
    def tiempo_transcurrido(self):
        """Calcula el tiempo transcurrido desde el reporte"""
        if self.fecha_finalizacion:
            return self.fecha_finalizacion - self.fecha_reporte
        return timezone.now() - self.fecha_reporte
    
    @property
    def esta_vencido(self):
        """Determina si el reporte está vencido según la prioridad"""
        dias_limite = {
            'critica': 1,
            'alta': 3,
            'media': 7,
            'baja': 15
        }
        
        if self.estado_reporte in ['reparado', 'cerrado', 'cancelado']:
            return False
        
        dias_transcurridos = self.tiempo_transcurrido.days
        return dias_transcurridos > dias_limite.get(self.prioridad, 7)
    
    @property
    def puede_ser_calificado(self):
        """Determina si el reporte puede ser calificado"""
        return self.estado_reporte in ['reparado', 'cerrado'] and not self.calificacion_servicio
    
    def asignar_tecnico(self, tecnico, usuario_asigna=None):
        """Asigna un técnico al reporte"""
        if tecnico.rol != 'tecnico':
            raise ValueError("Solo se pueden asignar usuarios con rol de técnico")
        
        self.tecnico_asignado = tecnico
        self.estado_reporte = 'asignado'
        self.fecha_asignacion = timezone.now()
        self.save()
        
        # Crear registro en el historial
        HistorialReparacion.objects.create(
            reporte=self,
            fecha_evento=timezone.now(),
            tipo_evento='asignacion',
            descripcion=f'Reporte asignado al técnico {tecnico.get_full_name()}',
            usuario=usuario_asigna
        )


class HistorialReparacion(models.Model):
    """
    Modelo para el historial detallado de reparaciones
    """
    
    TIPOS_EVENTO = [
        ('creacion', 'Creación del Reporte'),
        ('asignacion', 'Asignación a Técnico'),
        ('inicio_diagnostico', 'Inicio de Diagnóstico'),
        ('diagnostico_completado', 'Diagnóstico Completado'),
        ('inicio_reparacion', 'Inicio de Reparación'),
        ('pausa_reparacion', 'Pausa en Reparación'),
        ('continuacion_reparacion', 'Continuación de Reparación'),
        ('solicitud_repuestos', 'Solicitud de Repuestos'),
        ('instalacion_repuestos', 'Instalación de Repuestos'),
        ('pruebas', 'Realización de Pruebas'),
        ('reparacion_completada', 'Reparación Completada'),
        ('no_reparable', 'Declarado No Reparable'),
        ('entrega_equipo', 'Entrega del Equipo'),
        ('cierre_reporte', 'Cierre del Reporte'),
        ('reapertura', 'Reapertura del Reporte'),
        ('cancelacion', 'Cancelación del Reporte'),
        ('otro', 'Otro Evento'),
    ]
    
    reporte = models.ForeignKey(
        Reporte,
        on_delete=models.CASCADE,
        related_name='historial'
    )
    
    fecha_evento = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora del evento'
    )
    
    tipo_evento = models.CharField(
        max_length=30,
        choices=TIPOS_EVENTO,
        help_text='Tipo de evento registrado'
    )
    
    descripcion = models.TextField(
        help_text='Descripción detallada del evento'
    )
    
    diagnostico_tecnico = models.TextField(
        blank=True,
        help_text='Diagnóstico técnico detallado'
    )
    
    acciones_realizadas = models.TextField(
        blank=True,
        help_text='Acciones específicas realizadas'
    )
    
    repuestos_utilizados = models.TextField(
        blank=True,
        help_text='Lista de repuestos utilizados'
    )
    
    tiempo_empleado = models.DurationField(
        null=True,
        blank=True,
        help_text='Tiempo empleado en horas y minutos'
    )
    
    costo_repuestos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Costo de los repuestos utilizados'
    )
    
    observaciones = models.TextField(
        blank=True,
        help_text='Observaciones adicionales'
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Usuario que registra el evento'
    )
    
    # Archivos adjuntos (fotos, documentos)
    archivo_adjunto = models.FileField(
        upload_to='historial_reparaciones/',
        null=True,
        blank=True,
        help_text='Archivo adjunto (foto, documento, etc.)'
    )
    
    class Meta:
        db_table = 'historial_reparaciones'
        verbose_name = 'Historial de Reparación'
        verbose_name_plural = 'Historiales de Reparación'
        ordering = ['-fecha_evento']
        indexes = [
            models.Index(fields=['reporte', '-fecha_evento']),
            models.Index(fields=['tipo_evento']),
        ]
    
    def __str__(self):
        return f"{self.reporte.numero_reporte} - {self.get_tipo_evento_display()} - {self.fecha_evento}"

    def get_tipo_evento_display(self):
        """Returns the human-readable display value for the tipo_evento field."""
        return dict(self.TIPOS_EVENTO).get(self.tipo_evento, self.tipo_evento)


class Repuesto(models.Model):
    """
    Modelo para gestionar los repuestos utilizados
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    codigo_parte = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=50)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.CharField(max_length=100, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'repuestos'
        verbose_name = 'Repuesto'
        verbose_name_plural = 'Repuestos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo_parte})"
    
    @property
    def necesita_restock(self):
        return self.stock_actual <= self.stock_minimo