# urls.py
# =====================================================
# ARCHIVO: equipement/urls.py
# =====================================================
from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns =[
    # Dashboards por rol, ahora protegidos correctamente.
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('tech/', views.TechDashboardView.as_view(), name='tech_dashboard'),
    path('user/', views.CustomDashboardView.as_view(), name='user_dashboard'),
]
