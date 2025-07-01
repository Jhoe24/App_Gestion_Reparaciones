from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Construye las rutas dentro del proyecto como: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))


# Configuraciones de desarrollo de inicio rápido - no aptas para producción
# Ver https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: ¡mantén la clave secreta utilizada en producción en secreto!
SECRET_KEY = 'django-insecure-s9v$#l6z8*@u%+d5hq!1ikm+$#me!5dpluz$5y2_b4teuy2-kn'

# ADVERTENCIA DE SEGURIDAD: ¡no ejecutes con debug activado en producción!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# Definición de la aplicación

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'apps.authentication.apps.AuthenticationConfig',
    'apps.equipment.apps.EquipmentConfig',  # Considera actualizar a la ruta de AppConfig si existe
    'apps.maintenance',  # Considera actualizar a la ruta de AppConfig si existe
    'apps.reports',  # Considera actualizar a la ruta de AppConfig si existe
    'apps.users.apps.UsersConfig',
    'axes',

]

AUTHENTICATION_BACKENDS = [
    # AxesBackend debe ser el primero
    'axes.backends.AxesBackend',
    # El backend de autenticación por defecto de Django
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    
    'apps.authentication.url_blocker_middleware.URLBlockerMiddleware',  # Middleware personalizado para bloquear URLs

]

# Configuración de AXES (ejemplo)
AXES_FAILURE_LIMIT = 3  # Bloquear después de 3 intentos fallidos
AXES_COOLOFF_TIME = 0.1  # Bloquear por 6 minutos
AXES_LOCKOUT_TEMPLATE = 'authentication/lockout.html' # Crea esta plantilla

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Base de datos
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validación de contraseñas
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.CustomUser'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


if DEBUG:
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    



# Internacionalización
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_TZ = True


LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/login/'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

if DEBUG:
    SESSION_COOKIE_AGE = 3600
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    
else:
    # Estas configuraciones son para un entorno de producción real detrás de un proxy HTTPS.
    # No las actives para pruebas locales con runserver.
    # Para activarlas en producción, una variable de entorno como DJANGO_ENV=production es una buena práctica.
    # IS_PRODUCTION = os.environ.get('DJANGO_ENV') == 'production' # Comentamos esto para la prueba

    SESSION_COOKIE_AGE = 86400  # 1 día
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    SESSION_COOKIE_SECURE = False  # Forzamos a False para la prueba local
    CSRF_COOKIE_SECURE = False  # Forzamos a False para la prueba local
    SECURE_SSL_REDIRECT = False  # Forzamos a False para la prueba local
    SECURE_HSTS_SECONDS = 0  # Forzamos a 0 para desactivar HSTS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Tipo de clave primaria por defecto
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
