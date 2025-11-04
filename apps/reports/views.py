from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView
from apps.authentication.mixins import AdminRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .forms import FichaEntradaForm
from django.contrib import messages
from .models import FichaEntrada
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import json
from django.db.models import Q
import openpyxl
from openpyxl.styles import Font, Alignment
import io



CustomUser = get_user_model()


class AdminReportsDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'reports/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reportes'] = 0
        context['reportes_pendientes'] = 0
        context['reportes_resueltos'] = 0
        return context

class UserReportsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reportes'] = 0 #Reporte.objects.filter(usuario_reporta=self.request.user).order_by('-fecha_reporte')
        return context

class ReporteCreateView(LoginRequiredMixin, CreateView):
    model = None
    form_class = None
    template_name = 'reports/reporte_form.html'
    success_url = reverse_lazy('reports:user_dashboard')

    def form_valid(self, form):
        form.instance.usuario_reporta = self.request.user
        return super().form_valid(form)

class ReporteDetailView(LoginRequiredMixin, DetailView):
    model = None
    template_name = 'reports/reporte_detail.html'
    context_object_name = 'reporte'

    def dispatch(self, request, *args, **kwargs):
        reporte = self.get_object()
        if request.user.is_superuser or getattr(request.user, 'rol', None) == 'administrador':
            return super().dispatch(request, *args, **kwargs)
        if reporte.usuario_reporta == request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied('No tienes permiso para ver este reporte.')


@login_required
def ficha_entrada_view(request):
    try:
        if request.method == 'POST':
            form = FichaEntradaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Ficha de entrada creada exitosamente.")
                return redirect('reports:ficha_entrada')
        else:
            form = FichaEntradaForm()
            messages.info(request, "Por favor, completa el formulario para crear una ficha de entrada.")
        return render(request, 'reports/ficha_entrada.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Ocurrió un error al procesar la ficha de entrada: {e}")
        return render(request, 'reports/ficha_entrada.html', {'form': FichaEntradaForm()})

@login_required
def historial_equipos(request):
    search_query = request.GET.get('search', '')
    if search_query:
        registros = FichaEntrada.objects.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre_cliente__icontains=search_query) |
            Q(apellido_cliente__icontains=search_query) |
            Q(cedula_cliente__icontains=search_query) |
            Q(marca__icontains=search_query) |
            Q(modelo__icontains=search_query) |
            Q(dependencia__icontains=search_query) |
            Q(departamento_cliente__icontains=search_query) |
            Q(numero_serie__icontains=search_query) |
            Q(descripcion_falla__icontains=search_query) |
            Q(tipo_falla__icontains=search_query) |
            Q(fecha_creacion__icontains=search_query)
        ).distinct()
    else:
        registros = FichaEntrada.objects.all()
        
    users = CustomUser.objects.filter(rol__in=['tecnico', 'administrador'])

    return render(request, 'reports/historial_equipos.html', {'registros': registros, 'users': users})

@login_required
def get_equipo_details(request, registro_id):
    try:
        registro = FichaEntrada.objects.get(id=registro_id)
        data = {
            'codigo': registro.codigo,
            'tipo_equipo': registro.get_tipo_equipo_display(),
            'marca': registro.marca,
            'modelo': registro.modelo,
            'numero_serie': registro.numero_serie,
            'ubicacion': registro.get_ubicacion_display(),
            'dependencia': registro.dependencia,
            'descripcion': registro.descripcion,
            'nombre_cliente': registro.nombre_cliente,
            'apellido_cliente': registro.apellido_cliente,
            'cedula_cliente': registro.cedula_cliente,
            'departamento_cliente': registro.departamento_cliente,
            'telefono_cliente': registro.telefono_cliente,
            'correo_cliente': registro.correo_cliente,
            'descripcion_falla': registro.descripcion_falla,
            'tipo_falla': registro.get_tipo_falla_display(),
            'observaciones': registro.observaciones,
            'fecha_creacion': registro.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            'tecnico_asignado': registro.tecnico_asignado.get_full_name() if registro.tecnico_asignado else '',
        }
        return JsonResponse(data)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Registro no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def asignar_tecnico(request, registro_id):
    if request.method == 'POST':
        tecnico_id = request.POST.get('tecnico')
        tecnico = CustomUser.objects.get(id=tecnico_id)
        registro = FichaEntrada.objects.get(id=registro_id)
        registro.tecnico_asignado = tecnico  # Asignar la instancia del usuario
        registro.save()
        return redirect('reports:historial_equipos')  # Asegúrate de usar el nombre correcto de la URL
    # Obtener los usuarios con roles de tecnico o administrador
    tecnicos = CustomUser.objects.filter(rol__in=['tecnico', 'administrador'])
    return render(request, 'reports/asignar_tecnico.html', {'tecnicos': tecnicos})

def exportar_datos(request):
    search_query = request.GET.get('search', '')

    # Filtrar los registros (el mismo código que ya tenías)
    if search_query:
        registros = FichaEntrada.objects.filter(
            Q(marca__icontains=search_query) |
            Q(modelo__icontains=search_query) |
            Q(nombre_cliente__icontains=search_query) |
            Q(apellido_cliente__icontains=search_query) |
            Q(departamento_cliente__icontains=search_query) |
            Q(tipo_equipo__icontains=search_query) |
            Q(codigo__icontains=search_query)
        ).distinct()
    else:
        registros = FichaEntrada.objects.all()

    # 1. Crear un nuevo libro de trabajo de Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # 2. Definir el estilo de fuente en negrita
    bold_font = Font(bold=True)

    # 3. Encabezados (Fila 1)
    headers = [
        'Código',
        'Tipo de Equipo',
        'Marca',
        'Modelo',
        'Cliente',
        'Tipo de Falla',
        'Fecha de Creación',
    ]

    # Escribir los encabezados en la primera fila y aplicar negrita
    for col_num, header_title in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col_num, value=header_title)
        cell.font = bold_font  # <--- Aplicar el estilo de negrita

    # 4. Escribir los datos (A partir de la Fila 2)
    row_num = 2
    for registro in registros:
        sheet.cell(row=row_num, column=1, value=registro.codigo)
        sheet.cell(row=row_num, column=2, value=registro.get_tipo_equipo_display())
        sheet.cell(row=row_num, column=3, value=registro.marca)
        sheet.cell(row=row_num, column=4, value=registro.modelo)
        sheet.cell(row=row_num, column=5, value=f"{registro.nombre_cliente} {registro.apellido_cliente}")
        sheet.cell(row=row_num, column=6, value=registro.get_tipo_falla_display())
        sheet.cell(row=row_num, column=7, value=registro.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'))
        row_num += 1

    # 5. Crear la respuesta HTTP para el archivo XLSX
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)

    # Crear la respuesta HTTP con el tipo de contenido correcto para Excel
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="historial_equipos.xlsx"'

    return response



