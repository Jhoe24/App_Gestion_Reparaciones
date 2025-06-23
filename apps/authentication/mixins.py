# =====================================================
# ARCHIVO: apps/authentication/mixins.py
# =====================================================

from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages
from typing import cast, List

from apps.users.models import CustomUser


class RoleRequiredMixin(AccessMixin):
    """Mixin para requerir roles específicos en vistas basadas en clases"""
    required_roles: List[str] = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        user = cast(CustomUser, request.user)
        if user.rol not in self.required_roles:
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('equipment:user_dashboard')
        
        return super().dispatch(request, *args, **kwargs)  # type: ignore[misc]


class AdminRequiredMixin(RoleRequiredMixin):
    """Mixin para requerir rol de administrador"""
    required_roles = ['administrador']


class TechRequiredMixin(RoleRequiredMixin):
    """Mixin para requerir rol de técnico o administrador"""
    required_roles = ['administrador', 'tecnico']