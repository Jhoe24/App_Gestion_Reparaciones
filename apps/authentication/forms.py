# =====================================================
# ARCHIVO: apps/authentication/forms.py
# =====================================================

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordResetForm,
    SetPasswordForm, PasswordChangeForm
)
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from apps.users.models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    """Formulario personalizado de autenticación"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar campos
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingrese el Usuario',
            'autofocus': True
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        
        # Cambiar labels
        self.fields['username'].label = 'Usuario'
        self.fields['password'].label = 'Contraseña'
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Verificar si el usuario está activo
            try:
                user = CustomUser.objects.get(email=username)
                if not user.activo:
                    raise ValidationError(
                        'Tu cuenta está desactivada. Contacta al administrador.',
                        code='inactive'
                    )
            except CustomUser.DoesNotExist:
                pass
            
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):
    """Formulario personalizado para creación de usuarios"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombres'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos'
        })
    )
    
    nacionalidad = forms.ChoiceField(
        choices=[('V-', 'V-'), ('E-', 'E-')],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select form-control-sm',
            'id': 'nacionalidad'
        })
    )
    
    cedula = forms.CharField(
        max_length=8,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'cedula',
            'maxlength': '8',
            'pattern': '[0-9]{7,8}',
            'required': True
        })
    )
    
    celular = forms.CharField(
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'celular',
            'maxlength': '11',
            'pattern': '[0-9]{11}',
            'required': True
        })
    )
    
    cargo = forms.ChoiceField(
        choices=[
            ('docente', 'Docente'),
            ('coordinador', 'Coordinador'),
            ('administrativo', 'Personal Administrativo'),
            ('tecnico', 'Técnico'),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    activo = forms.BooleanField(
        required=False,
        initial=True,
        label='Usuario activo',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'nacionalidad', 'cedula', 'celular', 'cargo', 'activo', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar campos heredados
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
        
        # Cambiar labels
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['nacionalidad'].label = 'Nacionalidad'
        self.fields['cedula'].label = 'Cédula'
        self.fields['celular'].label = 'Celular'
        self.fields['cargo'].label = 'Cargo'
        self.fields['activo'].label = 'Usuario activo'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Ya existe un usuario con este correo electrónico.')
        return email
    
    def clean_cedula(self):
        nacionalidad = self.cleaned_data.get('nacionalidad', '')
        cedula_num = self.cleaned_data.get('cedula', '')
        
        # Validar que cedula_num no esté vacío
        if not cedula_num:
            raise ValidationError('La cédula es requerida.')
        
        # Validar que sean solo dígitos
        if not cedula_num.isdigit():
            raise ValidationError('La cédula debe contener solo números.')
        
        # Validar longitud
        if len(cedula_num) not in [7, 8]:
            raise ValidationError('La cédula debe tener entre 7 y 8 dígitos numéricos.')
        
        # Formar la cédula completa
        cedula_completa = f"{nacionalidad}{cedula_num}"
        
        # Validar formato completo
        if not cedula_completa.startswith(('V-', 'E-')):
            raise ValidationError('La cédula debe tener el formato V-12345678 o E-12345678')
        
        # Verificar si ya existe en la base de datos
        if CustomUser.objects.filter(cedula=cedula_completa).exists():
            raise ValidationError('Ya existe un usuario con esta cédula.')
        
        return cedula_completa  # Retornar la cédula completa
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Verificar que nacionalidad y cedula estén presentes
        nacionalidad = cleaned_data.get('nacionalidad')
        cedula_num = cleaned_data.get('cedula')
        
        if nacionalidad and cedula_num:
            # Si cedula_num ya es la cédula completa (viene de clean_cedula), no hacer nada
            if not cedula_num.startswith(('V-', 'E-')):
                # Formar la cédula completa
                cedula_completa = f"{nacionalidad}{cedula_num}"
                cleaned_data['cedula'] = cedula_completa
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # La cédula ya viene completa desde clean_cedula()
        user.cedula = self.cleaned_data['cedula']
        user.telefono = self.cleaned_data.get('celular', '')
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.activo = self.cleaned_data.get('activo', True)
        user.rol = 'usuario'  # Asignar rol por defecto
        
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """Formulario para editar usuarios (sin contraseña)"""
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'cedula', 'telefono', 'cargo', 'rol', 'activo')
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'V-12345678'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '04XX-XXXXXXX'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'cedula': 'Cédula de identidad',
            'telefono': 'Teléfono',
            'cargo': 'Cargo',
            'rol': 'Rol',
            'activo': 'Usuario activo',
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un usuario con este correo electrónico.')
        return email
    
    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if CustomUser.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un usuario con esta cédula.')
        return cedula


class CustomPasswordResetForm(PasswordResetForm):
    """Formulario personalizado para recuperación de contraseña"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
        
        self.fields['email'].label = 'Correo electrónico'


class CustomSetPasswordForm(SetPasswordForm):
    """Formulario personalizado para establecer nueva contraseña"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nueva contraseña'
        })
        
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar nueva contraseña'
        })
        
        self.fields['new_password1'].label = 'Nueva contraseña'
        self.fields['new_password2'].label = 'Confirmar nueva contraseña'


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulario personalizado para cambio de contraseña"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña actual'
        })
        
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nueva contraseña'
        })
        
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar nueva contraseña'
        })
        
        self.fields['old_password'].label = 'Contraseña actual'
        self.fields['new_password1'].label = 'Nueva contraseña'
        self.fields['new_password2'].label = 'Confirmar nueva contraseña'


class ProfileForm(forms.ModelForm):
    """Formulario para editar perfil de usuario"""
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'telefono', 'cargo')
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '04XX-XXXXXXX'
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'cargo': 'Cargo',
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un usuario con este correo electrónico.')
        return email
