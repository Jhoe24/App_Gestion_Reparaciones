from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView
from apps.authentication.mixins import AdminRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from apps.reports.forms import ReporteForm
from apps.maintenance.models import Reporte
from django.core.exceptions import PermissionDenied

class AdminReportsDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'reports/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reportes'] = Reporte.objects.all().order_by('-fecha_reporte')
        context['reportes_pendientes'] = Reporte.objects.filter(estado_reporte__in=['en_espera', 'asignado', 'en_diagnostico', 'en_mantenimiento', 'esperando_repuestos']).order_by('-fecha_reporte')
        context['reportes_resueltos'] = Reporte.objects.filter(estado_reporte__in=['reparado', 'cerrado', 'no_reparable', 'cancelado']).order_by('-fecha_reporte')
        return context

class UserReportsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reportes'] = Reporte.objects.filter(usuario_reporta=self.request.user).order_by('-fecha_reporte')
        return context

class ReporteCreateView(LoginRequiredMixin, CreateView):
    model = Reporte
    form_class = ReporteForm
    template_name = 'reports/reporte_form.html'
    success_url = reverse_lazy('reports:user_dashboard')

    def form_valid(self, form):
        form.instance.usuario_reporta = self.request.user
        return super().form_valid(form)

class ReporteDetailView(LoginRequiredMixin, DetailView):
    model = Reporte
    template_name = 'reports/reporte_detail.html'
    context_object_name = 'reporte'

    def dispatch(self, request, *args, **kwargs):
        reporte = self.get_object()
        if request.user.is_superuser or getattr(request.user, 'rol', None) == 'administrador':
            return super().dispatch(request, *args, **kwargs)
        if reporte.usuario_reporta == request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied('No tienes permiso para ver este reporte.')
