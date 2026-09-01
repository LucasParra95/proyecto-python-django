from django.urls import path
from . import views

urlpatterns = [
    # --- CLIENTES ---
    path("clientes", views.ClienteListView.as_view(), name='listar_clientes'),
    path("clientes/nuevo", views.ClienteCreateView.as_view(), name='crear_cliente'),
    path("clientes/editar/<int:pk>", views.ClienteUpdateView.as_view(), name='editar_cliente'),
    path("clientes/baja/<int:pk>", views.ClienteDeactivateView.as_view(), name='baja_cliente'),
    path("clientes/inactivos", views.ClienteListInactivateView.as_view(), name='listar_clientes_inactivos'),
    path('clientes/inactivos/restaurar/<int:pk>', views.ClienteRestoreView.as_view(), name='restaurar_cliente'),
    
    # --- SERVICIOS ---
    path("servicios", views.ServicioListView.as_view(), name='listar_servicios'),
    path("servicios/nuevo", views.ServicioCreateView.as_view(), name='crear_servicio'),
    path("servicios/editar/<int:pk>", views.ServicioUpdateView.as_view(), name='editar_servicio'),
    path("servicios/baja/<int:pk>", views.ServicioDeactivateView.as_view(), name='baja_servicio'),
    path("servicios/inactivos", views.ServicioListInactivateView.as_view(), name='listar_servicios_inactivos'),
    path('servicios/inactivos/restaurar/<int:pk>', views.ServicioRestoreView.as_view(), name='restaurar_servicio'),
# --- EMPLEADOS ---
    path('empleados', views.EmpleadoListView.as_view(), name='listar_empleados'),
    path('empleados/nuevo', views.EmpleadoCreateView.as_view(), name='crear_empleado'),
    path('empleados/editar/<int:pk>', views.EmpleadoUpdateView.as_view(), name='editar_empleado'),
    path('empleados/baja/<int:pk>', views.EmpleadoDeactivateView.as_view(), name='baja_empleado'),
    path('empleados/inactivos', views.EmpleadoListInactivateView.as_view(), name='listar_empleados_inactivos'),
    path('empleados/inactivos/restaurar/<int:pk>', views.EmpleadoRestoreView.as_view(), name='restaurar_empleado'),

    # --- COORDINADORES ---
    path('coordinadores/', views.CoordinadorListView.as_view(), name='listar_coordinadores'),
    path('coordinadores/nuevo', views.CoordinadorCreateView.as_view(), name='crear_coordinador'),
    path('coordinadores/editar/<int:pk>', views.CoordinadorUpdateView.as_view(), name='editar_coordinador'),
    path('coordinadores/baja/<int:pk>', views.CoordinadorDeactivateView.as_view(), name='baja_coordinador'),
    path('coordinadores/inactivos', views.CoordinadorListInactivateView.as_view(), name='listar_coordinadores_inactivos'),
    path('coordinadores/inactivos/restaurar/<int:pk>', views.CoordinadorRestoreView.as_view(), name='restaurar_coordinador'),
]