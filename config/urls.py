# urls.py
# =====================================================
# ARCHIVO: config/urls.py
# =====================================================

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings  # <--- Importa settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('users/', include('apps.users.urls')),
    path('dashboard/', include('apps.equipment.urls')),  # Dashboard principal
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    #path('', RedirectView.as_view(url='/auth/login/', permanent=False)),

]

# =====================================================
# MANEJADOR DE ERRORES
# =====================================================
handler404 = 'config.views.custom_404_view'

# =====================================================
# RUTA DE PRUEBA PARA LA PÁGINA 404 (SOLO DESARROLLO)
# =====================================================
if settings.DEBUG:
    urlpatterns += [
        path('test-404/', views.custom_404_view, kwargs={'exception': Exception('Página no encontrada')}),
        path('auth/test-404/', views.custom_404_view, kwargs={'exception': Exception('Página no encontrada')}),
        path('dashboard/test-404/', views.custom_404_view, kwargs={'exception': Exception('Página no encontrada')}),
    ]
    



