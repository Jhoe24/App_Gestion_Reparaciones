/**
 * -----------------------------------------------
 * DASHBOARD ADMIN JS
 * -----------------------------------------------
 * Este archivo gestiona la interactividad principal
 * del panel de administración, incluyendo la navegación,
 * animaciones, manejo de notificaciones, perfil de usuario
 * y comportamiento responsivo.
 * -----------------------------------------------
 */

/* ==============================
   1. SIDEBAR: Mostrar/Ocultar menú lateral
   ============================== */
/**
 * Permite alternar la visibilidad del sidebar al hacer clic
 * en el botón de menú. Añade o quita la clase 'active' para
 * mostrar u ocultar el menú lateral.
 */
document.getElementById('sidebarToggle').addEventListener('click', function () {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
});


/* ==============================
   3. ANIMACIONES: Tarjetas y elementos visuales
   ============================== */
/**
 * Inicializa la animación de entrada para todas las tarjetas
 * del dashboard, aplicando un pequeño retraso entre cada una
 * para lograr un efecto escalonado.
 */
function initCardAnimations() {
    const cards = document.querySelectorAll('.card, .equipment-card');
    cards.forEach((card, index) => {
        card.style.animation = `slideInUp 0.6s ease forwards`;
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

/**
 * Define la animación 'slideInUp' para las tarjetas.
 * Se agrega dinámicamente al documento.
 */
const slideInUpAnimation = `
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
const animationStyle = document.createElement('style');
animationStyle.textContent = slideInUpAnimation;
document.head.appendChild(animationStyle);

/**
 * Ejecuta la animación de las tarjetas cuando el contenido
 * de la página ha terminado de cargar.
 */
document.addEventListener('DOMContentLoaded', function () {
    initCardAnimations();
});

/* ==============================
   4. NOTIFICACIONES: Campana y badge animados
   ============================== */
/**
 * Añade una animación de rebote ('bounce') al hacer clic
 * en la campana de notificaciones para dar feedback visual.
 */
document.querySelector('.notification-bell').addEventListener('click', function () {
    this.style.animation = 'bounce 0.5s';
    setTimeout(() => {
        this.style.animation = '';
    }, 500);
});

/**
 * Define la animación 'bounce' para la campana y el badge
 * de notificaciones. Se agrega dinámicamente al documento.
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes bounce {
        0%, 20%, 60%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        80% { transform: translateY(-5px); }
    }
`;
document.head.appendChild(style);

/**
 * Simula la llegada de nuevas notificaciones en tiempo real.
 * Cada 5 segundos hay una pequeña probabilidad de incrementar
 * el contador y animar el badge.
 */
setInterval(() => {
    const badge = document.querySelector('.notification-badge');
    if (Math.random() > 0.95) { // 5% de probabilidad cada intervalo
        const currentCount = parseInt(badge.textContent);
        badge.textContent = currentCount + 1;
        badge.style.animation = 'bounce 0.5s';
        setTimeout(() => {
            badge.style.animation = '';
        }, 500);
    }
}, 5000);

/**
 * Gestiona el comportamiento del dropdown de notificaciones.
 * Permite mostrar/ocultar el menú al hacer clic en la campana
 * y lo cierra al hacer clic fuera de ella.
 */
document.addEventListener("DOMContentLoaded", function() {
    const bell = document.getElementById("notificationBell");
    const dropdown = document.getElementById("notificationDropdown");

    bell.addEventListener("click", function(e) {
        e.stopPropagation();
        bell.classList.toggle("active");
    });

    document.addEventListener("click", function(e) {
        if (!bell.contains(e.target)) {
            bell.classList.remove("active");
        }
    });
});

/* ==============================
   5. PERFIL DE USUARIO: Dropdown y cierre automático
   ============================== */
/**
 * Muestra u oculta el menú desplegable del perfil de usuario
 * al hacer clic en el avatar. Evita que el evento se propague
 * para no cerrar el menú inmediatamente.
 */
document.getElementById('userProfile').addEventListener('click', function (e) {
    e.stopPropagation();
    const dropdown = document.getElementById('userDropdown');
    const profile = document.getElementById('userProfile');

    dropdown.classList.toggle('active');
    profile.classList.toggle('active');
});

/**
 * Cierra el menú de perfil de usuario y el sidebar (en móviles)
 * al hacer clic fuera de ellos. Mejora la experiencia en dispositivos
 * móviles y evita menús abiertos accidentalmente.
 */
document.addEventListener('click', function (e) {
    const dropdown = document.getElementById('userDropdown');
    const profile = document.getElementById('userProfile');
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebarToggle');

    // Cierra el dropdown de usuario si se hace clic fuera
    if (!profile.contains(e.target)) {
        dropdown.classList.remove('active');
        profile.classList.remove('active');
    }

    // Cierra el sidebar en pantallas pequeñas si se hace clic fuera
    if (window.innerWidth <= 768) {
        if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    }
});

/* ==============================
   6. RESPONSIVE: Comportamiento en diferentes tamaños de pantalla
   ============================== */
/**
 * Ajusta la visibilidad del sidebar y cierra el menú de usuario
 * automáticamente al cambiar el tamaño de la ventana, asegurando
 * una experiencia consistente en escritorio y móvil.
 */
window.addEventListener('resize', function () {
    const sidebar = document.getElementById('sidebar');
    const dropdown = document.getElementById('userDropdown');
    const profile = document.getElementById('userProfile');

    if (window.innerWidth > 768) {
        sidebar.classList.remove('active');
    }

    // Cierra el dropdown de usuario al cambiar el tamaño
    dropdown.classList.remove('active');
    profile.classList.remove('active');
});

/* ==============================
   7. TIEMPOS DE ACTIVIDAD: Actualización dinámica (opcional)
   ============================== */
/**
 * Actualiza los elementos de tiempo de actividad en la interfaz.
 * Esta función está preparada para conectarse con el backend
 * y mostrar los tiempos reales de las actividades.
 */
function updateActivityTimes() {
    const timeElements = document.querySelectorAll('.activity-time');
    // Aquí se conectaría con el backend para obtener los tiempos reales
}
