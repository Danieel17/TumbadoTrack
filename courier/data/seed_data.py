"""
Datos de ejemplo para la Unidad 1 (sin base de datos).

IMPORTANTE (pensando en la Unidad 2):
Cada diccionario usa exactamente los mismos nombres de campo que van a
tener los futuros modelos de Django (Proveedor, Cliente, Producto, Envio,
SeguimientoEvento, Bodega). Las relaciones se simulan con campos "_id"
(por ejemplo producto_id, proveedor_id) igual que lo haria una ForeignKey.
Asi, cuando migremos a models.py real, solo cambia DONDE viven los datos
(base de datos en vez de estas listas), no como se llaman ni como se
relacionan entre si.
"""

# ---------------------------------------------------------------------------
# PROVEEDORES: empresas que fabrican/venden los equipos musicales
# ---------------------------------------------------------------------------
PROVEEDORES = [
    {
        "id": 1,
        "nombre": "Fender USA",
        "pais": "Estados Unidos",
        "email_contacto": "ventas@fender.com",
        "telefono": "+1 480 596 9690",
        "tasa_puntualidad": 96.5,
        "activo": True,
    },
    {
        "id": 2,
        "nombre": "Shure Incorporated",
        "pais": "Estados Unidos",
        "email_contacto": "logistica@shure.com",
        "telefono": "+1 847 600 2000",
        "tasa_puntualidad": 98.1,
        "activo": True,
    },
    {
        "id": 3,
        "nombre": "Roland Corporation",
        "pais": "Japón",
        "email_contacto": "export@roland.co.jp",
        "telefono": "+81 53 460 1111",
        "tasa_puntualidad": 94.0,
        "activo": True,
    },
    {
        "id": 4,
        "nombre": "Yamaha Music",
        "pais": "Japón",
        "email_contacto": "contact@yamaha.com",
        "telefono": "+81 53 460 2432",
        "tasa_puntualidad": 97.2,
        "activo": True,
    },
    {
        "id": 5,
        "nombre": "Clair Global (Sonido/Iluminación)",
        "pais": "Estados Unidos",
        "email_contacto": "ops@clairglobal.com",
        "telefono": "+1 610 691 5300",
        "tasa_puntualidad": 91.8,
        "activo": True,
    },
]

# ---------------------------------------------------------------------------
# CLIENTES: destinatarios de los envíos (venues/recintos del tour)
# ---------------------------------------------------------------------------
CLIENTES = [
    {
        "id": 1,
        "nombre": "Estadio GNP Seguros",
        "ciudad": "Ciudad de México, México",
        "tipo": "venue",
        "email_contacto": "produccion@estadiognp.mx",
        "telefono": "+52 55 5227 3100",
    },
    {
        "id": 2,
        "nombre": "Arena Monterrey",
        "ciudad": "Monterrey, México",
        "tipo": "venue",
        "email_contacto": "eventos@arenamty.com",
        "telefono": "+52 81 8153 8600",
    },
    {
        "id": 3,
        "nombre": "Auditorio Telmex",
        "ciudad": "Guadalajara, México",
        "tipo": "venue",
        "email_contacto": "contacto@auditorio.telmex.com",
        "telefono": "+52 33 3818 3800",
    },
    {
        "id": 4,
        "nombre": "Crypto.com Arena",
        "ciudad": "Los Ángeles, Estados Unidos",
        "tipo": "venue",
        "email_contacto": "booking@cryptoarena.com",
        "telefono": "+1 213 742 7100",
    },
    {
        "id": 5,
        "nombre": "American Airlines Center",
        "ciudad": "Dallas, Estados Unidos",
        "tipo": "venue",
        "email_contacto": "events@aacenter.com",
        "telefono": "+1 214 222 3687",
    },
    {
        "id": 6,
        "nombre": "Estudios MPC Rehearsal Hub",
        "ciudad": "Tijuana, México",
        "tipo": "estudio",
        "email_contacto": "rehearsal@mpc-studios.mx",
        "telefono": "+52 664 123 4567",
    },
]

# ---------------------------------------------------------------------------
# PRODUCTOS: equipos musicales, cada uno ligado a un Proveedor (proveedor_id)
# ---------------------------------------------------------------------------
PRODUCTOS = [
    {
        "id": 1,
        "nombre": "Fender Player Telecaster",
        "sku": "FEN-TEL-0142",
        "categoria": "instrumento",
        "peso_kg": 3.6,
        "proveedor_id": 1,
    },
    {
        "id": 2,
        "nombre": "Shure Axient Digital AD4Q (Receptor 4 canales)",
        "sku": "SHU-AD4Q-0987",
        "categoria": "sonido",
        "peso_kg": 4.1,
        "proveedor_id": 2,
    },
    {
        "id": 3,
        "nombre": "Roland TD-50X Módulo de Batería Electrónica",
        "sku": "ROL-TD50X-0231",
        "categoria": "instrumento",
        "peso_kg": 2.9,
        "proveedor_id": 3,
    },
    {
        "id": 4,
        "nombre": "Yamaha CL5 Consola Digital de Mezcla",
        "sku": "YAM-CL5-0056",
        "categoria": "sonido",
        "peso_kg": 41.0,
        "proveedor_id": 4,
    },
    {
        "id": 5,
        "nombre": "Clay Paky Sharpy Wash Cabeza Móvil",
        "sku": "CLA-SHWA-0819",
        "categoria": "iluminacion",
        "peso_kg": 17.5,
        "proveedor_id": 5,
    },
    {
        "id": 6,
        "nombre": "Shure SM58 Micrófono Vocal Dinámico (set x8)",
        "sku": "SHU-SM58-0033",
        "categoria": "sonido",
        "peso_kg": 5.2,
        "proveedor_id": 2,
    },
]

# ---------------------------------------------------------------------------
# ENVIOS: relaciona Producto + Proveedor + Cliente. Codigo tipo MPC-2026-XXXXX
# ---------------------------------------------------------------------------
ENVIOS = [
    {
        "id": 1,
        "codigo": "MPC-2026-00001",
        "producto_id": 4,
        "proveedor_id": 4,
        "cliente_id": 1,
        "destino": "Ciudad de México, México",
        "peso_total_kg": 41.0,
        "estado": "en_transito",
        "fecha_envio": "2026-02-10",
        "fecha_estimada_entrega": "2026-02-18",
        "fecha_real_entrega": None,
        "ubicacion_actual": "Puerto de Manzanillo, Colima",
    },
    {
        "id": 2,
        "codigo": "MPC-2026-00002",
        "producto_id": 2,
        "proveedor_id": 2,
        "cliente_id": 2,
        "destino": "Monterrey, México",
        "peso_total_kg": 4.1,
        "estado": "en_aduana",
        "fecha_envio": "2026-02-12",
        "fecha_estimada_entrega": "2026-02-19",
        "fecha_real_entrega": None,
        "ubicacion_actual": "Aduana Nuevo Laredo, Tamaulipas",
    },
    {
        "id": 3,
        "codigo": "MPC-2026-00003",
        "producto_id": 5,
        "proveedor_id": 5,
        "cliente_id": 4,
        "destino": "Los Ángeles, Estados Unidos",
        "peso_total_kg": 17.5,
        "estado": "entregado",
        "fecha_envio": "2026-01-28",
        "fecha_estimada_entrega": "2026-02-03",
        "fecha_real_entrega": "2026-02-02",
        "ubicacion_actual": "Crypto.com Arena, Los Ángeles",
    },
    {
        "id": 4,
        "codigo": "MPC-2026-00004",
        "producto_id": 1,
        "proveedor_id": 1,
        "cliente_id": 6,
        "destino": "Tijuana, México",
        "peso_total_kg": 3.6,
        "estado": "preparando",
        "fecha_envio": "2026-02-20",
        "fecha_estimada_entrega": "2026-02-25",
        "fecha_real_entrega": None,
        "ubicacion_actual": "Bodega Central Santiago, Chile",
    },
    {
        "id": 5,
        "codigo": "MPC-2026-00005",
        "producto_id": 3,
        "proveedor_id": 3,
        "cliente_id": 5,
        "destino": "Dallas, Estados Unidos",
        "peso_total_kg": 2.9,
        "estado": "en_transito",
        "fecha_envio": "2026-02-14",
        "fecha_estimada_entrega": "2026-02-22",
        "fecha_real_entrega": None,
        "ubicacion_actual": "Centro de distribución Los Ángeles, CA",
    },
    {
        "id": 6,
        "codigo": "MPC-2026-00006",
        "producto_id": 6,
        "proveedor_id": 2,
        "cliente_id": 3,
        "destino": "Guadalajara, México",
        "peso_total_kg": 5.2,
        "estado": "preparando",
        "fecha_envio": "2026-02-22",
        "fecha_estimada_entrega": "2026-02-28",
        "fecha_real_entrega": None,
        "ubicacion_actual": "Bodega Central Santiago, Chile",
    },
]

# ---------------------------------------------------------------------------
# SEGUIMIENTO_EVENTOS: historial de tracking de cada Envio (envio_id)
# ---------------------------------------------------------------------------
SEGUIMIENTO_EVENTOS = [
    # Envío 1 - Yamaha CL5 a CDMX
    {"id": 1, "envio_id": 1, "descripcion": "Envío creado y preparado en bodega", "ubicacion": "Bodega Central Santiago, Chile", "fecha_hora": "2026-02-10 09:15"},
    {"id": 2, "envio_id": 1, "descripcion": "Salida de bodega hacia puerto", "ubicacion": "Santiago, Chile", "fecha_hora": "2026-02-10 14:30"},
    {"id": 3, "envio_id": 1, "descripcion": "Carga embarcada en buque de carga", "ubicacion": "Puerto de Valparaíso, Chile", "fecha_hora": "2026-02-11 08:00"},
    {"id": 4, "envio_id": 1, "descripcion": "Arribo a puerto de destino, en espera de desaduanaje", "ubicacion": "Puerto de Manzanillo, Colima", "fecha_hora": "2026-02-17 11:45"},

    # Envío 2 - Shure AD4Q a Monterrey
    {"id": 5, "envio_id": 2, "descripcion": "Envío creado y preparado en bodega", "ubicacion": "Bodega Central Santiago, Chile", "fecha_hora": "2026-02-12 10:00"},
    {"id": 6, "envio_id": 2, "descripcion": "Salida de bodega vía transporte aéreo", "ubicacion": "Santiago, Chile", "fecha_hora": "2026-02-12 19:20"},
    {"id": 7, "envio_id": 2, "descripcion": "Ingreso a proceso de revisión aduanera", "ubicacion": "Aduana Nuevo Laredo, Tamaulipas", "fecha_hora": "2026-02-16 07:10"},

    # Envío 3 - Clay Paky Sharpy a Los Ángeles (entregado)
    {"id": 8, "envio_id": 3, "descripcion": "Envío creado y preparado en bodega", "ubicacion": "Bodega Central Santiago, Chile", "fecha_hora": "2026-01-28 08:30"},
    {"id": 9, "envio_id": 3, "descripcion": "Salida de bodega vía transporte aéreo", "ubicacion": "Santiago, Chile", "fecha_hora": "2026-01-28 22:00"},
    {"id": 10, "envio_id": 3, "descripcion": "Despacho aduanero aprobado", "ubicacion": "Los Ángeles, Estados Unidos", "fecha_hora": "2026-02-01 13:15"},
    {"id": 11, "envio_id": 3, "descripcion": "En tránsito hacia el recinto", "ubicacion": "Los Ángeles, Estados Unidos", "fecha_hora": "2026-02-02 09:00"},
    {"id": 12, "envio_id": 3, "descripcion": "Entrega confirmada en recinto", "ubicacion": "Crypto.com Arena, Los Ángeles", "fecha_hora": "2026-02-02 16:40"},

    # Envío 4 - Fender Telecaster a Tijuana
    {"id": 13, "envio_id": 4, "descripcion": "Envío creado y preparado en bodega", "ubicacion": "Bodega Central Santiago, Chile", "fecha_hora": "2026-02-20 09:00"},

    # Envío 5 - Roland TD-50X a Dallas
    {"id": 14, "envio_id": 5, "descripcion": "Envío creado y preparado en bodega", "ubicacion": "Bodega Central Santiago, Chile", "fecha_hora": "2026-02-14 09:00"},
    {"id": 15, "envio_id": 5, "descripcion": "Salida de bodega vía transporte aéreo", "ubicacion": "Santiago, Chile", "fecha_hora": "2026-02-14 23:10"},
    {"id": 16, "envio_id": 5, "descripcion": "Tránsito internacional, escala en centro de distribución", "ubicacion": "Centro de distribución Los Ángeles, CA", "fecha_hora": "2026-02-18 10:30"},

    # Envío 6 - Shure SM58 a Guadalajara
    {"id": 17, "envio_id": 6, "descripcion": "Envío creado y preparado en bodega", "ubicacion": "Bodega Central Santiago, Chile", "fecha_hora": "2026-02-22 08:00"},
]

# ---------------------------------------------------------------------------
# BODEGAS: punto(s) de origen de los envíos (opcional/secundario)
# ---------------------------------------------------------------------------
BODEGAS = [
    {
        "id": 1,
        "nombre": "Bodega Central Santiago",
        "ubicacion": "Santiago, Chile",
        "tipo": "principal",
        "capacidad": 5000,
    },
    {
        "id": 2,
        "nombre": "Centro de distribución Los Ángeles",
        "ubicacion": "Los Ángeles, Estados Unidos",
        "tipo": "sucursal",
        "capacidad": 1800,
    },
]
