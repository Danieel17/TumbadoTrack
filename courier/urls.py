from django.urls import path

from . import views

app_name = "courier"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("envios/", views.lista_envios, name="lista_envios"),
    path("envios/<int:envio_id>/", views.detalle_envio, name="detalle_envio"),
    path("proveedores/", views.lista_proveedores, name="lista_proveedores"),
    path("clientes/", views.lista_clientes, name="lista_clientes"),
]
