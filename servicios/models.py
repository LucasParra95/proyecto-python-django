from django.db import models

# Create your models here.
class Cliente(models.Model):
    """Modelo para gestionar clientes"""

    nombre = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="Nombre del cliente"
    )

    apellido = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="Apellido del cliente"
    )

    activo = models.BooleanField(
        default=True,
        help_text="Indica si el cliente está activo"
    )
    
class Servicio(models.Model):
    """Modelo para gestionar Servicios"""
    
    nombre = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Nombre del Servicio")
    
    descripcion = models.TextField(
        max_length=500,
        blank=False,
        null=False,
        help_text="Descripcion del Servicio")
    
    precio = models.IntegerField(
        blank=False,
        null=False,
        help_text="Precio del Servicio")
    
    activo = models.BooleanField(
        default=True,
        help_text="Indica si el servicio esta activo")

class Empleado(models.Model):
    """Modelo para gestionar Empleados"""
    nombre = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="Nombre del empleado"
    )
    apellido = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="Apellido del empleado"
    )
    numero_legajo = models.IntegerField(
        unique=True,
        blank=False,
        null=False,
        help_text="Número de legajo único del empleado"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Indica si el empleado está activo"
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Legajo: {self.numero_legajo})"


class Coordinador(models.Model):
    """Modelo para gestionar Coordinadores"""
    nombre = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="Nombre del coordinador"
    )
    apellido = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="Apellido del coordinador"
    )
    numero_documento = models.IntegerField(
        unique=True,
        blank=False,
        null=False,
        help_text="Número de documento del coordinador"
    )
    fecha_alta = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de alta en el sistema"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Indica si el coordinador está activo"
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class ReservaServicio(models.Model):
    """Modelo para gestionar las Reservas de Servicios"""
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='reservas',
        help_text="Cliente que realiza la reserva"
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name='reservas',
        help_text="Servicio reservado"
    )
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='reservas',
        help_text="Empleado asignado a la reserva"
    )
    coordinador = models.ForeignKey(
        Coordinador,
        on_delete=models.CASCADE,
        related_name='reservas',
        help_text="Coordinador responsable de la reserva"
    )
    fecha_reserva = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que se realizó la reserva"
    )
    fecha_servicio = models.DateField(
        help_text="Fecha solicitada para el evento/servicio"
    )

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente} ({self.servicio})"