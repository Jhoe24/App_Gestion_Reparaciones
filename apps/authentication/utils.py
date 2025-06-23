# =====================================================
# ARCHIVO: apps/authentication/utils.py
# =====================================================

from apps.users.models import LogAcceso


def get_client_ip(request):
    """Obtiene la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_user_action(user, action, ip_address=None, user_agent=''):
    """Registra una acción del usuario en el log"""
    LogAcceso.objects.create(
        usuario=user,
        accion=action,
        direccion_ip=ip_address,
        user_agent=user_agent
    )
