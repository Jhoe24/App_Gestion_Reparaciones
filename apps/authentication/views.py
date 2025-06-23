# =====================================================
# ARCHIVO: apps/authentication/views.py
# =====================================================

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeView, PasswordChangeDoneView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.db.models import Q
from typing import cast

from apps.users.models import CustomUser, LogAcceso
from .forms import (
    CustomAuthenticationForm, CustomUserCreationForm,
    CustomPasswordResetForm, CustomSetPasswordForm,
    CustomPasswordChangeForm, ProfileForm
)
from .utils import get_client_ip, log_user_action


class CustomLoginView(LoginView):
    """Vista personalizada para login"""
    form_class = CustomAuthenticationForm
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Login exitoso"""
        user = cast(CustomUser, form.get_user())

        # Registrar login exitoso
        log_user_action(
            user=user,
            action='login',
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(self.request, f'¡Bienvenido {user.username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Login fallido"""
        # Intentar obtener el usuario para el log
        username = form.cleaned_data.get("username")
        user = None
        if username:
            # El formulario parece usar el campo 'username' para el email, así que verificamos ambos.
            user = CustomUser.objects.filter(
                Q(email__iexact=username) | Q(username__iexact=username)
            ).first()

        # Registrar intento fallido
        log_user_action(
            user=user,
            action='failed_login',
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        
        messages.error(self.request, 'Credenciales incorrectas. Intente nuevamente.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        """Redirección según el rol del usuario"""
        user = cast(CustomUser, self.request.user)
        
        if user.is_administrador:
            return reverse_lazy('equipment:admin_dashboard')
        elif user.is_tecnico:
            return reverse_lazy('equipment:tech_dashboard')
        else:
            return reverse_lazy('equipment:user_dashboard')


class CustomLogoutView(LogoutView):
    """Vista personalizada para logout"""
    template_name = 'authentication/logout.html'
    # Forzar el uso de POST para el logout por seguridad (previene CSRF en logout).
    http_method_names = ['post', 'options']
    
    def post(self, request, *args, **kwargs):
        """Realiza el logout y añade un mensaje de éxito."""
        if request.user.is_authenticated:
            user = cast(CustomUser, request.user)
            log_user_action(
                user=user,
                action='logout',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
        return HttpResponseRedirect(self.get_success_url())


class RegisterView(CreateView):
    """Vista para registro de nuevos usuarios"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('authentication:login')
    
    def form_valid(self, form):
        """Registro exitoso"""
        response = super().form_valid(form)
        
        messages.success(
            self.request,
            '¡Registro exitoso! Ya puedes iniciar sesión con tus credenciales.'
        )
        
        # Registrar creación de usuario
        log_user_action(
            user=self.object,
            action='register',
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        
        return response
    
    def form_invalid(self, form):
        """Registro fallido"""
        messages.error(
            self.request,
            'Error en el registro. Por favor, revise los datos ingresados.'
        )
        return super().form_invalid(form)


class CustomPasswordResetView(PasswordResetView):
    """Vista personalizada para recuperación de contraseña"""
    form_class = CustomPasswordResetForm
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject.txt'
    success_url = reverse_lazy('authentication:password_reset_done')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Se ha enviado un enlace de recuperación a tu correo electrónico.'
        )
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Vista de confirmación de envío de email"""
    template_name = 'authentication/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Vista para confirmar nueva contraseña"""
    form_class = CustomSetPasswordForm
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('authentication:password_reset_complete')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Tu contraseña ha sido restablecida exitosamente.'
        )
        
        user = cast(CustomUser, form.user)
        # Registrar cambio de contraseña
        log_user_action(
            user=user,
            action='password_reset',
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        
        return super().form_valid(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Vista de finalización de recuperación"""
    template_name = 'authentication/password_reset_complete.html'


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Vista para cambio de contraseña"""
    form_class = CustomPasswordChangeForm
    template_name = 'authentication/password_change.html'
    success_url = reverse_lazy('authentication:password_change_done')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Tu contraseña ha sido cambiada exitosamente.'
        )
        
        user = cast(CustomUser, self.request.user)
        # Registrar cambio de contraseña
        log_user_action(
            user=user,
            action='password_change',
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        
        return super().form_valid(form)


class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    """Vista de confirmación de cambio de contraseña"""
    template_name = 'authentication/password_change_done.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    """Vista del perfil de usuario"""
    template_name = 'authentication/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = cast(CustomUser, self.request.user)
        context['user'] = user
        context['recent_logs'] = LogAcceso.objects.filter(
            usuario=user
        )[:10]
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Vista para editar perfil"""
    model = CustomUser
    form_class = ProfileForm
    template_name = 'authentication/profile_edit.html'
    success_url = reverse_lazy('authentication:profile')
    
    def get_object(self, queryset=None):
        return cast(CustomUser, self.request.user)
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Tu perfil ha sido actualizado exitosamente.'
        )
        return super().form_valid(form)
