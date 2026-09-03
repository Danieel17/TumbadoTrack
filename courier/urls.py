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
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("usuarios/nuevo/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/<int:usuario_id>/editar/", views.editar_usuario, name="editar_usuario"),
    path("usuarios/<int:usuario_id>/eliminar/", views.eliminar_usuario, name="eliminar_usuario"),
]
