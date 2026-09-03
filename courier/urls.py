from django.urls import path

from . import views

app_name = "courier"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("envios/", views.lista_envios, name="lista_envios"),
    path("envios/<int:envio_id>/", views.detalle_envio, name="detalle_envio"),
    path("proveedores/", views.lista_proveedores, name="lista_proveedores"),
    path("clientes/", views.lista_clientes, name="lista_clientes"),
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("usuarios/nuevo/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/<int:usuario_id>/editar/", views.editar_usuario, name="editar_usuario"),
    path("usuarios/<int:usuario_id>/eliminar/", views.eliminar_usuario, name="eliminar_usuario"),
]
