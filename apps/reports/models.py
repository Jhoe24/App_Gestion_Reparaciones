from django.db import models

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

    # Información del Cliente
    nombre_cliente = models.CharField("Nombre del Cliente", max_length=50)
    apellido_cliente = models.CharField("Apellido del Cliente", max_length=50)
    departamento_cliente = models.CharField("Departamento del Cliente", max_length=100, blank=True)
    telefono_cliente = models.CharField("Teléfono del Cliente", max_length=20, blank=True)
    correo_cliente = models.EmailField("Correo Electrónico del Cliente", blank=True)

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
    observaciones = models.TextField("Observaciones", blank=True)
    fecha_creacion = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre_cliente} {self.apellido_cliente}"
