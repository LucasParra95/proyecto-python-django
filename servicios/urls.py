from django.urls import path
from . import views

urlpatterns = [
    path("clientes", views.ClienteListView.as_view(), name='listar_clientes'),
    path("clientes/nuevo", views.ClienteCreateView.as_view(), name='crear_cliente'),
    path("clientes/editar/<int:pk>", views.ClienteUpdateView.as_view(), name='editar_cliente'),
    path("clientes/baja/<int:pk>", views.ClienteDeactivateView.as_view(), name='baja_cliente'),
    path("clientes/inactivos", views.ClienteListInactivateView.as_view(), name='listar_clientes_inactivos'),
    path('clientes/inactivos/restaurar/<int:pk>', views.ClienteRestoreView.as_view(), name='restaurar_cliente'),
    
    path("servicios", views.ServicioListView.as_view(), name='listar_servicios'),
    path("servicios/nuevo", views.ServicioCreateView.as_view(), name='crear_servicio'),
    path("servicios/editar/<int:pk>", views.ServicioUpdateView.as_view(), name='editar_servicio'),
    path("servicios/baja/<int:pk>", views.ServicioDeactivateView.as_view(), name='baja_servicio'),
    path("servicios/inactivos", views.ServicioListInactivateView.as_view(), name='listar_servicios_inactivos'),
    path('servicios/inactivos/restaurar/<int:pk>', views.ServicioRestoreView.as_view(), name='restaurar_servicio'),
]