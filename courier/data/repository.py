"""
Capa de acceso a datos para la Unidad 1.

Esta capa imita a propósito la forma en que se va a usar el ORM de Django
más adelante (Modelo.objects.all(), Modelo.objects.get(id=...), etc.).
En la Unidad 2, este archivo se reemplaza por managers/querysets reales de
Django, pero las views.py que consumen estas funciones no deberían tener
que cambiar su lógica, solo el import.
"""

from .seed_data import (
    PROVEEDORES,
    CLIENTES,
    PRODUCTOS,
    ENVIOS,
    SEGUIMIENTO_EVENTOS,
    BODEGAS,
)


def _get_by_id(coleccion, id_buscado):
    for item in coleccion:
        if item["id"] == id_buscado:
            return item
    return None


# ---------------------------------------------------------------------------
# Proveedores
# ---------------------------------------------------------------------------
def get_proveedores():
    return PROVEEDORES


def get_proveedor(proveedor_id):
    return _get_by_id(PROVEEDORES, proveedor_id)


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------
def get_clientes():
    return CLIENTES


def get_cliente(cliente_id):
    return _get_by_id(CLIENTES, cliente_id)


# ---------------------------------------------------------------------------
# Productos
# ---------------------------------------------------------------------------
def get_productos():
    return PRODUCTOS


def get_producto(producto_id):
    return _get_by_id(PRODUCTOS, producto_id)


def get_productos_by_proveedor(proveedor_id):
    return [p for p in PRODUCTOS if p["proveedor_id"] == proveedor_id]


# ---------------------------------------------------------------------------
# Envios
# ---------------------------------------------------------------------------
def get_envios():
    return ENVIOS


def get_envio(envio_id):
    return _get_by_id(ENVIOS, envio_id)


def get_envio_by_codigo(codigo):
    for envio in ENVIOS:
        if envio["codigo"] == codigo:
            return envio
    return None


def get_envios_by_estado(estado):
    return [e for e in ENVIOS if e["estado"] == estado]


def enriquecer_envio(envio):
    """Devuelve una copia del envío con sus relaciones ya resueltas
    (producto, proveedor, cliente), tal como se vería con select_related()
    en el ORM real."""
    if envio is None:
        return None
    envio_completo = dict(envio)
    envio_completo["producto"] = get_producto(envio["producto_id"])
    envio_completo["proveedor"] = get_proveedor(envio["proveedor_id"])
    envio_completo["cliente"] = get_cliente(envio["cliente_id"])
    return envio_completo


# ---------------------------------------------------------------------------
# Seguimiento de eventos
# ---------------------------------------------------------------------------
def get_eventos_by_envio(envio_id):
    eventos = [e for e in SEGUIMIENTO_EVENTOS if e["envio_id"] == envio_id]
    return sorted(eventos, key=lambda e: e["fecha_hora"])


# ---------------------------------------------------------------------------
# Bodegas
# ---------------------------------------------------------------------------
def get_bodegas():
    return BODEGAS


# ---------------------------------------------------------------------------
# Estadísticas para el dashboard
# ---------------------------------------------------------------------------
def get_estadisticas_dashboard():
    total = len(ENVIOS)
    return {
        "total_envios": total,
        "en_transito": len(get_envios_by_estado("en_transito")),
        "en_aduana": len(get_envios_by_estado("en_aduana")),
        "entregados": len(get_envios_by_estado("entregado")),
        "preparando": len(get_envios_by_estado("preparando")),
        "total_proveedores": len(PROVEEDORES),
        "total_clientes": len(CLIENTES),
    }
