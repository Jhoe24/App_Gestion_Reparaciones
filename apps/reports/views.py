from django.shortcuts import render
from django.views.generic import TemplateView
from apps.authentication.mixins import AdminRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class AdminReportsDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'reports/admin_dashboard.html'

class UserReportsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/user_dashboard.html'
