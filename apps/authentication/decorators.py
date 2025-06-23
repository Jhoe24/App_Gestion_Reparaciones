# =====================================================
# ARCHIVO: apps/authentication/decorators.py
# =====================================================

from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """Decorador para requerir roles específicos"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.rol in roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'No tienes permisos para acceder a esta página.')
                return redirect('equipment:user_dashboard')
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """Decorador para requerir rol de administrador"""
    return role_required('administrador')(view_func)


def tech_required(view_func):
    """Decorador para requerir rol de técnico o administrador"""
    return role_required('administrador', 'tecnico')(view_func)

