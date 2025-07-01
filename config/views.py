from django.shortcuts import render

ERROR_CONFIG = {
    400: {
        'error_message': 'Solicitud Incorrecta',
        'error_description': 'Lo sentimos, la solicitud que has realizado es incorrecta.'
    },
    401: {
        'error_message': 'No Autorizado',
        'error_description': 'Lo sentimos, necesitas autenticarte para acceder a esta página.'
    },
    403: {
        'error_message': 'Acceso Denegado',
        'error_description': 'Lo sentimos, no tienes permiso para acceder a esta página.'
    },
    404: {
        'error_message': 'Página no encontrada',
        'error_description': 'Lo sentimos, la página que buscas no existe o ha sido movida.'
    },
    405: {
        'error_message': 'Método No Permitido',
        'error_description': 'El método HTTP utilizado no está permitido para esta solicitud.'
    },
    408: {
        'error_message': 'Tiempo de Espera Agotado',
        'error_description': 'La solicitud ha tardado demasiado tiempo en completarse.'
    },
    429: {
        'error_message': 'Demasiadas Solicitudes',
        'error_description': 'Has realizado demasiadas solicitudes en un corto período de tiempo.'
    },
    500: {
        'error_message': 'Error Interno del Servidor',
        'error_description': 'Ha ocurrido un error interno en el servidor. Por favor, inténtalo de nuevo más tarde.'
    },
    502: {
        'error_message': 'Puerta de Enlace Incorrecta',
        'error_description': 'El servidor recibió una respuesta no válida de otro servidor.'
    },
    503: {
        'error_message': 'Servicio No Disponible',
        'error_description': 'El servicio está temporalmente no disponible. Por favor, inténtalo de nuevo más tarde.'
    },
    504: {
        'error_message': 'Tiempo de Espera de la Puerta de Enlace Agotado',
        'error_description': 'El servidor no recibió una respuesta a tiempo de otro servidor.'
    },
}

def generic_error_view(request, exception=None, status_code=500):
    config = ERROR_CONFIG.get(status_code, ERROR_CONFIG[500])
    context = {
        'error_code': status_code,
        'error_message': config['error_message'],
        'error_description': config['error_description'],
        'actions': [
            {
                'url': '/',
                'label': 'Ir al Inicio',
                'style': 'background-color: #4a90e2; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; margin-right: 10px;'
            },
            {
                'url': 'javascript:history.back()',
                'label': 'Volver Atrás',
                'style': 'background-color: #95a5a6; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px;'
            }
        ]
    }
    return render(request, 'errors/error.html', context, status=status_code)

# Handlers para Django

def custom_400_view(request, exception=None):
    return generic_error_view(request, exception, status_code=400)

def custom_401_view(request, exception=None):
    return generic_error_view(request, exception, status_code=401)

def custom_403_view(request, exception=None):
    return generic_error_view(request, exception, status_code=403)

def custom_404_view(request, exception=None):
    return generic_error_view(request, exception, status_code=404)

def custom_405_view(request, exception=None):
    return generic_error_view(request, exception, status_code=405)

def custom_408_view(request, exception=None):
    return generic_error_view(request, exception, status_code=408)

def custom_429_view(request, exception=None):
    return generic_error_view(request, exception, status_code=429)

def custom_500_view(request, exception=None):
    return generic_error_view(request, exception, status_code=500)

def custom_502_view(request, exception=None):
    return generic_error_view(request, exception, status_code=502)

def custom_503_view(request, exception=None):
    return generic_error_view(request, exception, status_code=503)

def custom_504_view(request, exception=None):
    return generic_error_view(request, exception, status_code=504)
