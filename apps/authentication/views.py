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
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.shortcuts import get_object_or_404

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

        # Verificar si el usuario ha verificado su email
        if not user.is_verified:
            messages.error(
                self.request,
                'Debes verificar tu email antes de iniciar sesión. '
                'Revisa tu bandeja de entrada y haz clic en el enlace de verificación.'
            )
            
            # Agregar mensaje adicional con opción de reenvío
            messages.info(
                self.request,
                f'¿No recibiste el email? '
                f'<a href="{reverse_lazy("authentication:resend_verification")}" '
                f'class="alert-link">Reenviar email de verificación</a>'
            )
            
            # Registrar intento de login con usuario no verificado
            log_user_action(
                user=user,
                action='login_unverified',
                ip_address=get_client_ip(self.request),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Marcar que ya se agregaron mensajes
            self._messages_added = True
            return self.form_invalid(form)

        # Verificar si el usuario está activo
        if not user.is_active:
            messages.error(
                self.request,
                'Tu cuenta ha sido desactivada. Contacta al administrador.'
            )
            
            # Registrar intento con cuenta desactivada
            log_user_action(
                user=user,
                action='login_inactive',
                ip_address=get_client_ip(self.request),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Marcar que ya se agregaron mensajes
            self._messages_added = True
            return self.form_invalid(form)

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
        """Login fallido - Solo para credenciales incorrectas"""
        # Solo agregar mensaje si no se agregaron previamente en form_valid
        if not hasattr(self, '_messages_added'):
            # Intentar obtener el usuario para dar mensaje específico
            username = form.cleaned_data.get("username")
            user = None
            
            if username:
                user = CustomUser.objects.filter(
                    Q(email__iexact=username) | Q(username__iexact=username)
                ).first()
                
                if user:
                    # Usuario existe pero credenciales incorrectas
                    messages.error(
                        self.request, 
                        'Contraseña incorrecta. Intenta nuevamente.'
                    )
                else:
                    # Usuario no encontrado
                    messages.error(
                        self.request, 
                        'No se encontró un usuario con esas credenciales.'
                    )
            else:
                # Campo username vacío
                messages.error(
                    self.request, 
                    'Por favor, ingresa tu email o nombre de usuario.'
                )

            # Registrar intento fallido
            log_user_action(
                user=user,
                action='failed_login',
                ip_address=get_client_ip(self.request),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')
            )
        
        return super().form_invalid(form)
    
    def get_success_url(self):
        """Redirección según el rol del usuario"""
        user = cast(CustomUser, self.request.user)
        
        if user.is_superuser or user.is_administrador:
            return reverse_lazy('equipment:admin_dashboard')
        elif user.is_tecnico:
            return reverse_lazy('equipment:tech_dashboard')
        else:
            return reverse_lazy('equipment:user_dashboard')


class CustomLogoutView(LogoutView):
    """Vista personalizada para logout"""
    template_name = 'authentication/logout.html'
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
    
    def get_success_url(self):
        """Redirige al login después del registro exitoso"""
        return reverse_lazy('authentication:login')
    
    def send_verification_email(self, user):
        """Envía el email de verificación"""
        current_site = get_current_site(self.request)
        
        # Generar token de verificación
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Crear el link de verificación
        verification_link = f"http://{current_site.domain}/auth/verify/{uid}/{token}/"
        
        # Contexto para el template
        context = {
            'user': user,
            'domain': current_site.domain,
            'site_name': current_site.name,
            'verification_link': verification_link,
            'protocol': 'https' if self.request.is_secure() else 'http',
        }
        
        # Renderizar el template HTML
        html_message = render_to_string('authentication/verification_email.html', context)
        plain_message = strip_tags(html_message)
        
        # Enviar el email
        send_mail(
            subject='Verifica tu cuenta - Bienvenido a nuestro sistema',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    def form_valid(self, form):
        """Registro exitoso"""
        response = super().form_valid(form)
        
        # Marcar el usuario como no verificado
        self.object.is_verified = False
        self.object.save()
        
        # Enviar email de verificación
        try:
            self.send_verification_email(self.object)
            messages.success(
                self.request,
                '¡Registro exitoso! Te hemos enviado un email de verificación. '
                'Revisa tu bandeja de entrada y haz clic en el enlace para activar tu cuenta.'
            )
            
            # Mensaje adicional para el login
            messages.info(
                self.request,
                'Una vez que hayas verificado tu email, podrás iniciar sesión con tus credenciales.'
            )
            
        except Exception as e:
            messages.error(
                self.request,
                'Error al enviar el email de verificación. Contacta al administrador.'
            )
            print(f"Error sending verification email: {e}")  # Para debugging
        
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


def verify_email(request, uidb64, token):
    """Vista para verificar el email del usuario"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        
        # Registrar verificación exitosa
        log_user_action(
            user=user,
            action='email_verified',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        messages.success(
            request,
            '¡Email verificado exitosamente! Ya puedes iniciar sesión.'
        )
        return redirect('authentication:login')
    else:
        messages.error(
            request,
            'El enlace de verificación es inválido o ha expirado.'
        )
        return redirect('authentication:register')

def resend_verification_email(request):
    """Vista para reenviar email de verificación"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Por favor, ingresa un email válido.')
            return render(request, 'authentication/resend_verification.html')
        
        try:
            # Buscar usuario por email
            user = CustomUser.objects.get(email__iexact=email)
            
            # Verificar si ya está verificado
            if user.is_verified:
                messages.info(
                    request,
                    'Esta cuenta ya ha sido verificada. Puedes iniciar sesión normalmente.'
                )
                return redirect('authentication:login')
            
            # Reenviar email de verificación
            register_view = RegisterView()
            register_view.request = request
            
            try:
                register_view.send_verification_email(user)
                messages.success(
                    request,
                    f'Email de verificación reenviado a {email}. '
                    f'Revisa tu bandeja de entrada y la carpeta de spam.'
                )
                
                # Registrar reenvío
                log_user_action(
                    user=user,
                    action='resend_verification',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
            except Exception as e:
                messages.error(
                    request,
                    'Error al enviar el email. Intenta nuevamente o contacta al administrador.'
                )
                print(f"Error resending verification email: {e}")  # Para debugging
                
        except CustomUser.DoesNotExist:
            # No revelar si el usuario existe o no por seguridad
            messages.info(
                request,
                'Si el email existe en nuestro sistema, se enviará un email de verificación.'
            )
    
    return render(request, 'authentication/resend_verification.html')

class CustomPasswordResetView(PasswordResetView):
    """Vista personalizada para recuperación de contraseña"""
    form_class = CustomPasswordResetForm
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject.txt'
    success_url = reverse_lazy('authentication:password_reset_done')
    
    html_email_template_name = 'authentication/password_reset_email.html' 

    
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