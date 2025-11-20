from django.db import models
from django.utils import timezone
from datetime import datetime

class SystemConfig(models.Model):
	FREQUENCY_CHOICES = [
		('daily', 'Diariamente'),
		('weekly', 'Semanalmente'),
		('monthly', 'Mensualmente'),
	]

	DAY_CHOICES = [
		('monday', 'Lunes'),
		('tuesday', 'Martes'),
		('wednesday', 'Miércoles'),
		('thursday', 'Jueves'),
		('friday', 'Viernes'),
		('saturday', 'Sábado'),
		('sunday', 'Domingo'),
	]

	app_name = models.CharField(max_length=200, default='App Gestión de Reparaciones')
	timezone = models.CharField(max_length=64, default='America/Caracas')

	email_notifications = models.BooleanField(default=True)
	sms_notifications = models.BooleanField(default=False)

	password_expiry = models.PositiveIntegerField(default=90)
	max_attempts = models.PositiveIntegerField(default=3)
	two_factor = models.BooleanField(default=False)
	activity_log = models.BooleanField(default=True)

	backup_frequency = models.CharField(max_length=16, choices=FREQUENCY_CHOICES, default='weekly')
	backup_day = models.CharField(max_length=16, choices=DAY_CHOICES, default='friday')
	backup_time = models.TimeField(null=True, blank=True, default=datetime.strptime('02:00', '%H:%M').time())
	upload_to_cloud = models.BooleanField(default=False)

	version = models.CharField(max_length=32, blank=True, default='2.1.5')
	last_update = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Configuración del Sistema'
		verbose_name_plural = 'Configuraciones del Sistema'

	def __str__(self):
		return f"Configuración — {self.app_name}"

	@classmethod
	def get_solo(cls):
		obj, created = cls.objects.get_or_create(pk=1)
		return obj
