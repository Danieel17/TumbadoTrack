from rest_framework import serializers

from .models import Bodega, Cliente, Envio, Producto, Proveedor, SeguimientoEvento


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ["id", "nombre", "pais", "email_contacto", "telefono", "tasa_puntualidad", "activo"]


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nombre", "ciudad", "tipo", "email_contacto", "telefono"]


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id", "nombre", "sku", "categoria", "peso_kg", "proveedor"]


class ProductoListSerializer(serializers.ModelSerializer):
    """Usada en el listado de productos: proveedor ya resuelto (nombre, país)."""
    proveedor = ProveedorSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ["id", "nombre", "sku", "categoria", "peso_kg", "proveedor"]


class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = ["id", "nombre", "ubicacion", "tipo", "capacidad"]


class SeguimientoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguimientoEvento
        fields = ["id", "descripcion", "ubicacion", "fecha_hora"]


class EnvioListSerializer(serializers.ModelSerializer):
    """Usada en el listado: relaciones ya resueltas, igual que
    repository.enriquecer_envio() hacía a mano con los datos hardcodeados."""
    producto = ProductoSerializer(read_only=True)
    proveedor = ProveedorSerializer(read_only=True)
    cliente = ClienteSerializer(read_only=True)

    class Meta:
        model = Envio
        fields = [
            "id", "codigo", "producto", "proveedor", "cliente", "destino",
            "peso_total_kg", "estado", "fecha_envio", "fecha_estimada_entrega",
            "fecha_real_entrega", "ubicacion_actual",
        ]


class EnvioDetailSerializer(EnvioListSerializer):
    eventos = SeguimientoEventoSerializer(many=True, read_only=True)

    class Meta(EnvioListSerializer.Meta):
        fields = EnvioListSerializer.Meta.fields + ["eventos"]


class EnvioWriteSerializer(serializers.ModelSerializer):
    """Usada para crear/editar: producto/proveedor/cliente van por id
    (PrimaryKeyRelatedField), no anidados como en la lectura."""

    class Meta:
        model = Envio
        fields = [
            "id", "codigo", "producto", "proveedor", "cliente", "destino",
            "peso_total_kg", "estado", "fecha_envio", "fecha_estimada_entrega",
            "fecha_real_entrega", "ubicacion_actual",
        ]

    def validate_codigo(self, value):
        queryset = Envio.objects.filter(codigo=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Ya existe un envío con este código.")
        return value
