from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from apps.authentication.mixins import AdminRequiredMixin, TechRequiredMixin
from django.contrib import messages

from apps.equipment.models import SystemConfig
from apps.equipment.forms import SystemConfigForm

from datetime import datetime
from django.utils import timezone
from apps.reports.models import FichaEntrada, Seguimiento
from django.db.models import Q

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
        context['en_reparacion'] = 0
        context['completadas_hoy'] = 0
        context['urgentes'] = 0
        context['actividad_reciente'] = 0
        return context

class TechDashboardView(TechRequiredMixin, CustomDashboardView):
    template_name = 'home/home_dashboard_tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Equipos pendientes (asignados al técnico y en estado pendiente)
        pendientes_states = ['recibido', 'diagnostico', 'en_espera']
        equipos_pendientes = FichaEntrada.objects.filter(tecnico_asignado=user, estado__in=pendientes_states)
        # Equipos en reparación (asignados al técnico y en reparación)
        equipos_en_reparacion = FichaEntrada.objects.filter(tecnico_asignado=user, estado='reparacion')
        # Equipos completados (asignados al técnico y entregados)
        equipos_completados = FichaEntrada.objects.filter(tecnico_asignado=user, estado='entregado')
        # Reportes actuales (seguimientos de equipos a su cargo, últimos 8)
        reportes_actuales = (
            Seguimiento.objects.filter(tecnico=user)
            .select_related('ficha')
            .order_by('-fecha_ingreso')[:8]
        )

        context['equipos_pendientes'] = equipos_pendientes.count()
        context['equipos_en_reparacion'] = equipos_en_reparacion.count()
        context['equipos_completados'] = equipos_completados.count()
        # Lista de reportes actuales para mostrar detalles
        context['reportes_actuales'] = [
            {
                'codigo': r.ficha.codigo,
                'tipo_equipo': r.ficha.get_tipo_equipo_display() if hasattr(r.ficha, 'get_tipo_equipo_display') else '',
                'estado': r.estado,
                'descripcion': r.descripcion,
                'fecha': r.fecha_ingreso,
            }
            for r in reportes_actuales
        ]
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
        # Pasar el formulario para el modal (no hay formulario de usuario definido aquí)
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
        # Métricas dinámicas basadas en la base de datos
        try:
            # Fecha/hora actual
            now = timezone.now()
            today = now.date()

            # Solicitudes pendientes: estados que indican que aún no se ha iniciado reparación
            pendientes_states = ['recibido', 'diagnostico']
            solicitudes_pendientes = FichaEntrada.objects.filter(estado__in=pendientes_states).count()

            # En reparación
            en_reparacion = FichaEntrada.objects.filter(estado='reparacion').count()

            # Completadas hoy: buscamos seguimientos con estado 'entregado' registrados hoy
            completadas_hoy = Seguimiento.objects.filter(estado='entregado', fecha_ingreso__date=today).count()

            # Actividad reciente: últimos seguimientos
            recent_qs = (
                Seguimiento.objects.select_related('ficha', 'tecnico')
                .order_by('-fecha_ingreso')[:8]
            )

            def _human_time(dt):
                delta = timezone.now() - dt
                seconds = int(delta.total_seconds())
                if seconds < 60:
                    return f"Hace {seconds}s"
                minutes = seconds // 60
                if minutes < 60:
                    return f"Hace {minutes}m"
                hours = minutes // 60
                if hours < 24:
                    return f"Hace {hours}h"
                days = hours // 24
                return f"Hace {days}d"

            estado_icon_map = {
                'recepcion': ('pending', 'fa-clock'),
                'diagnostico': ('repair', 'fa-stethoscope'),
                'reparacion': ('in-progress', 'fa-tools'),
                'pruebas': ('completed', 'fa-vial'),
                'listo': ('completed', 'fa-check-circle'),
                'listo_entrega': ('completed', 'fa-check-circle'),
                'entregado': ('completed', 'fa-check-circle'),
                'otro': ('maintenance', 'fa-wrench'),
            }

            actividad = []
            for s in recent_qs:
                estado_key = (s.estado or '').lower()
                icon_cls, fa_icon = estado_icon_map.get(estado_key, ('repair', 'fa-info-circle'))
                title = f"{s.ficha.codigo} - {s.ficha.get_tipo_equipo_display()}"
                desc = s.descripcion or ''
                if not desc and s.timeline:
                    # intentar obtener la última entrada del timeline
                    try:
                        last = list(s.timeline)[-1]
                        desc = last.get('descripcion') or last.get('titulo') or desc
                    except Exception:
                        pass
                actividad.append({
                    'title': title,
                    'description': desc,
                    'time': _human_time(s.fecha_ingreso),
                    'icon': icon_cls,
                    'fa_icon': fa_icon,
                })

            context['solicitudes_pendientes'] = solicitudes_pendientes
            context['en_reparacion'] = en_reparacion
            context['completadas_hoy'] = completadas_hoy
            context['actividad_reciente'] = actividad
        except Exception:
            # En caso de fallo en consulta, devolver valores por defecto
            context['solicitudes_pendientes'] = 0
            context['en_reparacion'] = 0
            context['completadas_hoy'] = 0
            context['actividad_reciente'] = []

        return context
    
    
class ConfiguracionView(AdminRequiredMixin, TemplateView):
    template_name = 'setting/configuracion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = SystemConfig.get_solo()
        context['config'] = config
        context['form'] = SystemConfigForm(instance=config)
        return context

    def post(self, request, *args, **kwargs):
        config = SystemConfig.get_solo()
        form = SystemConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración guardada correctamente.')
            return redirect(request.path)
        else:
            context = self.get_context_data()
            context['form'] = form
            context['config'] = config
            return render(request, self.template_name, context)
    
    
class CongiguracionViewTech(TechRequiredMixin, TemplateView):
    template_name = 'setting/configuracion_tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = SystemConfig.get_solo()
        context['config'] = config
        return context