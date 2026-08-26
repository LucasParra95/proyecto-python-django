from django.urls import path
from . import views

urlpatterns = [
    path("clientes", views.ClienteListView.as_view(), name='listar_clientes'),
    path("clientes/nuevo", views.ClienteCreateView.as_view(), name='crear_cliente'),
]