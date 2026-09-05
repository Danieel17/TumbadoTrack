# Investigación de soluciones o proyectos similares

Antes de definir el alcance de **TumbadoTrack**, se revisaron soluciones existentes de seguimiento
logístico y transporte, para identificar funcionalidades habituales del rubro y oportunidades de
diferenciación aplicables al caso de Music Pro Company (transporte de equipo musical para giras).

## 1. Portales de tracking de couriers internacionales (FedEx, DHL, UPS)

**Qué resuelven:** permiten a un cliente final rastrear un envío por número de guía, mostrando el
estado actual (en tránsito, en aduana, entregado) y un historial de eventos con fecha, hora y ubicación.

**Funcionalidades clave observadas:**
- Búsqueda de un envío por código de seguimiento.
- Línea de tiempo de eventos (recolectado, en tránsito, en aduana, entregado).
- Estados estandarizados con indicadores visuales (colores/íconos).

**Limitaciones frente al caso de Music Pro:**
- Están pensados para un cliente externo que rastrea *un* paquete, no para un equipo interno que
  administra *todos* los envíos, proveedores y clientes de una operación completa.
- No exponen relaciones de negocio (qué proveedor despachó, a qué cliente/recinto va, qué producto es).
- No tienen noción de roles internos (administrador vs. cliente) ni gestión de usuarios.

## 2. Sistemas de gestión de flotas y logística (TMS genéricos tipo Samsara, Fleetio)

**Qué resuelven:** planificación de rutas, asignación de despachos y control de flota para empresas
de transporte.

**Funcionalidades clave observadas:**
- Dashboard con métricas agregadas (envíos activos, retrasos, cumplimiento).
- Gestión de proveedores/transportistas y de clientes/destinos.
- Filtros por estado del envío.

**Limitaciones frente al caso de Music Pro:**
- Son plataformas genéricas de carga, sin especialización en equipo musical de alto valor
  (instrumentos, sonido, iluminación) ni en la lógica de una gira con fechas de concierto fijas.
- Suelen requerir licencias corporativas complejas, pensadas para flotas propias, no para coordinar
  proveedores externos internacionales con clientes/recintos de un tour.

## 3. Paneles de administración tipo e-commerce (Django Admin, Shopify Admin)

**Qué resuelven:** CRUD de entidades de negocio (productos, pedidos, usuarios) con control de acceso
por rol.

**Funcionalidades clave observadas:**
- CRUD completo de entidades con formularios validados.
- Roles diferenciados (administrador vs. usuario estándar).
- Autenticación y control de sesión.

**Limitaciones frente al caso de Music Pro:**
- No incluyen la lógica de tracking/eventos de un envío ni una vista de "seguimiento" orientada al
  cliente final.
- No combinan, en una sola experiencia, la administración interna (CRUD de proveedores/clientes/
  usuarios) con la visibilidad operativa de un dashboard logístico.

## Oportunidades de diferenciación adoptadas en TumbadoTrack

A partir de esta revisión, TumbadoTrack combina lo mejor de los tres enfoques, ajustado al caso
específico de una gira musical:

1. **Tracking con historial de eventos** (como los couriers internacionales), pero integrado a nivel
   de sistema interno, no solo de un envío aislado.
2. **Dashboard operativo con métricas agregadas** (como un TMS), pero especializado en equipo musical
   (instrumentos, sonido, iluminación) y en la relación proveedor–producto–cliente/recinto propia del
   caso Music Pro Tour 2026.
3. **Panel administrativo con roles y CRUD** (como un admin de e-commerce), pero acotado a lo que la
   gerencia de Music Pro necesita: gestión de usuarios, proveedores, clientes y envíos, sin la
   complejidad de un ERP genérico.
4. **Landing pública** que explica el propósito del sistema antes del login, algo que las herramientas
   internas de flota normalmente omiten (suelen ir directo a un login corporativo).

Esta combinación responde directamente a la problemática planteada en el caso: evitar que el sistema
de transporte sea una "isla informática" más, dándole visibilidad de extremo a extremo (proveedor →
bodega → tránsito → cliente/recinto) con un único punto de acceso para el equipo de Music Pro.
