from django.shortcuts import render
from django.views.generic import TemplateView
from apps.authentication.mixins import AdminRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class AdminMaintenanceListView(AdminRequiredMixin, TemplateView):
    template_name = 'maintenance/admin_maintenance_list.html'

class UserMaintenanceListView(LoginRequiredMixin, TemplateView):
    template_name = 'maintenance/user_maintenance_list.html'

# Create your views here.
