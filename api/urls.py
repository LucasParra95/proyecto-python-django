from django.urls import path
from . import views

urlpatterns = [
    path('servicios', views.ServicioListAPIView.as_view(), name='api_list_servicio'),
    path('servicios/<int:pk>', views.ServicioRetrieveAPIView.as_view(), name='api_retrieve_servicio'),
]