from django.db import models

# Create your models here.
class Servicio(models.Model):
    nombre = models.CharField(max_length=100,blank=False,null=False,help_text="Nombre del Servicio")
    descripcion = models.TextField(max_length=500,blank=False,null=False,help_text="Descripcion del Servicio")
    precio = models.IntegerField(blank=False,null=False,help_text="Precio del Servicio")
    activo = models.BooleanField(default=True,help_text="Indica si el servicio esta activo")