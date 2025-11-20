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
    # Listados por rol
    path('admin/list/', views.AdminEquipmentListView.as_view(), name='admin_list'),
    path('user/list/', views.UserEquipmentListView.as_view(), name='user_list'),
    # Registro de equipos
    path('create/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('admin/panel/', views.AdminPanelView.as_view(), name='admin_panel'),

    path('configuracion/', views.ConfiguracionView.as_view(), name='configuracion'),
    path('configuracion_tech/', views.CongiguracionViewTech.as_view(), name='configuracion_tech'),
]
