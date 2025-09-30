from django import forms
from .models import FichaEntrada

class FichaEntradaForm(forms.ModelForm):
    class Meta:
        model = FichaEntrada
        fields = [
            "codigo",
            "tipo_equipo",
            "marca",
            "modelo",
            "numero_serie",
            "ubicacion",
            "dependencia",
            "descripcion",
            "nombre_cliente",
            "apellido_cliente",
            "departamento_cliente",
            "telefono_cliente",
            "correo_cliente",
            "descripcion_falla",
            "tipo_falla",
            "observaciones",
        ]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Código institucional"}),
            "tipo_equipo": forms.Select(attrs={"class": "form-control form-select"}),
            "marca": forms.TextInput(attrs={"class": "form-control", "placeholder": "Marca del equipo"}),
            "modelo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Modelo del equipo"}),
            "numero_serie": forms.TextInput(attrs={"class": "form-control", "placeholder": "Número de serie"}),
            "ubicacion": forms.Select(attrs={"class": "form-control form-select"}),
            "dependencia": forms.TextInput(attrs={"class": "form-control", "placeholder": "Dependencia específica"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción adicional del equipo", "rows": 2}),
            "nombre_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del cliente"}),
            "apellido_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido del cliente"}),
            "departamento_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Departamento del cliente"}),
            "telefono_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono del cliente"}),
            "correo_cliente": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Correo electrónico del cliente"}),
            "descripcion_falla": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción detallada del problema", "rows": 2}),
            "tipo_falla": forms.Select(attrs={"class": "form-control form-select"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "placeholder": "Observaciones adicionales", "rows": 2}),
        }