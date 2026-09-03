from django.urls import path
from . import views

urlpatterns = [
    path('api/servicios', views.ServicioListAPIView.as_view(), name='api_list_servicio'),
]