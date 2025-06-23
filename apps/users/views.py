
# =====================================================
# ARCHIVO: apps/users/views.py
# =====================================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import CustomUser, LogAcceso
from apps.authentication.mixins import AdminRequiredMixin
from apps.authentication.forms import CustomUserCreationForm, ProfileForm


class UserListView(AdminRequiredMixin, ListView):
    """Vista para listar usuarios (solo admin)"""
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = CustomUser.objects.all().order_by('last_name', 'first_name')
        
        # Filtro por búsqueda
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(cedula__icontains=search) |
                Q(username__icontains=search)
            )
        
        # Filtro por rol
        rol = self.request.GET.get('rol')
        if rol:
            queryset = queryset.filter(rol=rol)
        
        # Filtro por estado
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(activo=True)
        elif status == 'inactive':
            queryset = queryset.filter(activo=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['rol_selected'] = self.request.GET.get('rol', '')
        context['status_selected'] = self.request.GET.get('status', '')
        context['roles'] = CustomUser.ROLES
        return context


class UserDetailView(AdminRequiredMixin, DetailView):
    """Vista de detalle de usuario"""
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'user_obj'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_logs'] = LogAcceso.objects.filter(
            usuario=self.object
        )[:10]
        return context


class UserCreateView(AdminRequiredMixin, CreateView):
    """Vista para crear usuario"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuario creado exitosamente.')
        return super().form_valid(form)


class UserUpdateView(AdminRequiredMixin, UpdateView):
    """Vista para editar usuario"""
    model = CustomUser
    form_class = ProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuario actualizado exitosamente.')
        return super().form_valid(form)


class UserDeleteView(AdminRequiredMixin, DeleteView):
    """Vista para eliminar usuario"""
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Variable para cambiar el texto en la plantilla
        context['is_deactivation'] = True
        return context

    def delete(self, request, *args, **kwargs):
        """En lugar de borrar, desactiva al usuario (borrado lógico)."""
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object == request.user:
            messages.error(request, 'No puedes desactivar tu propia cuenta.')
            return redirect(success_url)
 
        self.object.activo = False
        self.object.save()
        messages.success(request, f'El usuario "{self.object.get_full_name()}" ha sido desactivado exitosamente.')
        return redirect(success_url)


@login_required
def toggle_user_status(request, pk):
    """Función para activar/desactivar usuario"""
    if not request.user.is_administrador:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('equipment:user_dashboard')
    
    user = get_object_or_404(CustomUser, pk=pk)
    
    if user == request.user:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
        return redirect('users:user_list')
    
    user.activo = not user.activo
    user.save()
    
    status = "activado" if user.activo else "desactivado"
    messages.success(request, f'Usuario {user.get_full_name()} {status} exitosamente.')
    
    return redirect('users:user_list')