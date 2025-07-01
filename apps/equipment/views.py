from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.users.models import CustomUser
from apps.authentication.mixins import AdminRequiredMixin, TechRequiredMixin
from .models import Equipo
#from apps.maintenance.models import Solicitud

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

class UserEquipmentListView(LoginRequiredMixin, TemplateView):
    template_name = 'equipment/user_equipment_list.html'
