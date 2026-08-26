from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteForm

# Create your views here.

class ClienteListView(ListView):
    """Vista para listar todos los clientes."""
    model = Cliente
    template_name = 'clientes/listado_clientes.html'
    context_object_name = 'clientes'
    paginate_by = 20

class ClienteCreateView(SuccessMessageMixin, CreateView):
    """Vista para crear un nuevo cliente."""
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/agregar_cliente.html'
    success_url = reverse_lazy('listar_clientes')
    success_message = 'Cliente "%(nombre)s %(apellido)s" agregado correctamente.'

    def get_context_data(self, **kwargs):
        """Agrega título al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Agregar Cliente'
        return context