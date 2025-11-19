from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class RoleAccessTests(TestCase):
	def setUp(self):
		User = get_user_model()
		# Administrador (superuser)
		self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='pass')
		# asegurar rol si el campo existe
		if hasattr(self.admin, 'rol'):
			self.admin.rol = 'administrador'
			self.admin.save()

		# Técnico
		self.tech = User.objects.create_user(username='tech', password='pass')
		if hasattr(self.tech, 'rol'):
			self.tech.rol = 'tecnico'
			self.tech.save()

		# Usuario sin permisos
		self.other = User.objects.create_user(username='other', password='pass')
		if hasattr(self.other, 'rol'):
			self.other.rol = 'usuario'
			self.other.save()

	def test_tech_and_admin_can_access_ficha(self):
		url = reverse('reports:ficha_entrada')

		self.client.force_login(self.tech)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)

		self.client.logout()
		self.client.force_login(self.admin)
		resp2 = self.client.get(url)
		self.assertEqual(resp2.status_code, 200)

	def test_other_cannot_access_ficha(self):
		url = reverse('reports:ficha_entrada')
		self.client.force_login(self.other)
		resp = self.client.get(url)
		# role_required redirige a 'equipment:user_dashboard' por defecto
		self.assertIn(resp.status_code, (302, 403))

	def test_tech_and_admin_can_access_historial(self):
		url = reverse('reports:historial_equipos')

		self.client.force_login(self.tech)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)

		self.client.logout()
		self.client.force_login(self.admin)
		resp2 = self.client.get(url)
		self.assertEqual(resp2.status_code, 200)

	def test_other_cannot_access_historial(self):
		url = reverse('reports:historial_equipos')
		self.client.force_login(self.other)
		resp = self.client.get(url)
		self.assertIn(resp.status_code, (302, 403))
