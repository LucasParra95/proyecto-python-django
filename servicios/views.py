import json
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from .models import Cliente, Servicio, Empleado, Coordinador, ReservaServicio
from .forms import ClienteForm, ServicioForm, EmpleadoForm, CoordinadorForm, ReservaServicioForm


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

########## EMPLEADOS VIEWS ##########

class EmpleadoListView(ListView):
    """Vista para listar todos los empleados activos."""
    model = Empleado
    template_name = 'listado_generico.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return Empleado.objects.filter(activo=True).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Cliente.html',  # O el index base que utilices
            'titulo': 'Listado de Empleados Activos',
            'boton_principal_texto': 'Agregar Empleado',
            'boton_principal_url': reverse('crear_empleado'),
            'boton_secundario_texto': 'Ver Empleados Inactivos',
            'boton_secundario_url': reverse('listar_empleados_inactivos'),
            'mensaje_vacio': 'No hay empleados activos registrados.',
            'columnas': [
                {'nombre': 'Nombre', 'campo': 'nombre'},
                {'nombre': 'Apellido', 'campo': 'apellido'},
                {'nombre': 'N° Legajo', 'campo': 'numero_legajo'},
            ],
            'acciones': [
                {
                    'texto': 'Editar',
                    'clase': 'primary',
                    'url_pattern': reverse('editar_empleado', kwargs={'pk': 0})[:-1],
                },
                {
                    'texto': 'Eliminar',
                    'clase': 'danger',
                    'url_pattern': reverse('baja_empleado', kwargs={'pk': 0})[:-1],
                },
            ],
        })
        return context


class EmpleadoCreateView(SuccessMessageMixin, CreateView):
    """Vista para crear un nuevo empleado."""
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'agregar_editar.html'
    success_url = reverse_lazy('listar_empleados')
    success_message = 'Empleado "%(nombre)s %(apellido)s" agregado correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index.html',
            'titulo': 'Agregar Nuevo Empleado',
            'boton_texto': 'Guardar Empleado',
            'boton_clase': 'btn-accent',
            'url_cancelar': reverse('listar_empleados'),
        })
        return context


class EmpleadoUpdateView(SuccessMessageMixin, UpdateView):
    """Vista para editar un empleado."""
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'agregar_editar.html'
    success_url = reverse_lazy('listar_empleados')
    success_message = 'Empleado "%(nombre)s %(apellido)s" actualizado correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Editar Empleado',
            'boton_texto': 'Actualizar Empleado',
            'boton_clase': 'btn-primary',
            'url_cancelar': reverse('listar_empleados'),
        })
        return context


class EmpleadoDeactivateView(SuccessMessageMixin, UpdateView):
    """Vista para dar de baja un empleado (baja lógica)."""
    model = Empleado
    fields = []
    template_name = 'confirmar_accion.html'
    success_url = reverse_lazy('listar_empleados')
    success_message = 'Empleado dado de baja correctamente.'

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
            'mensaje_confirmacion': '¿Estás seguro de que deseas dar de baja al empleado?',
            'mensaje_adicional': 'Este empleado será marcado como inactivo y podrá restaurarse más adelante.',
            'nombre_display': nombre_completo,
            'boton_texto': 'Sí, dar de baja',
            'boton_clase': 'btn-danger',
            'url_cancelar': reverse('listar_empleados'),
        })
        return context


class EmpleadoListInactivateView(ListView):
    """Vista para listar empleados inactivos."""
    model = Empleado
    template_name = 'listado_generico.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return Empleado.objects.filter(activo=False).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index.html',
            'titulo': 'Listado de Empleados Inactivos',
            'boton_principal_texto': 'Volver a Empleados Activos',
            'boton_principal_url': reverse('listar_empleados'),
            'mensaje_vacio': 'No hay empleados inactivos.',
            'columnas': [
                {'nombre': 'Nombre', 'campo': 'nombre'},
                {'nombre': 'Apellido', 'campo': 'apellido'},
                {'nombre': 'N° Legajo', 'campo': 'numero_legajo'},
            ],
            'acciones': [
                {
                    'texto': 'Restaurar',
                    'clase': 'success',
                    'url_pattern': reverse('restaurar_empleado', kwargs={'pk': 0})[:-1],
                },
            ],
        })
        return context


class EmpleadoRestoreView(SuccessMessageMixin, UpdateView):
    """Vista para restaurar un empleado inactivo."""
    model = Empleado
    fields = []
    template_name = 'confirmar_accion.html'
    success_url = reverse_lazy('listar_empleados_inactivos')
    success_message = 'Empleado restaurado correctamente.'

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
            'mensaje_confirmacion': '¿Está seguro de que desea restaurar el empleado?',
            'mensaje_adicional': 'El empleado volverá a estar activo en el sistema.',
            'nombre_display': nombre_completo,
            'boton_texto': 'Restaurar Empleado',
            'boton_clase': 'btn-success',
            'url_cancelar': reverse('listar_empleados_inactivos'),
        })
        return context


########## COORDINADORES VIEWS ##########

class CoordinadorListView(ListView):
    """Vista para listar todos los coordinadores activos."""
    model = Coordinador
    template_name = 'listado_generico.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return Coordinador.objects.filter(activo=True).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Listado de Coordinadores Activos',
            'boton_principal_texto': 'Agregar Coordinador',
            'boton_principal_url': reverse('crear_coordinador'),
            'boton_secundario_texto': 'Ver Coordinadores Inactivos',
            'boton_secundario_url': reverse('listar_coordinadores_inactivos'),
            'mensaje_vacio': 'No hay coordinadores activos registrados.',
            'columnas': [
                {'nombre': 'Nombre', 'campo': 'nombre'},
                {'nombre': 'Apellido', 'campo': 'apellido'},
                {'nombre': 'N° Documento', 'campo': 'numero_documento'},
            ],
            'acciones': [
                {
                    'texto': 'Editar',
                    'clase': 'primary',
                    'url_pattern': reverse('editar_coordinador', kwargs={'pk': 0})[:-1],
                },
                {
                    'texto': 'Eliminar',
                    'clase': 'danger',
                    'url_pattern': reverse('baja_coordinador', kwargs={'pk': 0})[:-1],
                },
            ],
        })
        return context


class CoordinadorCreateView(SuccessMessageMixin, CreateView):
    """Vista para crear un nuevo coordinador."""
    model = Coordinador
    form_class = CoordinadorForm
    template_name = 'agregar_editar.html'
    success_url = reverse_lazy('listar_coordinadores')
    success_message = 'Coordinador "%(nombre)s %(apellido)s" agregado correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Agregar Nuevo Coordinador',
            'boton_texto': 'Guardar Coordinador',
            'boton_clase': 'btn-accent',
            'url_cancelar': reverse('listar_coordinadores'),
        })
        return context


class CoordinadorUpdateView(SuccessMessageMixin, UpdateView):
    """Vista para editar un coordinador."""
    model = Coordinador
    form_class = CoordinadorForm
    template_name = 'agregar_editar.html'
    success_url = reverse_lazy('listar_coordinadores')
    success_message = 'Coordinador "%(nombre)s %(apellido)s" actualizado correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Editar Coordinador',
            'boton_texto': 'Actualizar Coordinador',
            'boton_clase': 'btn-primary',
            'url_cancelar': reverse('listar_coordinadores'),
        })
        return context


class CoordinadorDeactivateView(SuccessMessageMixin, UpdateView):
    """Vista para dar de baja un coordinador (baja lógica)."""
    model = Coordinador
    fields = []
    template_name = 'confirmar_accion.html'
    success_url = reverse_lazy('listar_coordinadores')
    success_message = 'Coordinador dado de baja correctamente.'

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
            'mensaje_confirmacion': '¿Estás seguro de que deseas dar de baja al coordinador?',
            'mensaje_adicional': 'Este coordinador será marcado como inactivo y podrá restaurarse más adelante.',
            'nombre_display': nombre_completo,
            'boton_texto': 'Sí, dar de baja',
            'boton_clase': 'btn-danger',
            'url_cancelar': reverse('listar_coordinadores'),
        })
        return context


class CoordinadorListInactivateView(ListView):
    """Vista para listar coordinadores inactivos."""
    model = Coordinador
    template_name = 'listado_generico.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return Coordinador.objects.filter(activo=False).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_template': 'index_Cliente.html',
            'titulo': 'Listado de Coordinadores Inactivos',
            'boton_principal_texto': 'Volver a Coordinadores Activos',
            'boton_principal_url': reverse('listar_coordinadores'),
            'mensaje_vacio': 'No hay coordinadores inactivos.',
            'columnas': [
                {'nombre': 'Nombre', 'campo': 'nombre'},
                {'nombre': 'Apellido', 'campo': 'apellido'},
                {'nombre': 'N° Documento', 'campo': 'numero_documento'},
            ],
            'acciones': [
                {
                    'texto': 'Restaurar',
                    'clase': 'success',
                    'url_pattern': reverse('restaurar_coordinador', kwargs={'pk': 0})[:-1],
                },
            ],
        })
        return context


class CoordinadorRestoreView(SuccessMessageMixin, UpdateView):
    """Vista para restaurar un coordinador inactivo."""
    model = Coordinador
    fields = []
    template_name = 'confirmar_accion.html'
    success_url = reverse_lazy('listar_coordinadores_inactivos')
    success_message = 'Coordinador restaurado correctamente.'

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
            'mensaje_confirmacion': '¿Está seguro de que desea restaurar el coordinador?',
            'mensaje_adicional': 'El coordinador volverá a estar activo en el sistema.',
            'nombre_display': nombre_completo,
            'boton_texto': 'Restaurar Coordinador',
            'boton_clase': 'btn-success',
            'url_cancelar': reverse('listar_coordinadores_inactivos'),
        })
        return context

class HomeView(TemplateView):
    """Vista principal del home con acceso a todos los módulos."""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Inicio - Servicios de Fiesta',
            'total_servicios': Servicio.objects.filter(activo=True).count(),
            'total_clientes': Cliente.objects.filter(activo=True).count(),
            'total_empleados': Empleado.objects.filter(activo=True).count(),
            'total_coordinadores': Coordinador.objects.filter(activo=True).count(),
        })
        return context
 
# --- LISTADO DE RESERVAS ---
class ReservaListView(ListView):
    model = ReservaServicio
    template_name = 'listado_generico.html'
    context_object_name = 'items'
    ordering = ['-fecha_servicio']

    def get_queryset(self):
        return ReservaServicio.objects.select_related(
            'cliente', 'empleado', 'coordinador'
        ).prefetch_related('servicios').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo'] = 'Gestión de Reservas de Servicios'
        context['mensaje_vacio'] = 'No hay reservas registradas en el sistema.'
        
        context['boton_principal_url'] = reverse_lazy('crear_reserva')
        context['boton_principal_texto'] = '➕ Nueva Reserva'

        context['columnas'] = [
            {'nombre': 'ID', 'campo': 'pk'},
            {'nombre': 'Cliente', 'campo': 'cliente'},
            {'nombre': 'Servicios Contratados', 'campo': 'servicios_str'},
            {'nombre': 'Total', 'campo': 'total_reserva', 'tipo': 'precio'},
            {'nombre': 'Empleado', 'campo': 'empleado'},
            {'nombre': 'Coordinador', 'campo': 'coordinador'},
            {'nombre': 'Fecha Evento', 'campo': 'fecha_servicio', 'tipo': 'fecha'},
        ]

        context['acciones'] = [
            {'url_pattern': '/servicios/reservas/editar/', 'clase': 'warning', 'texto': 'Editar'},
            {'url_pattern': '/servicios/reservas/eliminar/', 'clase': 'danger', 'texto': 'Eliminar'},
        ]
        
        return context


# --- CREAR RESERVA ---
class ReservaCreateView(CreateView):
    model = ReservaServicio
    form_class = ReservaServicioForm
    template_name = 'reserva.html'  # Reutiliza el HTML de formulario genérico
    success_url = reverse_lazy('listar_reservas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nueva Reserva de Servicios'
        context['boton_texto'] = 'Guardar Reserva'
        context['boton_clase'] = 'btn-primary'
        context['url_cancelar'] = reverse_lazy('listar_reservas')
        
        precios = {str(s.id): float(s.precio) for s in Servicio.objects.all()}
        context['precios_servicios_json'] = json.dumps(precios)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Reserva creada exitosamente con los servicios seleccionados.")
        return super().form_valid(form)


# --- EDITAR RESERVA ---
class ReservaUpdateView(UpdateView):
    model = ReservaServicio
    form_class = ReservaServicioForm
    template_name = 'reserva.html'  # Reutiliza el HTML de formulario genérico
    success_url = reverse_lazy('listar_reservas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Reserva #{self.object.pk}'
        context['boton_texto'] = 'Actualizar Reserva'
        context['boton_clase'] = 'btn-warning'
        context['url_cancelar'] = reverse_lazy('listar_reservas')
        
        precios = {str(s.id): float(s.precio) for s in Servicio.objects.all()}
        context['precios_servicios_json'] = json.dumps(precios)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Reserva actualizada correctamente.")
        return super().form_valid(form)


# --- ELIMINAR RESERVA ---
class ReservaDeleteView(DeleteView):
    model = ReservaServicio
    template_name = 'confirmar_accion.html'  # Reutiliza el HTML de eliminación genérico
    success_url = reverse_lazy('listar_reservas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Reserva'
        context['color_alerta'] = 'danger'
        context['color_fondo'] = '#dc3545'
        context['mensaje_confirmacion'] = '¿Estás seguro de que deseas cancelar/eliminar esta reserva?'
        context['nombre_display'] = f"Reserva #{self.object.pk} - Cliente: {self.object.cliente}"
        context['mensaje_adicional'] = 'Esta acción desvinculará los servicios asociados y no se podrá deshacer.'
        context['boton_texto'] = 'Sí, Eliminar'
        context['boton_clase'] = 'btn-danger'
        context['url_cancelar'] = reverse_lazy('listar_reservas')
        return context