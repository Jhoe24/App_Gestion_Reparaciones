from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from apps.authentication.mixins import AdminRequiredMixin, TechRequiredMixin

from datetime import datetime

class CustomDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home_dashboard_tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipos_reparados'] = str(50) # Equipo.objects.filter(estado='reparado').count()
        context['equipos_espera'] = str(20) #Equipo.objects.filter(estado='espera').count()
        context['solicitudes'] = str(37) #Solicitud.objects.count()
        context['completados'] = str(17)
        context['equipos_reparados_lista'] = [
            {'nombre': 'Laptop HP', 'tecnico': 'Jose luis', 'estado': 'En espera', 'fecha_solicitud': '2025-05-24'},
            {'nombre': 'Impresora Epson', 'tecnico': 'Carlos', 'estado': 'Reparado', 'fecha_solicitud': '2025-05-24'},
            {'nombre': 'Monitor Samsung', 'tecnico': 'Luis', 'estado': 'Reparado', 'fecha_solicitud': '2025-05-24'},
        ]
        return context

class AdminDashboardView(AdminRequiredMixin, CustomDashboardView):
    template_name = 'equipment/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Solicitudes_Pendientes'] = 0
        context['en_repacion'] = 0
        context['completadas_hoy'] = 0
        context['urgentes'] = 0
        context['actividad_reciente'] = 0
        return context

class TechDashboardView(TechRequiredMixin, CustomDashboardView):
    template_name = 'home/home_dashboard_tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AdminEquipmentListView(AdminRequiredMixin, TemplateView):
    template_name = 'equipment/admin_equipment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todos los equipos
        equipos = None#Equipo.objects.all()
        # Obtener parámetros de búsqueda
        #responsable_search = self.request.GET.get('responsable', '')
        #if responsable_search:
           # equipos = 0#equipos.filter(responsable_actual__username__icontains=responsable_search)
        context['equipos'] = 0#equipos
        context['equipos_reparados'] = 0#equipos.filter(estado_actual='reparado')
        context['equipos_mantenimiento'] = 0#equipos.filter(estado_actual='en_mantenimiento')
        context['equipos_espera'] = 0#equipos.filter(estado_actual__in=['en_espera'])
        context['responsable_search'] = 0#responsable_search
        return context

class UserEquipmentListView(LoginRequiredMixin, TemplateView):
    template_name = 'equipment/user_equipment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Solo mostrar equipos donde el usuario es responsable_actual
        context['equipos'] = 0#Equipo.objects.filter(responsable_actual=self.request.user)
        # Pasar el formulario para el modal
        from .forms import EquipoFormUsuario
        context['form'] = None
        return context

class EquipmentCreateView(LoginRequiredMixin, CreateView):
    model = None
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:user_list')

    def get_form_class(self):
        if self.request.user.is_superuser or getattr(self.request.user, 'is_administrador', False):
            return None
        return None

    def form_valid(self, form):
        equipo = form.save(commit=False)
        # Asignar responsable actual y creado_por al usuario logueado
        equipo.responsable_actual = self.request.user
        equipo.creado_por = self.request.user
        equipo.save()
        return super().form_valid(form)

class AdminPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'home/home_dashboard_admin.html'

    def test_func(self):
        return self.request.user.is_superuser or getattr(self.request.user, 'is_administrador', False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['nombre'] = user.first_name
        context['apellido'] = user.last_name
        context['email'] = user.email
        context['username'] = user.username
        # Agrega aquí cualquier otro dato necesario
        return context
