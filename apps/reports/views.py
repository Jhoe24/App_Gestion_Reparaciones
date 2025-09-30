from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView
from apps.authentication.mixins import AdminRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .forms import FichaEntradaForm
from django.contrib import messages

class AdminReportsDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'reports/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reportes'] = 0
        context['reportes_pendientes'] = 0
        context['reportes_resueltos'] = 0
        return context

class UserReportsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reportes'] = 0 #Reporte.objects.filter(usuario_reporta=self.request.user).order_by('-fecha_reporte')
        return context

class ReporteCreateView(LoginRequiredMixin, CreateView):
    model = None
    form_class = None
    template_name = 'reports/reporte_form.html'
    success_url = reverse_lazy('reports:user_dashboard')

    def form_valid(self, form):
        form.instance.usuario_reporta = self.request.user
        return super().form_valid(form)

class ReporteDetailView(LoginRequiredMixin, DetailView):
    model = None
    template_name = 'reports/reporte_detail.html'
    context_object_name = 'reporte'

    def dispatch(self, request, *args, **kwargs):
        reporte = self.get_object()
        if request.user.is_superuser or getattr(request.user, 'rol', None) == 'administrador':
            return super().dispatch(request, *args, **kwargs)
        if reporte.usuario_reporta == request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied('No tienes permiso para ver este reporte.')


@login_required
def ficha_entrada_view(request):
    try:
        if request.method == 'POST':
            form = FichaEntradaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Ficha de entrada creada exitosamente.")
                return redirect('reports:ficha_entrada')
        else:
            form = FichaEntradaForm()
            messages.info(request, "Por favor, completa el formulario para crear una ficha de entrada.")
        return render(request, 'reports/ficha_entrada.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Ocurrió un error al procesar la ficha de entrada: {e}")
        return render(request, 'reports/ficha_entrada.html', {'form': FichaEntradaForm()})