from django.urls import path

from . import views

app_name = "courier"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("envios/", views.lista_envios, name="lista_envios"),
    path("envios/nuevo/", views.crear_envio, name="crear_envio"),
    path("envios/<int:envio_id>/", views.detalle_envio, name="detalle_envio"),
    path("envios/<int:envio_id>/editar/", views.editar_envio, name="editar_envio"),
    path("envios/<int:envio_id>/eliminar/", views.eliminar_envio, name="eliminar_envio"),
    path("proveedores/", views.lista_proveedores, name="lista_proveedores"),
    path("proveedores/nuevo/", views.crear_proveedor, name="crear_proveedor"),
    path("proveedores/<int:proveedor_id>/editar/", views.editar_proveedor, name="editar_proveedor"),
    path("proveedores/<int:proveedor_id>/eliminar/", views.eliminar_proveedor, name="eliminar_proveedor"),
    path("clientes/", views.lista_clientes, name="lista_clientes"),
    path("clientes/nuevo/", views.crear_cliente, name="crear_cliente"),
    path("clientes/<int:cliente_id>/editar/", views.editar_cliente, name="editar_cliente"),
    path("clientes/<int:cliente_id>/eliminar/", views.eliminar_cliente, name="eliminar_cliente"),
    path("vehiculos/", views.lista_vehiculos, name="lista_vehiculos"),
    path("vehiculos/nuevo/", views.crear_vehiculo, name="crear_vehiculo"),
    path("vehiculos/<int:vehiculo_id>/editar/", views.editar_vehiculo, name="editar_vehiculo"),
    path("vehiculos/<int:vehiculo_id>/eliminar/", views.eliminar_vehiculo, name="eliminar_vehiculo"),
    path("conductores/", views.lista_conductores, name="lista_conductores"),
    path("conductores/nuevo/", views.crear_conductor, name="crear_conductor"),
    path("conductores/<int:conductor_id>/editar/", views.editar_conductor, name="editar_conductor"),
    path("conductores/<int:conductor_id>/eliminar/", views.eliminar_conductor, name="eliminar_conductor"),
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("usuarios/nuevo/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/<int:usuario_id>/editar/", views.editar_usuario, name="editar_usuario"),
    path("usuarios/<int:usuario_id>/eliminar/", views.eliminar_usuario, name="eliminar_usuario"),
]
