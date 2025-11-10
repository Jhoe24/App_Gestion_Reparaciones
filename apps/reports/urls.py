from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('dashboard/', views.AdminReportsDashboardView.as_view(), name='dashboard'),
    path('user/dashboard/', views.UserReportsDashboardView.as_view(), name='user_dashboard'),
    path('nuevo/', views.ReporteCreateView.as_view(), name='reporte_create'),
    path('<int:pk>/', views.ReporteDetailView.as_view(), name='reporte_detail'),
    
    path('ficha_entrada/', views.ficha_entrada_view, name='ficha_entrada'),
    path('historial_equipos/', views.historial_equipos, name='historial_equipos'),
    path('get_equipo_details/<int:registro_id>/', views.get_equipo_details, name='get_equipo_details'),
    path('asignar_tecnico/<int:registro_id>/', views.asignar_tecnico, name='asignar_tecnico'),
    path('exportar_datos/', views.exportar_datos, name='exportar_datos'),

    path('ficha/<int:registro_id>/seguimiento/', views.add_seguimiento, name='add_seguimiento'),
    path('timelines/', views.timelines_by_cedula, name='timelines_by_cedula'),

    path('estadisticas/', views.reporte_estadisticas, name='reporte_estadisticas')


]
