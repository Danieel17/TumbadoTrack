from django.contrib import admin

from .models import (
    Bodega,
    Cliente,
    ComprobanteEntrega,
    Conductor,
    Envio,
    Incidencia,
    Producto,
    Proveedor,
    SeguimientoEvento,
    Vehiculo,
)


class SeguimientoEventoInline(admin.TabularInline):
    model = SeguimientoEvento
    extra = 1


class IncidenciaInline(admin.TabularInline):
    model = Incidencia
    extra = 0


@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ("codigo", "estado", "producto", "proveedor", "cliente", "vehiculo", "conductor", "fecha_envio")
    list_filter = ("estado",)
    search_fields = ("codigo", "destino")
    inlines = [SeguimientoEventoInline, IncidenciaInline]


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "pais", "tasa_puntualidad", "activo")
    list_filter = ("activo", "pais")
    search_fields = ("nombre",)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ciudad", "tipo")
    list_filter = ("tipo",)
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sku", "categoria", "proveedor")
    list_filter = ("categoria",)
    search_fields = ("nombre", "sku")


@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ubicacion", "tipo", "capacidad")


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("patente", "tipo", "capacidad_kg", "proveedor")
    list_filter = ("tipo", "proveedor")
    search_fields = ("patente",)


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "licencia", "telefono", "vehiculo")
    search_fields = ("nombre", "licencia")


@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ("envio", "tipo", "fecha_hora")
    list_filter = ("tipo",)
    search_fields = ("envio__codigo", "descripcion")


@admin.register(ComprobanteEntrega)
class ComprobanteEntregaAdmin(admin.ModelAdmin):
    list_display = ("envio", "nombre_receptor", "fecha_hora")
    search_fields = ("envio__codigo", "nombre_receptor")
