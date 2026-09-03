from django.db import models  # noqa: F401

# Unidad 1: sin modelos de base de datos todavía.
# Los "datos" viven en courier/data/seed_data.py como listas de diccionarios
# y se acceden a través de courier/data/repository.py.
#
# En la Unidad 2, aquí se definen los modelos reales (Proveedor, Cliente,
# Producto, Envio, SeguimientoEvento, Bodega) usando los mismos nombres de
# campo que ya se usan en seed_data.py, para que la migración sea directa.
