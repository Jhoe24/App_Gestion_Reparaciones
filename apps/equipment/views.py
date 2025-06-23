from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.users.models import CustomUser
from apps.authentication.mixins import AdminRequiredMixin, TechRequiredMixin
from .models import Equipo


class CustomDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'equipment/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AdminDashboardView(AdminRequiredMixin, CustomDashboardView):
    template_name = 'equipment/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['user_count'] = CustomUser.objects.count()
        context['equipment_count'] = Equipo.objects.count()

        return context    

class TechDashboardView(TechRequiredMixin, CustomDashboardView):
    """Dashboard para Técnicos y Administradores"""

    template_name = 'equipment/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
 