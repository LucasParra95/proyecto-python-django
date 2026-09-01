from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from .models import Cliente, Servicio
from .forms import ClienteForm, ServicioForm


##########CLIENTES VIEWS##########

class ClienteListView(ListView):
    """Vista para listar todos los clientes activos."""
    model = Cliente
    template_name = 'listado_generico.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return Cliente.objects.filter(activo=True).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Listado de Clientes Activos',
            'boton_principal_texto': 'Agregar Cliente',
            'boton_principal_url': reverse('crear_cliente'),
            'boton_secundario_texto': 'Ver Clientes Inactivos',
            'boton_secundario_url': reverse('listar_clientes_inactivos'),
            'mensaje_vacio': 'No hay clientes activos registrados.',
            'columnas': [
                {'nombre': 'Nombre', 'campo': 'nombre'},
                {'nombre': 'Apellido', 'campo': 'apellido'},
            ],
            'acciones': [
                {
                    'texto': 'Editar',
                    'clase': 'primary',
                    'url_pattern': reverse('editar_cliente', kwargs={'pk': 0})[:-1],
                },
                {
                    'texto': 'Eliminar',
                    'clase': 'danger',
                    'url_pattern': reverse('baja_cliente', kwargs={'pk': 0})[:-1],
                },
            ],
        })
        return context


class ClienteCreateView(SuccessMessageMixin, CreateView):
    """Vista para crear un nuevo cliente."""
    model = Cliente
    form_class = ClienteForm
    template_name = 'agregar_editar.html'
    success_url = reverse_lazy('listar_clientes')
    success_message = 'Cliente "%(nombre)s %(apellido)s" agregado correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Agregar Nuevo Cliente',
            'boton_texto': 'Guardar Cliente',
            'boton_clase': 'btn-accent',
            'url_cancelar': reverse('listar_clientes'),
        })
        return context


class ClienteUpdateView(SuccessMessageMixin, UpdateView):
    """Vista para editar un cliente."""
    model = Cliente
    form_class = ClienteForm
    template_name = 'agregar_editar.html'
    success_url = reverse_lazy('listar_clientes')
    success_message = 'Cliente "%(nombre)s %(apellido)s" actualizado correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Editar Cliente',
            'boton_texto': 'Actualizar Cliente',
            'boton_clase': 'btn-primary',
            'url_cancelar': reverse('listar_clientes'),
        })
        return context


class ClienteDeactivateView(SuccessMessageMixin, UpdateView):
    """Vista para dar de baja un cliente (baja lógica)."""
    model = Cliente
    fields = []
    template_name = 'confirmar_accion.html'
    success_url = reverse_lazy('listar_clientes')
    success_message = 'Cliente dado de baja correctamente.'

    def form_valid(self, form):
        self.object.activo = False
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nombre_completo = f"{self.object.nombre} {self.object.apellido}"
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Confirmar Eliminación',
            'color_alerta': 'danger',
            'color_fondo': '#dc3545',
            'mensaje_confirmacion': '¿Estás seguro de que deseas dar de baja el cliente?',
            'mensaje_adicional': 'Este cliente será marcado como inactivo y podrá restaurarse más adelante.',
            'nombre_display': nombre_completo,
            'boton_texto': 'Sí, dar de baja',
            'boton_clase': 'btn-danger',
            'url_cancelar': reverse('listar_clientes'),
        })
        return context


class ClienteListInactivateView(ListView):
    """Vista para listar clientes inactivos."""
    model = Cliente
    template_name = 'listado_generico.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return Cliente.objects.filter(activo=False).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Listado de Clientes Inactivos',
            'boton_principal_texto': 'Volver a Clientes Activos',
            'boton_principal_url': reverse('listar_clientes'),
            'mensaje_vacio': 'No hay clientes inactivos.',
            'columnas': [
                {'nombre': 'Nombre', 'campo': 'nombre'},
                {'nombre': 'Apellido', 'campo': 'apellido'},
            ],
            'acciones': [
                {
                    'texto': 'Restaurar',
                    'clase': 'success',
                    'url_pattern': reverse('restaurar_cliente', kwargs={'pk': 0})[:-1],
                },
            ],
        })
        return context


class ClienteRestoreView(SuccessMessageMixin, UpdateView):
    """Vista para restaurar un cliente inactivo."""
    model = Cliente
    fields = []
    template_name = 'confirmar_accion.html'
    success_url = reverse_lazy('listar_clientes_inactivos')
    success_message = 'Cliente restaurado correctamente.'

    def form_valid(self, form):
        self.object.activo = True
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nombre_completo = f"{self.object.nombre} {self.object.apellido}"
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Confirmar Restauración',
            'color_alerta': 'success',
            'color_fondo': '#28a745',
            'mensaje_confirmacion': '¿Está seguro de que desea restaurar el cliente?',
            'mensaje_adicional': 'El cliente volverá a estar activo en el sistema.',
            'nombre_display': nombre_completo,
            'boton_texto': 'Restaurar Cliente',
            'boton_clase': 'btn-success',
            'url_cancelar': reverse('listar_clientes_inactivos'),
        })
        return context


##########SERVICIOS VIEWS##########

class ServicioListView(ListView):
    """Vista para listar todos los servicios activos."""
    model = Servicio
    template_name = 'listado_generico.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return Servicio.objects.filter(activo=True).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Servicio.html',
            'titulo': 'Listado de Servicios Activos',
            'boton_principal_texto': 'Agregar Servicio',
            'boton_principal_url': reverse('crear_servicio'),
            'boton_secundario_texto': 'Ver Servicios Inactivos',
            'boton_secundario_url': reverse('listar_servicios_inactivos'),
            'mensaje_vacio': 'No hay servicios activos registrados.',
            'columnas': [
                {'nombre': 'Nombre', 'campo': 'nombre'},
                {'nombre': 'Descripción', 'campo': 'descripcion'},
                {'nombre': 'Precio', 'campo': 'precio', 'tipo': 'precio'},
            ],
            'acciones': [
                {
                    'texto': 'Editar',
                    'clase': 'primary',
                    'url_pattern': reverse('editar_servicio', kwargs={'pk': 0})[:-1],
                },
                {
                    'texto': 'Eliminar',
                    'clase': 'danger',
                    'url_pattern': reverse('baja_servicio', kwargs={'pk': 0})[:-1],
                },
            ],
        })
        return context


class ServicioCreateView(SuccessMessageMixin, CreateView):
    """Vista para crear un nuevo servicio."""
    model = Servicio
    form_class = ServicioForm
    template_name = 'agregar_editar.html'
    success_url = reverse_lazy('listar_servicios')
    success_message = 'Servicio "%(nombre)s" agregado correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Servicio.html',
            'titulo': 'Agregar Nuevo Servicio',
            'boton_texto': 'Guardar Servicio',
            'boton_clase': 'btn-accent',
            'url_cancelar': reverse('listar_servicios'),
        })
        return context


class ServicioUpdateView(SuccessMessageMixin, UpdateView):
    """Vista para editar un servicio."""
    model = Servicio
    form_class = ServicioForm
    template_name = 'agregar_editar.html'
    success_url = reverse_lazy('listar_servicios')
    success_message = 'Servicio "%(nombre)s" actualizado correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Servicio.html',
            'titulo': 'Editar Servicio',
            'boton_texto': 'Actualizar Servicio',
            'boton_clase': 'btn-primary',
            'url_cancelar': reverse('listar_servicios'),
        })
        return context


class ServicioDeactivateView(SuccessMessageMixin, UpdateView):
    """Vista para dar de baja un servicio (baja lógica)."""
    model = Servicio
    fields = []
    template_name = 'confirmar_accion.html'
    success_url = reverse_lazy('listar_servicios')
    success_message = 'Servicio dado de baja correctamente.'

    def form_valid(self, form):
        self.object.activo = False
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Servicio.html',
            'titulo': 'Confirmar Eliminación',
            'color_alerta': 'danger',
            'color_fondo': '#dc3545',
            'mensaje_confirmacion': '¿Estás seguro de que deseas dar de baja el servicio?',
            'mensaje_adicional': 'Este servicio será marcado como inactivo y podrá restaurarse más adelante.',
            'nombre_display': self.object.nombre,
            'boton_texto': 'Sí, dar de baja',
            'boton_clase': 'btn-danger',
            'url_cancelar': reverse('listar_servicios'),
        })
        return context


class ServicioListInactivateView(ListView):
    """Vista para listar servicios inactivos."""
    model = Servicio
    template_name = 'listado_generico.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return Servicio.objects.filter(activo=False).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Servicio.html',
            'titulo': 'Listado de Servicios Inactivos',
            'boton_principal_texto': 'Volver a Servicios Activos',
            'boton_principal_url': reverse('listar_servicios'),
            'mensaje_vacio': 'No hay servicios inactivos.',
            'columnas': [
                {'nombre': 'Nombre', 'campo': 'nombre'},
                {'nombre': 'Descripción', 'campo': 'descripcion'},
                {'nombre': 'Precio', 'campo': 'precio', 'tipo': 'precio'},
            ],
            'acciones': [
                {
                    'texto': 'Restaurar',
                    'clase': 'success',
                    'url_pattern': reverse('restaurar_servicio', kwargs={'pk': 0})[:-1],
                },
            ],
        })
        return context


class ServicioRestoreView(SuccessMessageMixin, UpdateView):
    """Vista para restaurar un servicio inactivo."""
    model = Servicio
    fields = []
    template_name = 'confirmar_accion.html'
    success_url = reverse_lazy('listar_servicios_inactivos')
    success_message = 'Servicio restaurado correctamente.'

    def form_valid(self, form):
        self.object.activo = True
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Servicio.html',
            'titulo': 'Confirmar Restauración',
            'color_alerta': 'success',
            'color_fondo': '#28a745',
            'mensaje_confirmacion': '¿Está seguro de que desea restaurar el servicio?',
            'mensaje_adicional': 'El servicio volverá a estar activo en el sistema.',
            'nombre_display': self.object.nombre,
            'boton_texto': 'Restaurar Servicio',
            'boton_clase': 'btn-success',
            'url_cancelar': reverse('listar_servicios_inactivos'),
        })
        return context