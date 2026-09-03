from django.shortcuts import render
from servicios.models import Servicio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ServicioSerializer

class ServicioListAPIView(APIView):
    """API view to list all active services."""
    def get(self, request):
        query_set = Servicio.objects.filter(activo=True)
        serializer = ServicioSerializer(query_set, many=True)
        return Response(serializer.data)