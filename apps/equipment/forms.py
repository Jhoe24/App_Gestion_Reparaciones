from django import forms
from .models import Equipo

# Opciones comunes para dependencia
DEPENDENCIAS_COMUNES = [
    ('', '---------'),
    ('administracion', 'Administración'),
    ('rectorado', 'Rectorado'),
    ('vicerrectorado_academico', 'Vicerrectorado Académico'),
    ('coordinacion_informatica', 'Coordinación de Informática'),
    ('laboratorio_1', 'Laboratorio 1'),
    ('laboratorio_2', 'Laboratorio 2'),
    ('biblioteca', 'Biblioteca'),
    ('otra', 'Otra Dependencia'),
]

class EquipoForm(forms.ModelForm):
    dependencia = forms.ChoiceField(
        choices=DEPENDENCIAS_COMUNES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'checkDependencia(this)'}),
        label='Dependencia'
    )

    otra_dependencia = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-2',
            'placeholder': 'Otra dependencia (especificar)',
            'style': 'display:none;',
            'id': 'id_otra_dependencia'
        }),
        label=''
    )

    class Meta:
        model = Equipo
        fields = [
            'codigo', 'tipo_equipo', 'marca', 'modelo', 'numero_serie',
            'ubicacion', 'dependencia', 'estado_actual', 'descripcion',
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
            'ubicacion': 'Sede',
            'dependencia': 'Dependencia',
            'estado_actual': 'Estado',
            'descripcion': 'Descripción',
            'especificaciones': 'Especificaciones',
            'fecha_adquisicion': 'Fecha de adquisición',
            'valor_adquisicion': 'Valor de adquisición',
            'responsable_actual': 'Responsable actual',
            'activo': '¿Está funcionando?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si hay un valor en dependencia que no está en las opciones comunes,
        # seleccionamos 'otra' y mostramos el campo de texto
        if self.instance and self.instance.dependencia:
            dependencia = self.instance.dependencia
            # Verificar si la dependencia actual está en las opciones comunes
            dependencias_comunes = [d[0] for d in DEPENDENCIAS_COMUNES if d[0]]
            if dependencia not in dependencias_comunes:
                self.fields['dependencia'].initial = 'otra'
                self.fields['otra_dependencia'].initial = dependencia

    def clean(self):
        cleaned_data = super().clean()
        dependencia = cleaned_data.get('dependencia')
        otra_dependencia = cleaned_data.get('otra_dependencia', '').strip()

        if dependencia == 'otra' and not otra_dependencia:
            self.add_error('otra_dependencia', 'Este campo es obligatorio si se selecciona "Otra Dependencia".')
        elif dependencia != 'otra' and dependencia:  # Si se seleccionó una opción común
            # Buscar el valor legible para humano de la dependencia seleccionada
            dict_dependencias = dict(DEPENDENCIAS_COMUNES)
            cleaned_data['dependencia'] = dict_dependencias.get(dependencia, dependencia)
        elif dependencia == 'otra':  # Si se seleccionó "Otra Dependencia"
            cleaned_data['dependencia'] = otra_dependencia
        else:  # Si no se seleccionó nada (campo vacío)
            cleaned_data['dependencia'] = ''

        return cleaned_data

class EquipoFormUsuario(forms.ModelForm):
    dependencia = forms.ChoiceField(
        choices=DEPENDENCIAS_COMUNES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'checkDependencia(this)'}),
        label='Dependencia'
    )

    otra_dependencia = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-2',
            'placeholder': 'Otra dependencia (especificar)',
            'style': 'display:none;',
            'id': 'id_otra_dependencia'
        }),
        label=''
    )

    class Meta:
        model = Equipo
        fields = [
            'codigo', 'tipo_equipo', 'marca', 'modelo', 'numero_serie',
            'ubicacion', 'dependencia', 'descripcion'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código institucional'}),
            'tipo_equipo': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de serie'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'codigo': 'Código',
            'tipo_equipo': 'Tipo de equipo',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'numero_serie': 'Número de serie',
            'ubicacion': 'Sede',
            'dependencia': 'Dependencia',
            'descripcion': 'Descripción',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.dependencia:
            dependencia = self.instance.dependencia
            dependencias_comunes = [d[0] for d in DEPENDENCIAS_COMUNES if d[0]]
            if dependencia not in dependencias_comunes:
                self.fields['dependencia'].initial = 'otra'
                self.fields['otra_dependencia'].initial = dependencia

    def clean(self):
        cleaned_data = super().clean()
        dependencia = cleaned_data.get('dependencia')
        otra_dependencia = cleaned_data.get('otra_dependencia', '').strip()

        if dependencia == 'otra' and not otra_dependencia:
            self.add_error('otra_dependencia', 'Este campo es obligatorio si se selecciona "Otra Dependencia".')
        elif dependencia != 'otra' and dependencia:  # Si se seleccionó una opción común
            dict_dependencias = dict(DEPENDENCIAS_COMUNES)
            cleaned_data['dependencia'] = dict_dependencias.get(dependencia, dependencia)
        elif dependencia == 'otra':  # Si se seleccionó "Otra Dependencia"
            cleaned_data['dependencia'] = otra_dependencia
        else:  # Si no se seleccionó nada (campo vacío)
            cleaned_data['dependencia'] = ''

        return cleaned_data
