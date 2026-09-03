from django.shortcuts import render , get_object_or_404
from servicios.models import Servicio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ServicioSerializer

class ServicioListAPIView(APIView):
    """API view to list all active services."""
    def get(self, request):
        query_set = Servicio.objects.all()
        serializer = ServicioSerializer(query_set, many=True)
        return Response(serializer.data)
    
class ServicioRetrieveAPIView(APIView):
    """API view to retrieve a single service by ID."""
    def get_object(self, pk):
        return get_object_or_404(Servicio, pk=pk)
       
    def get(self, request, pk):
        servicio = self.get_object(pk)
        serializer = ServicioSerializer(servicio)
        return Response(serializer.data)