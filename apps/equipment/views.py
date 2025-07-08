from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from apps.users.models import CustomUser
from apps.authentication.mixins import AdminRequiredMixin, TechRequiredMixin
from .models import Equipo
from .forms import EquipoForm, EquipoFormUsuario

class CustomDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'equipment/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipos_reparados'] = str(50) # Equipo.objects.filter(estado='reparado').count()
        context['equipos_espera'] = str(20) #Equipo.objects.filter(estado='espera').count()
        context['solicitudes'] = str(37) #Solicitud.objects.count()   # Ajusta el modelo si tu app usa otro nombre
        context['completados'] = str(17)
        context['equipos_reparados_lista'] = [
            {'nombre': 'Laptop HP', 'tecnico': 'Jose luis', 'estado': 'En espera', 'fecha_solicitud': '2025-05-24'},
            {'nombre': 'Impresora Epson', 'tecnico': 'Carlos', 'estado': 'Reparado', 'fecha_solicitud': '2025-05-24'},
            {'nombre': 'Monitor Samsung', 'tecnico': 'Luis', 'estado': 'Reparado', 'fecha_solicitud': '2025-05-24'},
            ] 
        #Equipo.objects.filter(estado='reparado').order_by('-fecha_reparacion')[:5]
        return context

class AdminDashboardView(AdminRequiredMixin, CustomDashboardView):
    template_name = 'equipment/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipos_reparados'] = str(50) # Equipo.objects.filter(estado='reparado').count()
        context['equipos_espera'] = str(20) #Equipo.objects.filter(estado='espera').count()
        context['solicitudes'] = str(37) #Solicitud.objects.count()   # Ajusta el modelo si tu app usa otro nombre
        context['equipos_reparados_lista'] = [
            {'nombre': 'Laptop HP', 'tecnico': 'Jose luis', 'usuario': 'Maria',  'fecha_reparacion': '2025-06-30'},
            {'nombre': 'Impresora Epson', 'tecnico': 'Carlos', 'usuario': 'Ana', 'fecha_reparacion': '2025-06-28'},
            {'nombre': 'Monitor Samsung', 'tecnico': 'Luis', 'usuario': 'Pedro', 'fecha_reparacion': '2025-06-25'},
        ]
        return context

class TechDashboardView(TechRequiredMixin, CustomDashboardView):
    """Dashboard para Técnicos y Administradores"""

    template_name = 'equipment/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class AdminEquipmentListView(AdminRequiredMixin, TemplateView):
    template_name = 'equipment/admin_equipment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipos'] = Equipo.objects.all()
        context['equipos_reparados'] = Equipo.objects.filter(estado_actual='reparado')
        context['equipos_mantenimiento'] = Equipo.objects.filter(estado_actual='en_mantenimiento')
        context['equipos_espera'] = Equipo.objects.filter(estado_actual__in=['en_espera'])
        return context

class UserEquipmentListView(LoginRequiredMixin, TemplateView):
    template_name = 'equipment/user_equipment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Solo mostrar equipos donde el usuario es responsable_actual
        context['equipos'] = Equipo.objects.filter(responsable_actual=self.request.user)
        # Pasar el formulario para el modal
        from .forms import EquipoFormUsuario
        context['form'] = EquipoFormUsuario()
        return context

class EquipmentCreateView(LoginRequiredMixin, CreateView):
    model = Equipo
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:user_list')

    def get_form_class(self):
        if self.request.user.is_superuser or getattr(self.request.user, 'is_administrador', False):
            return EquipoForm
        return EquipoFormUsuario

    def form_valid(self, form):
        equipo = form.save(commit=False)
        # Asignar responsable actual y creado_por al usuario logueado
        equipo.responsable_actual = self.request.user
        equipo.creado_por = self.request.user
        equipo.save()
        return super().form_valid(form)
