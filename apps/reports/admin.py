from django.contrib import admin
from .models import FichaEntrada, Seguimiento, QueuedEmail
# Register your models here.

admin.site.register(FichaEntrada)
admin.site.register(Seguimiento)
admin.site.register(QueuedEmail)