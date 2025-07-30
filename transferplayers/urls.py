"""
URL configuration for TransferPlayers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from core import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin-panel/', views.admin_view, name='admin_panel'),
    path("jugador/<int:id>/", views.player_view, name="jugador"),
    path('admin/', admin.site.urls),
    path('obtener_jugadores_por_equipo/', views.obtener_jugadores_por_equipo, name='obtener_jugadores_por_equipo'),
    path('reporte_solicitudes/', views.reporte_solicitudes, name='reporte_solicitudes'),
    path('obtener_solicitudes/', views.obtener_solicitudes, name='obtener_solicitudes'),
    path('solicitudes_aprobadas/', views.solicitudes_aprobadas, name='solicitudes_aprobadas'),
    path('obtener_solicitudes_aprobadas/', views.obtener_solicitudes_aprobadas, name='obtener_solicitudes_aprobadas'),
    path('usuarios_registrados/', views.usuarios_registrados, name='usuarios_registrados'),
    path('obtener_usuarios_registrados/', views.obtener_usuarios_registrados, name='obtener_usuarios_registrados'),
    path('reporte_semanal/', views.reporte_semanal, name='reporte_semanal'),
    path('obtener_solicitudes_semanales/', views.obtener_solicitudes_semanales, name='obtener_solicitudes_semanales'),
    path('graficas_tactico/', views.vista_graficas, name='graficas_tactico'),
    path('reporte_datos/<str:tipo>/', views.reporte_datos, name='reporte_datos')
]
