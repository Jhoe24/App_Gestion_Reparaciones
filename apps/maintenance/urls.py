from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('admin/list/', views.AdminMaintenanceListView.as_view(), name='admin_list'),
    path('user/list/', views.UserMaintenanceListView.as_view(), name='user_list'),
    path('desarrollo/', views.under_development_view, name='under_development'),
    path('mantenimiento/', views.maintenance_view, name='maintenance'),
]
