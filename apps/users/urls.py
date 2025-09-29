# =====================================================
# ARCHIVO: apps/users/urls.py
# =====================================================

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Gestión de usuarios (solo admin)
    path('', views.UserListView.as_view(), name='user_list'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('<int:pk>/toggle-status/', views.toggle_user_status, name='toggle_status'),
    # agregamos la ruta para ver la lista de usuarios
    path('list/users', views.list_user_view, name='list_user_admin'),
    path('new/user', views.new_user_view, name='new_user'),
    #agregamod la ruta para ver el perfil del usuario
    path('profile/', views.profile_view, name='profile'),

]
