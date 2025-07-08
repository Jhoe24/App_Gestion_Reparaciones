from django import forms
from .models import Equipo

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = [
            'codigo', 'tipo_equipo', 'marca', 'modelo', 'numero_serie',
            'ubicacion', 'ubicacion_detalle', 'estado_actual', 'descripcion',
            'especificaciones', 'fecha_adquisicion', 'valor_adquisicion',
            'responsable_actual', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código institucional'}),
            'tipo_equipo': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de serie'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion_detalle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Detalle de ubicación'}),
            'estado_actual': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'especificaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'fecha_adquisicion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_adquisicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'responsable_actual': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'codigo': 'Código',
            'tipo_equipo': 'Tipo de equipo',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'numero_serie': 'Número de serie',
            'ubicacion': 'Ubicación',
            'ubicacion_detalle': 'Detalle de ubicación',
            'estado_actual': 'Estado',
            'descripcion': 'Descripción',
            'especificaciones': 'Especificaciones',
            'fecha_adquisicion': 'Fecha de adquisición',
            'valor_adquisicion': 'Valor de adquisición',
            'responsable_actual': 'Responsable actual',
            'activo': 'Activo',
        }

class EquipoFormUsuario(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = [
            'codigo', 'tipo_equipo', 'marca', 'modelo', 'numero_serie',
            'ubicacion', 'ubicacion_detalle', 'descripcion'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código institucional'}),
            'tipo_equipo': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de serie'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion_detalle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Detalle de ubicación'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'codigo': 'Código',
            'tipo_equipo': 'Tipo de equipo',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'numero_serie': 'Número de serie',
            'ubicacion': 'Ubicación',
            'ubicacion_detalle': 'Detalle de ubicación',
            'descripcion': 'Descripción',
        }
