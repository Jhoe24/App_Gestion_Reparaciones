from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class FichaEntrada(models.Model):
    # Información del Equipo
    codigo = models.CharField("Código Institucional", max_length=50)
    tipo_equipo = models.CharField(
        "Tipo de Equipo",
        max_length=30,
        choices=[
            ("computadora_escritorio", "Computadora de Escritorio"),
            ("laptop", "Laptop"),
            ("impresora", "Impresora"),
            ("proyector", "Proyector"),
            ("scanner", "Escáner"),
            ("servidor", "Servidor"),
            ("switch", "Switch de Red"),
            ("router", "Router"),
            ("ups", "UPS/Regulador"),
            ("monitor", "Monitor"),
            ("teclado", "Teclado"),
            ("mouse", "Mouse"),
            ("camara", "Cámara Web"),
            ("bocinas", "Bocinas/Altavoces"),
            ("microfono", "Micrófono"),
            ("tablet", "Tablet"),
            ("disco_externo", "Disco Duro Externo"),
            ("otro", "Otro"),
        ]
    )
    marca = models.CharField("Marca", max_length=50, blank=True)
    modelo = models.CharField("Modelo", max_length=50, blank=True)
    numero_serie = models.CharField("Número de Serie", max_length=100, blank=True)
    ubicacion = models.CharField(
        "Ubicación",
        max_length=20,
        choices=[
            ("barinas", "Sede: Barinas"),
            ("barinitas", "Sede: Barinitas"),
            ("pedraza", "Sede: Pedraza"),
            ("socopo", "Sede: Socopó"),
            ("otra", "Otra Sede"),
        ]
    )
    dependencia = models.CharField("Dependencia", max_length=100, blank=True)
    descripcion = models.TextField("Descripción", blank=True)
    # Campo opcional para cuando el usuario elija "otro" en tipo_equipo
    tipo_equipo_otro = models.CharField("Tipo de Equipo (otro)", max_length=100, blank=True)
    # Información del Cliente
    nombre_cliente = models.CharField("Nombre del Cliente", max_length=50)
    apellido_cliente = models.CharField("Apellido del Cliente", max_length=50)
    cedula_cliente = models.CharField("Cédula del Cliente", max_length=20, blank=True)
    departamento_cliente = models.CharField("Departamento del Cliente", max_length=100, blank=True)
    telefono_cliente = models.CharField("Teléfono del Cliente", max_length=20, blank=True)
    correo_cliente = models.EmailField("Correo del Cliente", blank=True)
    # Información del Reporte
    descripcion_falla = models.TextField("Descripción de la Falla")
    tipo_falla = models.CharField(
        "Tipo de Falla",
        max_length=30,
        choices=[
            ("hardware", "Falla de Hardware"),
            ("software", "Falla de Software"),
            ("conectividad", "Problemas de Conectividad"),
            ("rendimiento", "Problemas de Rendimiento"),
            ("configuracion", "Problemas de Configuración"),
            ("mantenimiento_preventivo", "Mantenimiento Preventivo"),
            ("actualizacion", "Actualización/Upgrade"),
            ("limpieza", "Limpieza"),
            ("otro", "Otro"),
        ]
    )
    tipo_falla_otro = models.CharField("Tipo de Falla (otro)", max_length=100, blank=True)
    observaciones = models.TextField("Observaciones", blank=True)
    # los estados son recivido, en diagnostico, en reparacion, pruebas de calidad, listo para entrega, entregado
    ESTADOS_CHOICES = [
        ("recibido", "Recibido"),
        ("diagnostico", "En Diagnóstico"),
        ("reparacion", "En Reparación"),
        ("pruebas_calidad", "Pruebas de Calidad"),
        ("listo_entrega", "Listo para Entrega"),
        ("entregado", "Entregado"),
    ] 
    estado = models.CharField("Estado", max_length=20, choices=ESTADOS_CHOICES, default="recibido")
    fecha_creacion = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    tecnico_asignado = models.ForeignKey(
            CustomUser,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='fichas_asignadas',
            verbose_name="Técnico Asignado"
        )
    def __str__(self):
        # Mostrar el tipo de equipo personalizado si existe
        tipo = self.get_tipo_equipo_display()
        if self.tipo_equipo == 'otro' and self.tipo_equipo_otro:
            tipo = self.tipo_equipo_otro
        return f"{self.codigo} - {self.nombre_cliente} {self.apellido_cliente} ({tipo})"


class Seguimiento(models.Model):
    """Modelo para llevar el seguimiento / reporte del equipo relacionado con una FichaEntrada.

    Se utiliza un JSONField llamado `timeline` para almacenar una lista de eventos
    (fecha, título, descripción, estado, icono), tal como en el ejemplo provisto.
    """
    ESTADO_CHOICES = [
        ("recepcion", "Recepción"),
        ("diagnostico", "Diagnóstico"),
        ("reparacion", "Reparación"),
        ("pruebas", "Pruebas de Calidad"),
        ("listo", "Listo para Entrega"),
        ("entregado", "Entregado"),
        ("otro", "Otro"),
    ]

    ficha = models.ForeignKey(
        FichaEntrada,
        on_delete=models.CASCADE,
        related_name="seguimientos",
        verbose_name="Ficha de Entrada",
    )
    estado = models.CharField("Estado", max_length=30, choices=ESTADO_CHOICES, default="recepcion")
    progreso = models.PositiveSmallIntegerField("Progreso (%)", default=0)
    fecha_ingreso = models.DateTimeField("Fecha de Ingreso", auto_now_add=True)
    fecha_estimada = models.DateField("Fecha Estimada", null=True, blank=True)
    tecnico = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seguimientos_asignados",
        verbose_name="Técnico asignado",
    )
    descripcion = models.TextField("Descripción general", blank=True)
    # Usamos JSONField para guardar el timeline como una lista de objetos
    timeline = models.JSONField("Timeline", default=list, blank=True)
    # Ejemplo de como se guardaria en el timeline:
    # [
    #     {
    #         "fecha": "2025-10-01T10:00:00",
    #         "titulo": "Equipo Recibido",
    #         "descripcion": "El equipo ha sido recibido en el taller.",
    #         "estado": "completed",
    #         "icono": "check-circle"
    #     },
    #     {
    #         "fecha": "2025-10-02T14:30:00",
    #         "titulo": "Diagnóstico Realizado",
    #         "descripcion": "Se ha completado el diagnóstico y se identificaron los problemas.",
    #         "estado": "completed",
    #         "icono": "stethoscope"
    #     },
    #     ...
    # ]                     
    # Video opcional subido junto al seguimiento. Se recortará a los primeros 10 segundos al guardarse.
    video = models.FileField(
        "Video (opcional)",
        upload_to='seguimientos/videos/',
        null=True,
        blank=True,
        help_text='Sube un video opcional. Si es más largo, se recortará a los primeros 10 segundos.'
    )

    class Meta:
        verbose_name = "Seguimiento"
        verbose_name_plural = "Seguimientos"
        ordering = ["-fecha_ingreso"]

    def __str__(self):
        codigo = self.ficha.codigo if self.ficha else "-"
        return f"Seguimiento {codigo} - {self.get_estado_display()} ({self.progreso}%)"

    def add_event(self, fecha, titulo, descripcion, estado="pending", icono=""):
        """Conveniencia para añadir un evento al timeline y guardar el modelo."""
        evento = {
            "fecha": fecha,
            "titulo": titulo,
            "descripcion": descripcion,
            "estado": estado,
            "icono": icono,
        }
        timeline = list(self.timeline or [])
        timeline.append(evento)
        self.timeline = timeline
        self.save()


class QueuedEmail(models.Model):
    """Modelo simple para encolar correos a reenviar en background si el envío directo falla.

    Campos:
    - to: lista de destinatarios (JSON)
    - subject: asunto
    - body_text: texto plano
    - body_html: HTML (opcional)
    - attempts: número de intentos realizados
    - last_error: último error registrado (texto)
    - send_after: datetime opcional para esperar antes de reintentar
    - sent: si ya se envió
    - sent_at: datetime de envío
    """
    to = models.JSONField("Destinatarios", default=list)
    subject = models.CharField("Asunto", max_length=255)
    body_text = models.TextField("Cuerpo (texto)")
    body_html = models.TextField("Cuerpo (html)", blank=True)
    attempts = models.PositiveSmallIntegerField("Intentos", default=0)
    last_error = models.TextField("Último error", blank=True)
    send_after = models.DateTimeField("Reintentar después de", null=True, blank=True)
    sent = models.BooleanField("Enviado", default=False)
    sent_at = models.DateTimeField("Fecha de envío", null=True, blank=True)
    created_at = models.DateTimeField("Creado en", auto_now_add=True)

    class Meta:
        verbose_name = "Correo en cola"
        verbose_name_plural = "Correos en cola"

    def __str__(self):
        return f"QueuedEmail to={','.join(self.to or [])} sent={self.sent} attempts={self.attempts}"
        
