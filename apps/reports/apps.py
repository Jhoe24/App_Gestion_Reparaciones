from django.apps import AppConfig
import threading
import time
import traceback
import datetime
from django.utils import timezone
from django.db import models


class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reports'

    def ready(self):
        # Iniciar un worker en background que intente reenviar correos en cola.
        # Evitar iniciar en procesos de management commands innecesarios.
        import sys
        argv = sys.argv
        # No arrancar el worker en comandos de migración, makemigrations, shell o test.
        disallowed = ('makemigrations', 'migrate', 'collectstatic', 'shell', 'test')
        if any(a in argv for a in disallowed):
            return

        def _worker():
            from django.conf import settings
            from django.core.mail import EmailMultiAlternatives, send_mail
            from django.apps import apps as django_apps
            QueuedEmail = django_apps.get_model('reports', 'QueuedEmail')

            LOOP_SLEEP = getattr(settings, 'QUEUED_EMAIL_LOOP_SLEEP', 30)
            MAX_BATCH = getattr(settings, 'QUEUED_EMAIL_BATCH', 10)
            MAX_ATTEMPTS = getattr(settings, 'QUEUED_EMAIL_MAX_ATTEMPTS', 6)

            while True:
                try:
                    now = timezone.now()
                    qs = QueuedEmail.objects.filter(sent=False).filter(models.Q(send_after__isnull=True) | models.Q(send_after__lte=now)).order_by('created_at')[:MAX_BATCH]
                    for q in qs:
                        try:
                            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
                            recipients = list(q.to or [])
                            if q.body_html:
                                msg = EmailMultiAlternatives(q.subject, q.body_text, from_email, recipients)
                                msg.attach_alternative(q.body_html, "text/html")
                                msg.send(fail_silently=False)
                            else:
                                send_mail(q.subject, q.body_text, from_email, recipients, fail_silently=False)
                            q.sent = True
                            q.sent_at = timezone.now()
                            q.attempts = q.attempts + 1
                            q.last_error = ''
                            q.save()
                        except Exception as ex_inner:
                            q.attempts = q.attempts + 1
                            q.last_error = str(ex_inner)
                            # exponencial backoff: 2^attempts * 60 seconds, limitado
                            backoff = min(3600, (2 ** q.attempts) * 60)
                            q.send_after = timezone.now() + datetime.timedelta(seconds=backoff)
                            # Si excede max attempts, marcar como enviado (no volver a intentar) pero dejar error
                            if q.attempts >= MAX_ATTEMPTS:
                                q.sent = False
                                # mantener send_after como null para no reintentar
                            q.save()
                            # seguir con siguiente correo
                except Exception:
                    # Never let the worker die silently
                    traceback.print_exc()
                time.sleep(LOOP_SLEEP)

        # Lanzar hilo daemon para que no bloquee el proceso principal en shutdown
        t = threading.Thread(target=_worker, name='reports-queued-email-worker', daemon=True)
        t.start()
