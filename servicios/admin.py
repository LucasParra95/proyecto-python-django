from django.contrib import admin

from .models import Cliente, Servicio, Empleado, Coordinador, ReservaServicio


@admin.register(Servicio) #registra el modelo en el panel del admin
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre" , "precio", "activo") # las columnas que se van a ver. descripcion no se si hace falta
    list_filter = ("activo",) # filtro. Se puede probar la baja logica asi
    search_fields = ("nombre",) # habilita la barra de busqueda
    ordering = ("nombre",) # solo ordena

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre" , "apellido", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "apellido")
    ordering = ("apellido", "nombre")

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "numero_legajo", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "apellido")
    ordering = ("apellido", "nombre")

@admin.register(Coordinador)
class CoordinadorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "numero_documento", "activo")
    list_filter = ("activo", "numero_documento")
    search_fields = ("nombre", "apellido")
    ordering = ("apellido", "nombre")


@admin.register(ReservaServicio)
class ReservaServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'empleado', 'coordinador', 'fecha_servicio', 'fecha_reserva')
    filter_horizontal = ('servicios',)  # Interfaz cómoda para seleccionar varios servicios
    list_filter = ('fecha_servicio',)
    search_fields = (
        'cliente__nombre', 'cliente__apellido',
        'empleado__nombre', 'empleado__apellido',
        'coordinador__nombre', 'coordinador__apellido'
    )