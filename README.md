---
title: Sistema de Gestión de Mantenimiento de Equipos
author: Deviam
date: 2024-07-20
---

# 🛠️ Sistema de Gestión de Mantenimiento de Equipos

¡Bienvenido al Sistema de Gestión de Mantenimiento de Equipos! Este proyecto es como un "cerebro" digital que ayuda a la universidad a mantener todos sus equipos (computadoras, impresoras, proyectores, etc.) funcionando perfectamente. Imagina que es un asistente muy organizado que sabe qué equipo necesita reparación, quién lo está arreglando y cuándo estará listo.

## ✨ ¿Qué hace este sistema? (Las "Super Habilidades")

Este sistema está diseñado para simplificar la vida de todos en la universidad, desde los estudiantes hasta los técnicos. Aquí te explico sus principales "super habilidades":

*   **Gestión de Usuarios Inteligente**:
    *   **Administradores**: Son como los "directores" del sistema. Pueden ver y controlar todo, crear nuevas cuentas para técnicos y usuarios, y asegurarse de que todo funcione bien.
    *   **Técnicos**: Son los "doctores" de los equipos. Reciben los reportes de fallas, diagnostican los problemas, realizan las reparaciones y actualizan el estado de los equipos.
    *   **Usuarios Regulares**: Son como los "detectives" que encuentran problemas. Pueden reportar fácilmente cuando un equipo no funciona y seguir el progreso de su reparación.

*   **Inventario de Equipos Organizado**:
    *   Guarda toda la información importante de cada equipo: su código, tipo (¿es una laptop o una impresora?), marca, modelo, número de serie y dónde está ubicado en la universidad.
    *   Siempre sabes si un equipo está "operativo" (funcionando), "en mantenimiento" (siendo reparado) o "dado de baja" (ya no se usa).

*   **Reportes de Mantenimiento Sencillos**:
    *   Cualquier usuario puede crear un "reporte" cuando un equipo tiene un problema. Es como llenar un formulario para pedir ayuda.
    *   Los técnicos reciben estos reportes y pueden ver todos los detalles de la falla.
    *   Se registra todo el "historial" de cada reparación: qué se hizo, quién lo hizo, qué repuestos se usaron, etc. ¡Así no se pierde ningún detalle!

*   **Registro de Actividad (El "Diario" del Sistema)**:
    *   Cada vez que alguien inicia sesión, cierra sesión o hace algo importante, el sistema lo anota en un "diario". Esto es útil para saber quién hizo qué y cuándo.

## 💻 ¿Qué "idiomas" y "herramientas" usa? (La "Magia" por Dentro)

Este proyecto está construido con algunas de las herramientas más populares y robustas del mundo de la programación:

*   **Python**: Es el "idioma principal" en el que está escrito el cerebro del sistema. Es muy potente y fácil de entender.
*   **Django**: Es un "marco de trabajo" (framework) de Python. Piensa en él como un conjunto de herramientas y reglas que hacen que construir sitios web y aplicaciones sea mucho más rápido y seguro.
*   **SQLite**: Es la "caja fuerte" donde se guarda toda la información del sistema (usuarios, equipos, reportes). Es perfecta para empezar porque no necesita mucha configuración.
*   **Bootstrap**: Es un "kit de diseño" que hace que la aplicación se vea bonita y funcione bien en cualquier dispositivo (computadora, tablet, celular).
*   **Font Awesome**: Es una "biblioteca de iconos" que añade esos pequeños dibujos (como el martillo 🛠️ o el candado 🔒) que hacen la interfaz más intuitiva.

## 🚀 ¿Cómo ponerlo a funcionar? (¡Manos a la Obra!)

No te preocupes si no sabes de programación. Sigue estos pasos como si fueran una receta de cocina. Necesitarás un poco de paciencia y seguir las instrucciones al pie de la letra.

### Paso 1: Las Herramientas Necesarias (Pre-requisitos)

Antes de empezar, asegúrate de tener estas "herramientas mágicas" instaladas en tu computadora:

1.  **Python (versión 3.x)**:
    *   **¿Qué es?** Es el "idioma" que entiende nuestro programa.
    *   **¿Cómo lo consigo?** Ve a la página oficial de Python: [python.org/downloads](https://www.python.org/downloads/). Descarga la última versión de Python 3 (por ejemplo, Python 3.10 o superior) y sigue las instrucciones de instalación. **¡Muy importante!** Durante la instalación, asegúrate de marcar la casilla que dice "Add Python to PATH" (o similar).

2.  **Git**:
    *   **¿Qué es?** Es una herramienta para descargar el proyecto de internet.
    *   **¿Cómo lo consigo?** Ve a [git-scm.com/downloads](https://git-scm.com/downloads/). Descarga la versión para tu sistema operativo y sigue las instrucciones de instalación.

3.  **Un "Terminal" o "Símbolo del Sistema"**:
    *   **¿Qué es?** Es una ventana donde escribes comandos de texto.
    *   **¿Cómo lo abro?**
        *   **Windows**: Busca "CMD" o "Símbolo del sistema" en el menú de inicio.
        *   **macOS**: Busca "Terminal" en Spotlight (Cmd + Espacio).
        *   **Linux**: Generalmente se llama "Terminal" y lo encuentras en tus aplicaciones.

### Paso 2: Traer el Proyecto a Tu Computadora

Ahora vamos a "descargar" el proyecto a tu computadora.

1.  Abre tu "Terminal" o "Símbolo del Sistema".
2.  Escribe el siguiente comando y presiona `Enter`:
    ```bash
    git clone https://github.com/your-username/Gestion_Reparaciones.git
    ```
    *(Nota: `https://github.com/your-username/Gestion_Reparaciones.git` es un ejemplo. Si el proyecto está en otro lugar, usa la dirección correcta que te hayan dado.)*
3.  Una vez que termine de descargar, entra a la carpeta del proyecto. Escribe:
    ```bash
    cd Gestion_Reparaciones
    ```

### Paso 3: Crear un Espacio de Trabajo Limpio (Entorno Virtual)

Esto es como crear un "taller" especial para este proyecto, para que sus herramientas no se mezclen con las de otros programas que tengas.

1.  Dentro de la carpeta `Gestion_Reparaciones` (donde estás ahora en el Terminal), escribe:
    ```bash
    python -m venv venv
    ```
    Esto creará una nueva carpeta llamada `venv`.
2.  Ahora, "activa" este taller. El comando cambia un poco según tu sistema:
    *   **Windows**:
        ```bash
        venv\Scripts\activate
        ```
    *   **macOS / Linux**:
        ```bash
        source venv/bin/activate
        ```
    Verás que el nombre `(venv)` aparece al principio de la línea en tu Terminal. ¡Eso significa que el taller está activo!

### Paso 4: Instalar las Herramientas del Proyecto

El proyecto necesita algunas herramientas adicionales para funcionar. Las instalaremos todas de golpe.

1.  Con el "taller" (venv) activo, escribe:
    ```bash
    pip install -r requirements.txt
    ```
    Espera a que termine. Puede tardar un poco.

### Paso 5: Preparar la Base de Datos (Donde se Guarda la Información)

El sistema necesita un lugar para guardar todos los datos (usuarios, equipos, reportes). Esto lo hacemos con dos comandos:

1.  Primero, le decimos a Django (nuestro "cerebro" del sistema) que prepare las "tablas" para guardar la información:
    ```bash
    python manage.py migrate
    ```
    Verás muchos mensajes, ¡es normal!
2.  Ahora, vamos a crear un "usuario administrador" especial para que puedas entrar al sistema y configurarlo todo. Es como el "dueño" del sistema.
    ```bash
    python manage.py createsuperuser
    ```
    *   Te pedirá un **nombre de usuario** (ej: `admin`).
    *   Luego, una **dirección de correo electrónico** (ej: `admin@example.com`).
    *   Finalmente, una **contraseña**. Escríbela y presiona `Enter`, luego repítela y presiona `Enter` de nuevo. (No verás lo que escribes, ¡es por seguridad!).

### Paso 6: ¡Encender el Sistema!

¡Ya casi terminamos! Ahora vamos a iniciar el sistema para que puedas usarlo.

1.  En el Terminal (asegúrate de que `(venv)` siga apareciendo), escribe:
    ```bash
    python manage.py runserver
    ```
    Verás un mensaje que dice algo como "Starting development server at http://127.0.0.1:8000/".
2.  **¡Listo!** Abre tu navegador de internet (Chrome, Firefox, Edge, etc.) y en la barra de direcciones (donde escribes las páginas web), escribe exactamente esto:
    ```
    http://127.0.0.1:8000/
    ```
    Presiona `Enter`. ¡Deberías ver la página de inicio de sesión del sistema!

## 🚀 ¿Cómo usar el sistema? (¡A Jugar!)

Una vez que el sistema esté funcionando en tu navegador:

1.  **Inicia Sesión**: Usa el nombre de usuario y la contraseña que creaste en el "Paso 5" (`createsuperuser`).
2.  **Explora los Paneles (Dashboards)**:
    *   Si inicias sesión como **Administrador**, verás un panel con estadísticas generales y opciones para gestionar usuarios y equipos.
    *   Si creas un usuario con rol de **Técnico**, verá un panel enfocado en los reportes de mantenimiento.
    *   Los **Usuarios Regulares** verán un panel más simple, donde podrán reportar problemas y ver el estado de sus equipos.
3.  **Gestiona Usuarios**: Como administrador, puedes ir a la sección de "Usuarios" para crear, editar o desactivar cuentas.
4.  **Registra Equipos**: Puedes añadir nuevos equipos al inventario, especificando todos sus detalles.
5.  **Reporta Fallas**: Si eres un usuario, puedes crear un reporte cuando un equipo no funcione.
6.  **Sigue las Reparaciones**: Como técnico, puedes actualizar el estado de los reportes y registrar lo que haces en el historial de reparación.

¡Disfruta usando el sistema! Si tienes alguna pregunta o encuentras algún problema, no dudes en pedir ayuda.

## 🤝 Contribuciones

¡Tu ayuda es bienvenida! Si eres programador y quieres mejorar este sistema, puedes:
*   Reportar errores.
*   Sugerir nuevas funcionalidades.
*   Enviar tus propias mejoras (pull requests).

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Puedes ver los detalles en el archivo `LICENSE` (si existe) en la carpeta principal del proyecto.

---

¡Gracias por usar y apoyar el Sistema de Gestión de Mantenimiento de Equipos!