from rest_framework import serializers
from servicios.models import Servicio

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__" #Trabajar con todos los campos de Servicio