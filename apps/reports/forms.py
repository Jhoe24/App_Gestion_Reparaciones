from django import forms
from apps.maintenance.models import Reporte

class ReporteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control rounded-3'

    class Meta:
        model = Reporte
        fields = [
            'equipo',
            'descripcion_falla',
            'tipo_falla',
            'prioridad',
            'condiciones_falla',
            'pasos_reproducir',
            'intentos_solucion',
            'observaciones',
        ]
        widgets = {
            'descripcion_falla': forms.Textarea(attrs={'rows': 3}),
            'condiciones_falla': forms.Textarea(attrs={'rows': 2}),
            'pasos_reproducir': forms.Textarea(attrs={'rows': 2}),
            'intentos_solucion': forms.Textarea(attrs={'rows': 2}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }
