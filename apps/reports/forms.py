from django import forms
from .models import FichaEntrada
import json
from django.core.exceptions import ValidationError

from .models import Seguimiento

class FichaEntradaForm(forms.ModelForm):
    class Meta:
        model = FichaEntrada
        fields = [
            "codigo",
            "tipo_equipo",
            "tipo_equipo_otro",
            "marca",
            "modelo",
            "numero_serie",
            "ubicacion",
            "dependencia",
            "descripcion",
            "nombre_cliente",
            "apellido_cliente",
            "cedula_cliente",
            "departamento_cliente",
            "telefono_cliente",
            "correo_cliente",
            "descripcion_falla",
            "tipo_falla",
            "tipo_falla_otro",
            "observaciones",
        ]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Código institucional"}),
            "tipo_equipo": forms.Select(attrs={"class": "form-control form-select"}),
            "tipo_equipo_otro": forms.TextInput(attrs={"class": "form-control", "placeholder": "Especifica el tipo de equipo"}),
            "marca": forms.TextInput(attrs={"class": "form-control", "placeholder": "Marca del equipo"}),
            "modelo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Modelo del equipo"}),
            "numero_serie": forms.TextInput(attrs={"class": "form-control", "placeholder": "Número de serie"}),
            "ubicacion": forms.Select(attrs={"class": "form-control form-select"}),
            "dependencia": forms.TextInput(attrs={"class": "form-control", "placeholder": "Dependencia específica"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción adicional del equipo", "rows": 2}),
            "nombre_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del cliente"}),
            "apellido_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido del cliente"}),
            "cedula_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Cédula del cliente"}),
            "departamento_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Departamento del cliente"}),
            "telefono_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono del cliente"}),
            "correo_cliente": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Correo del cliente"}),
            "descripcion_falla": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción detallada del problema", "rows": 2}),
            "tipo_falla": forms.Select(attrs={"class": "form-control form-select"}),
            "tipo_falla_otro": forms.TextInput(attrs={"class": "form-control", "placeholder": "Especifica el tipo de falla"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "placeholder": "Observaciones adicionales", "rows": 2}),
        }

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo_equipo')
        otro = cleaned.get('tipo_equipo_otro')
        if tipo == 'otro':
            if not otro:
                raise ValidationError({'tipo_equipo_otro': 'Por favor especifica el tipo de equipo cuando seleccionas "Otro".'})
        else:
            # Si no es 'otro', asegurarse de que no quede texto en tipo_equipo_otro
            cleaned['tipo_equipo_otro'] = ''
        return cleaned


class SeguimientoForm(forms.ModelForm):
    """Formulario para crear/actualizar un Seguimiento.

    Expone el campo `timeline` como un textarea JSON editable llamado `timeline_json`.
    """
    timeline_json = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        required=False,
        label="Timeline (JSON)",
        help_text="Ingresa una lista JSON de eventos. Ej: [{\"fecha\": \"01 Oct 2025\", \"titulo\": \"Equipo Recibido\", ... }]",
    )

    class Meta:
        model = Seguimiento
        fields = [
            "ficha",
            "estado",
            "progreso",
            "fecha_estimada",
            "tecnico",
            "descripcion",
        ]
        widgets = {
            "estado": forms.Select(attrs={"class": "form-control form-select"}),
            "progreso": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100}),
            "fecha_estimada": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "tecnico": forms.Select(attrs={"class": "form-control form-select"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si existe instancia, pre-llenar timeline_json con el JSON formateado
        if self.instance and getattr(self.instance, "timeline", None):
            try:
                self.fields["timeline_json"].initial = json.dumps(self.instance.timeline, ensure_ascii=False, indent=2)
            except Exception:
                # en caso de que el contenido no sea serializable, dejar en blanco
                self.fields["timeline_json"].initial = ""

    def clean_timeline_json(self):
        data = self.cleaned_data.get("timeline_json", "")
        if not data:
            return []
        try:
            parsed = json.loads(data)
            if not isinstance(parsed, list):
                raise forms.ValidationError("El timeline debe ser una lista JSON de eventos.")
            return parsed
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"JSON inválido: {e}")

    def save(self, commit=True):
        instancia = super().save(commit=False)
        # Asignar timeline parseado (si existe)
        timeline = self.cleaned_data.get("timeline_json", [])
        instancia.timeline = timeline
        if commit:
            instancia.save()
        return instancia