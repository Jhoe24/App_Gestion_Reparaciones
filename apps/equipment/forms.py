from django import forms
from .models import SystemConfig


class SystemConfigForm(forms.ModelForm):
	class Meta:
		model = SystemConfig
		fields = [
			'app_name', 'timezone',
			'email_notifications', 'sms_notifications',
			'password_expiry', 'max_attempts', 'two_factor', 'activity_log',
			'backup_frequency', 'backup_day', 'backup_time', 'upload_to_cloud',
			'version'
		]
		widgets = {
			'backup_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
			'app_name': forms.TextInput(attrs={'class': 'form-control'}),
			'timezone': forms.Select(attrs={'class': 'form-select'}),
			'password_expiry': forms.NumberInput(attrs={'class': 'form-control'}),
			'max_attempts': forms.NumberInput(attrs={'class': 'form-control'}),
		}

