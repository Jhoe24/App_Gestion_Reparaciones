from django.shortcuts import render
from django.views.generic import TemplateView
from apps.authentication.mixins import AdminRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

class AdminMaintenanceListView(AdminRequiredMixin, TemplateView):
    template_name = 'maintenance/admin_maintenance_list.html'

class UserMaintenanceListView(LoginRequiredMixin, TemplateView):
    template_name = 'maintenance/user_maintenance_list.html'



@login_required
def under_development_view(request):
    context = {
        'estimated_date': (datetime.now() + timedelta(days=30)).strftime('%d de %B, %Y'),
        'progress_percentage': 75,
        'section_name': 'Inventario Avanzado'  # Personalizable
    }
    return render(request, 'errors/chamba.html', context)

# Para diferentes tipos de páginas
@login_required
def maintenance_view(request):
    
    
    if request.user.is_superuser or request.user.role == 'admin':
        template_name = 'errors/chamba.html'
    else:
        template_name = 'errors/chamba_tech.html'

    context = {
        'page_type': 'maintenance',
        'estimated_time': '2 horas',
        'maintenance_reason': 'Actualización de seguridad'
    }
    
    return render(request, template_name, context) 