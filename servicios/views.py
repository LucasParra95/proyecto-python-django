from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Cliente , Servicio
from .forms import ClienteForm, ServicioForm

##########CLIENTES VIEWS##########

class ClienteListView(ListView):
    """Vista para listar todos los clientes activos."""
    model = Cliente
    template_name = 'clientes/listado_clientes.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        return Cliente.objects.filter(activo=True)

    def get_context_data(self, **kwargs):
        """Agrega título al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado Clientes Activos'
        return context

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

class ClienteUpdateView(SuccessMessageMixin, UpdateView):
    """Vista para editar un cliente."""
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/editar_cliente.html'
    success_url = reverse_lazy('listar_clientes')
    success_message = 'Cliente "%(nombre)s %(apellido)s" actualizado correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Cliente'
        return context

class ClienteDeactivateView(SuccessMessageMixin, UpdateView):
    """Vista para dar de baja un cliente (baja lógica)."""
    model = Cliente
    fields = []
    template_name = 'clientes/baja_cliente.html'
    success_url = reverse_lazy('listar_clientes')
    success_message = 'Cliente dado de baja correctamente.'

    def form_valid(self, form):
        self.object.activo = False
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente_nombre'] = f"{self.object.nombre} {self.object.apellido}"
        return context

class ClienteListInactivateView(ListView):
    """Vista para listar clientes inactivos."""
    model = Cliente
    template_name = 'clientes/listado_inactivos.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        return Cliente.objects.filter(activo=False)

    def get_context_data(self, **kwargs):
        """Agrega título al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado Clientes Inactivos'
        return context

class ClienteRestoreView(SuccessMessageMixin, UpdateView):
    """Vista para restaurar un cliente inactivo."""
    model = Cliente
    fields = []
    template_name = 'clientes/restaurar_cliente.html'
    success_url = reverse_lazy('listar_clientes_inactivos')
    success_message = 'Cliente restaurado correctamente.'

    def form_valid(self, form):
        self.object.activo = True
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente_nombre'] = f"{self.object.nombre} {self.object.apellido}"
        return context
    

##########SERVICIOS VIEWS##########
class ServicioListView(ListView):
    """Vista para listar todos los servicios activos."""
    model = Servicio
    template_name = 'servicios/listado_servicios.html'
    context_object_name = 'servicios'
    paginate_by = 20

    def get_queryset(self):
        return Servicio.objects.filter(activo=True)

    def get_context_data(self, **kwargs):
        """Agrega título al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado Servicios Activos'
        return context

class ServicioCreateView(SuccessMessageMixin, CreateView):
    """Vista para crear un nuevo servicio."""
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicios/agregar_servicio.html'
    success_url = reverse_lazy('listar_servicios')
    success_message = 'Servicio "%(nombre)s" agregado correctamente.'

    def get_context_data(self, **kwargs):
        """Agrega título al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Agregar Servicio'
        return context
    
class ServicioUpdateView(SuccessMessageMixin, UpdateView):
    """Vista para editar un servicio."""
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicios/editar_servicio.html'
    success_url = reverse_lazy('listar_servicios')
    success_message = 'Servicio "%(nombre)s" actualizado correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Servicio'
        return context

class ServicioDeactivateView(SuccessMessageMixin, UpdateView):
    """Vista para dar de baja un servicio (baja lógica)."""
    model = Servicio
    fields = []
    template_name = 'servicios/baja_servicio.html'
    success_url = reverse_lazy('listar_servicios')
    success_message = 'Servicio dado de baja correctamente.'

    def form_valid(self, form):
        self.object.activo = False
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicio_nombre'] = f"{self.object.nombre}"
        return context

class ServicioListInactivateView(ListView):
    """Vista para listar servicios inactivos."""
    model = Servicio
    template_name = 'servicios/listado_inactivos.html'
    context_object_name = 'servicios'
    paginate_by = 20

    def get_queryset(self):
        return Servicio.objects.filter(activo=False)

    def get_context_data(self, **kwargs):
        """Agrega título al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado Servicios Inactivos'
        return context
    
class ServicioRestoreView(SuccessMessageMixin, UpdateView):
    """Vista para restaurar un servicio inactivo."""
    model = Servicio
    fields = []
    template_name = 'servicios/restaurar_servicio.html'
    success_url = reverse_lazy('listar_servicios_inactivos')
    success_message = 'Servicio restaurado correctamente.'

    def form_valid(self, form):
        self.object.activo = True
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicio_nombre'] = f"{self.object.nombre}"
        return context
