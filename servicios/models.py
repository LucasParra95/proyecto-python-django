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