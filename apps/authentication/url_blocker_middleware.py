from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import resolve
from config import views

LISTA_BLANCA_PREFIX = [
    '/',  # raíz
    '/auth/',
    '/dashboard/',
    '/users/',
    '/reports/',
    '/maintenance/',
    '/static/',
    '/media/',
    '/favicon.ico',
    '/test-',  # para pruebas de errores, mas adelante se eliminará
]

LISTA_NEGRA = [
    #'/admin/',  
]


class URLBlockerMiddleware:
    
    def __init__(self, obtener_respuesta):
        self.obtener_respuesta = obtener_respuesta
        # Verificamos si el middleware está activo

    def __call__(self, solicitud): # Metodo que se llama para cada solicitud
        ruta = solicitud.path

        # DEBUG: Mostrar información del usuario en consola
        print(f"[DEBUG] Ruta: {ruta} | Auth: {solicitud.user.is_authenticated} | Superuser: {getattr(solicitud.user, 'is_superuser', None)} | Admin: {getattr(solicitud.user, 'is_administrador', None)} | User: {getattr(solicitud.user, 'username', None)}")

        # Permitir acceso total a superusuarios y administradores
        if solicitud.user.is_authenticated and (solicitud.user.is_superuser or getattr(solicitud.user, 'is_administrador', False)):
            return self.obtener_respuesta(solicitud)

        if ruta in LISTA_NEGRA:
            return views.custom_403_view(solicitud)

        if not any(ruta.startswith(prefijo) for prefijo in LISTA_BLANCA_PREFIX):
            return views.custom_403_view(solicitud)

        return self.obtener_respuesta(solicitud) # Si la ruta está en la lista blanca, se continúa con el procesamiento de la solicitud