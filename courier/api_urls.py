from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register("envios", api_views.EnvioViewSet, basename="envio")
router.register("proveedores", api_views.ProveedorViewSet, basename="proveedor")
router.register("clientes", api_views.ClienteViewSet, basename="cliente")
router.register("productos", api_views.ProductoViewSet, basename="producto")
router.register("bodegas", api_views.BodegaViewSet, basename="bodega")

urlpatterns = [
    path("dashboard/", api_views.DashboardView.as_view(), name="api-dashboard"),
    path("", include(router.urls)),
]
