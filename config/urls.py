# urls.py
# =====================================================
# ARCHIVO: config/urls.py
# =====================================================

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings  # <--- Importa settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('users/', include('apps.users.urls')),
    path('dashboard/', include('apps.equipment.urls')),  # Dashboard principal
    #path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    #path('', RedirectView.as_view(url='/404', permanent=False)),
    path('maintenance/', include(('apps.maintenance.urls', 'maintenance'), namespace='maintenance')),
    path('reports/', include(('apps.reports.urls', 'reports'), namespace='reports')),


]

# =====================================================
# MANEJADOR DE ERRORES
# =====================================================
handler400 = 'config.views.custom_400_view'
handler401 = 'config.views.custom_401_view'
handler403 = 'config.views.custom_403_view'
handler404 = 'config.views.custom_404_view'
handler405 = 'config.views.custom_405_view'
handler408 = 'config.views.custom_408_view'
handler429 = 'config.views.custom_429_view'
handler500 = 'config.views.custom_500_view'
handler502 = 'config.views.custom_502_view'
handler503 = 'config.views.custom_503_view'
handler504 = 'config.views.custom_504_view'
# =====================================================
# RUTA DE PRUEBA PARA LA PÁGINA 404 (SOLO DESARROLLO)
# =====================================================
if settings.DEBUG:
    urlpatterns += [
        path('test-404/', views.custom_404_view, kwargs={'exception': Exception('Página no encontrada')}),
        path('test-500/', views.custom_500_view, kwargs={'exception': Exception('Error interno del servidor')}),
        path('test-403/', views.custom_403_view, kwargs={'exception': Exception('Acceso denegado')}),
        path('test-400/', views.custom_400_view, kwargs={'exception': Exception('Algun error de solicitud')}),
        path('test-405/', views.custom_405_view, kwargs={'exception': Exception('Método no permitido')}),
        path('test-408/', views.custom_408_view, kwargs={'exception': Exception('Tiempo de espera agotado')}),
        path('test-429/', views.custom_429_view, kwargs={'exception': Exception('Demasiadas solicitudes')}),
        path('test-502/', views.custom_502_view, kwargs={'exception': Exception('Puerta de enlace incorrecta')}),
        path('test-503/', views.custom_503_view, kwargs={'exception': Exception('Servicio no disponible')}),
        path('test-504/', views.custom_504_view, kwargs={'exception': Exception('Tiempo de espera de la puerta de enlace agotado')}),
    ]
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




