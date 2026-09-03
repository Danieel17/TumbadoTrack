from django.contrib import admin

from .models import Bodega, Cliente, Envio, Producto, Proveedor, SeguimientoEvento


class SeguimientoEventoInline(admin.TabularInline):
    model = SeguimientoEvento
    extra = 1


@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ("codigo", "estado", "producto", "proveedor", "cliente", "fecha_envio")
    list_filter = ("estado",)
    search_fields = ("codigo", "destino")
    inlines = [SeguimientoEventoInline]


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
