from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Bodega, Cliente, Envio, Producto, Proveedor
from .serializers import (
    BodegaSerializer,
    ClienteSerializer,
    EnvioDetailSerializer,
    EnvioListSerializer,
    EnvioWriteSerializer,
    ProductoListSerializer,
    ProductoSerializer,
    ProveedorSerializer,
    SeguimientoEventoSerializer,
)


class EnvioViewSet(ModelViewSet):
    """/api/envios/ y /api/envios/<id>/ — admite ?estado=en_transito, etc.
    También expone /api/envios/<id>/eventos/ (POST) para registrar un nuevo
    evento de tracking sin tener que editar el envío completo."""
    queryset = Envio.objects.select_related("producto", "proveedor", "cliente").prefetch_related("eventos")

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return EnvioWriteSerializer
        if self.action == "retrieve":
            return EnvioDetailSerializer
        return EnvioListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        envio = serializer.save()
        return Response(EnvioDetailSerializer(envio).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        envio = serializer.save()
        return Response(EnvioDetailSerializer(envio).data)

    @action(detail=True, methods=["post"])
    def eventos(self, request, pk=None):
        envio = self.get_object()
        serializer = SeguimientoEventoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(envio=envio)
        # `envio` viene de un queryset con prefetch_related("eventos") ya
        # evaluado antes de crear el evento nuevo, así que su caché de
        # eventos está desactualizada — hay que refrescarla explícitamente.
        envio.refresh_from_db()
        return Response(EnvioDetailSerializer(envio).data, status=status.HTTP_201_CREATED)


class ProveedorViewSet(ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.select_related("proveedor")

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ProductoSerializer
        return ProductoListSerializer


class BodegaViewSet(ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer


class DashboardView(APIView):
    """Estadísticas agregadas para las tarjetas del dashboard."""

    def get(self, request):
        envios = Envio.objects.all()
        data = {
            "total_envios": envios.count(),
            "en_transito": envios.filter(estado=Envio.ESTADO_EN_TRANSITO).count(),
            "en_aduana": envios.filter(estado=Envio.ESTADO_EN_ADUANA).count(),
            "entregados": envios.filter(estado=Envio.ESTADO_ENTREGADO).count(),
            "preparando": envios.filter(estado=Envio.ESTADO_PREPARANDO).count(),
            "total_proveedores": Proveedor.objects.count(),
            "total_clientes": Cliente.objects.count(),
            "envios_recientes": EnvioListSerializer(
                envios.select_related("producto", "proveedor", "cliente")[:5], many=True
            ).data,
        }
        return Response(data)
