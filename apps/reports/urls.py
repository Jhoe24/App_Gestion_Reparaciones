from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('dashboard/', views.AdminReportsDashboardView.as_view(), name='dashboard'),
    path('user/dashboard/', views.UserReportsDashboardView.as_view(), name='user_dashboard'),
]
