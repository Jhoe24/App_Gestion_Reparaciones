from django.http import JsonResponse
from django.views.decorators.http import require_GET
from apps.users.models import CustomUser

@require_GET
def validate_field(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    nacionalidad = request.GET.get('nacionalidad', '')
    response = {'exists': False, 'message': ''}

    if field == 'cedula':
        cedula = f"{nacionalidad}{value}" if nacionalidad and value else value
        if CustomUser.objects.filter(cedula=cedula).exists():
            response['exists'] = True
            response['message'] = 'Ya existe un usuario con esta cédula.'
    elif field == 'email':
        if CustomUser.objects.filter(email=value).exists():
            response['exists'] = True
            response['message'] = 'Ya existe un usuario con este correo electrónico.'
    elif field == 'username':
        if CustomUser.objects.filter(username=value).exists():
            response['exists'] = True
            response['message'] = 'Ya existe un usuario con este nombre de usuario.'
    return JsonResponse(response)
