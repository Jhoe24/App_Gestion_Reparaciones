// Datos de ejemplo
const equiposData = {
    '12345678': [
        {
            id: 'UPT-2025-0089',
            nombre: 'Laptop Dell Latitude 5420',
            modelo: 'Intel Core i7 - 16GB RAM',
            estado: 'reparacion',
            progreso: 60,
            fechaIngreso: '01 Oct 2025',
            fechaEstimada: '',//'10 Oct 2025',
            timeline: [
                {
                    fecha: '01 Oct 2025 - 09:30 AM',
                    titulo: 'Equipo Recibido',
                    descripcion: 'Tu equipo ha sido recibido en nuestro centro de servicio y registrado en el sistema.',
                    estado: 'completed',
                    icono: '📦'
                },
                {
                    fecha: '02 Oct 2025 - 02:15 PM',
                    titulo: 'Asignación de Técnico',
                    descripcion: 'Un técnico ha sido asignado para diagnosticar el problema.',
                    estado: 'completed',
                    icono: '👨‍🔧'
                },
                {
                    fecha: '05 Oct 2025 - 10:00 AM',
                    titulo: 'En Reparación',
                    descripcion: 'Instalación de disco SSD nuevo de 512GB. Clonación de datos en proceso.',
                    estado: 'active',
                    icono: '🔧'
                },
                {
                    fecha: '',//'Estimado: 08 Oct 2025',
                    titulo: 'Pruebas de Calidad',
                    descripcion: 'Verificación de funcionamiento y pruebas de rendimiento.',
                    estado: 'pending',
                    icono: '✅'
                },
                {
                    fecha: '',//'Estimado: 10 Oct 2025',
                    titulo: 'Listo para Entrega',
                    descripcion: 'Equipo reparado y disponible para retiro en ventanilla.',
                    estado: 'pending',
                    icono: '📦'
                }
            ]
        }
    ],
    '87654321': [
        {
            id: 'UPT-2025-0067',
            nombre: 'Impresora HP LaserJet Pro M404dn',
            modelo: 'Láser Monocromática',
            estado: 'completado',
            progreso: 100,
            fechaIngreso: '25 Sep 2025',
            fechaEstimada: '',//'30 Sep 2025',
            timeline: [
                {
                    fecha: '25 Sep 2025 - 10:00 AM',
                    titulo: 'Equipo Recibido',
                    descripcion: 'Impresora recibida con problema de atasco constante de papel.',
                    estado: 'completed',
                    icono: '📦'
                },
                {
                    fecha: '28 Sep 2025 - 11:00 AM',
                    titulo: 'Asignación de Técnico',
                    descripcion: 'Un técnico ha sido asignado para diagnosticar el problema.',
                    estado: 'completed',
                    icono: '👨‍🔧'
                },
                {
                    fecha: '30 Sep 2025 - 08:00 AM',
                    titulo: 'Listo para Entrega',
                    descripcion: '✅ Equipo disponible para retiro. Ventanilla de atención: Lunes a Viernes 8AM-5PM',
                    estado: 'completed',
                    icono: '📦'
                }
            ]
        }
    ]
};

// Función para buscar equipos
function buscarEquipos() {
    const cedula = document.getElementById('cedulaInput').value.trim();
    if (!cedula) {
        alert('⚠️ Por favor ingresa tu número de cédula');
        return;
    }
    if (cedula.length < 6) {
        alert('⚠️ Ingresa un número de cédula válido');
        return;
    }
    // Llamada al endpoint del backend que devuelve fichas y timelines por cédula
    fetch(`/reports/timelines/?cedula=${encodeURIComponent(cedula)}`, { method: 'GET', credentials: 'same-origin' })
        .then(resp => resp.json())
        .then(data => {
            if (data && data.success && Array.isArray(data.fichas) && data.fichas.length > 0) {
                // Adaptar la respuesta al formato que espera mostrarResultados
                const equipos = data.fichas.map(f => ({
                    id: f.codigo || `ID-${f.id}`,
                    nombre: f.tipo_equipo || f.codigo,
                    modelo: f.modelo || '',
                    estado: (f.estado || 'recibido').toLowerCase(),
                    progreso: f.progreso || 0,
                    fechaIngreso: f.fechaIngreso || '',
                    fechaEstimada: f.fechaEstimada || '',
                    timeline: f.timeline || [],
                }));
                mostrarResultados(equipos, cedula);
            } else {
                mostrarSinResultados(cedula);
            }
        })
        .catch(err => {
            console.error('Error obteniendo timelines:', err);
            alert('Ocurrió un error al consultar el estado. Intenta nuevamente.');
        });
}

// Función para mostrar resultados
function mostrarResultados(equipos, cedula) {
    const modalOverlay = document.getElementById('modalOverlay');
    const modalBody = document.getElementById('modalBody');
    const cedulaInfo = document.getElementById('cedulaInfo');

    cedulaInfo.textContent = `CI: ${cedula} • ${equipos.length} equipo(s) registrado(s)`;
    let html = '';
    equipos.forEach((equipo) => {
        const estadoTexto = {
            'recibido': 'Recibido',
            'diagnostico': 'En Diagnóstico',
            'reparacion': 'En Reparación',
            'completado': 'Completado'
        };
        html += `
            <div class="equipment-card">
                <div class="equipment-header">
                    <div class="equipment-info">
                        <h3>${equipo.nombre}</h3>
                        <span class="equipment-code">${equipo.id}</span>
                        <p style="color: #6b7280; margin-top: 8px; font-size: 0.95rem;">${equipo.modelo}</p>
                    </div>
                    <span class="status-badge status-${equipo.estado}">${estadoTexto[equipo.estado]}</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${equipo.progreso}%"></div>
                    </div>
                    <div class="progress-info">
                        <span><strong>Ingreso:</strong> ${equipo.fechaIngreso}</span>
                        <span><strong>Entrega estimada:</strong> ${equipo.fechaEstimada}</span>
                    </div>
                </div>
                <div class="timeline">
        `;
        equipo.timeline.forEach(item => {
            // icono por estado si no viene
            const estadoIcon = (item.icono) ? item.icono : (item.estado === 'recepcion' ? '📦' : (item.estado === 'diagnostico' ? '🔍' : (item.estado === 'reparacion' ? '🔧' : (item.estado === 'pruebas' ? '✅' : '📌'))));
            // Mostrar fecha tal cual (backend envía ISO o texto formateado)
            const fechaTexto = item.fecha || '';
            html += `
                <div class="timeline-item ${item.estado}">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-date">${fechaTexto}</div>
                        <div class="timeline-title">${estadoIcon} ${item.titulo}</div>
                        <div class="timeline-desc">${item.descripcion || ''}</div>
                        ${item.video ? (`<div class="timeline-video"><a href="${item.video}" target="_blank">Ver video</a></div>`) : ''}
                    </div>
                </div>
            `;
        });
        html += `
                </div>
            </div>
        `;
    });
    modalBody.innerHTML = html;
    modalOverlay.style.display = 'block';
}

// Función para mostrar sin resultados
function mostrarSinResultados(cedula) {
    const modalOverlay = document.getElementById('modalOverlay');
    const modalBody = document.getElementById('modalBody');
    const cedulaInfo = document.getElementById('cedulaInfo');

    cedulaInfo.textContent = `CI: ${cedula}`;
    modalBody.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">📦</div>
            <h3>No se encontraron equipos</h3>
            <p>No hay equipos registrados con ese numero de cédula.</p>
            <p style="margin-top: 15px;">Si acabas de dejar tu equipo, puede tardar algunas horas en aparecer en el sistema. Por favor intenta más tarde.</p>
        </div>
    `;
    modalOverlay.style.display = 'block';
}

// Función para cerrar el modal
function cerrarModal() {
    const modalOverlay = document.getElementById('modalOverlay');
    modalOverlay.style.display = 'none';
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    const cedulaInput = document.getElementById('cedulaInput');
    const trackBtn = document.querySelector('.track-btn');

    cedulaInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            buscarEquipos();
        }
    });

    trackBtn.addEventListener('click', buscarEquipos);
});

// Logging para depuración
console.log('root.js cargado');
