from django.urls import path
from . import views

urlpatterns = [
    path("clientes", views.ClienteListView.as_view(), name='listar_clientes'),
    path("clientes/nuevo", views.ClienteCreateView.as_view(), name='crear_cliente'),
    path("clientes/editar/<int:pk>", views.ClienteUpdateView.as_view(), name='editar_cliente'),
    path("clientes/baja/<int:pk>", views.ClienteDeactivateView.as_view(), name='baja_cliente'),
    path("clientes/inactivos", views.ClienteListInactivateView.as_view(), name='listar_clientes_inactivos'),
    path('clientes/inactivos/<int:pk>/restaurar', views.ClienteRestoreView.as_view(), name='restaurar_cliente'),
]