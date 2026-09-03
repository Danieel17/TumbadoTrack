export type EstadoEnvio = 'preparando' | 'en_transito' | 'en_aduana' | 'entregado';

export interface Proveedor {
  id: number;
  nombre: string;
  pais: string;
  email_contacto: string;
  telefono: string;
  tasa_puntualidad: string;
  activo: boolean;
}

export interface Cliente {
  id: number;
  nombre: string;
  ciudad: string;
  tipo: 'venue' | 'estudio';
  email_contacto: string;
  telefono: string;
}

export interface Producto {
  id: number;
  nombre: string;
  sku: string;
  categoria: string;
  peso_kg: string;
  proveedor: number;
}

/** Usado en /api/productos/, donde el proveedor viene resuelto (no solo el id). */
export interface ProductoListado {
  id: number;
  nombre: string;
  sku: string;
  categoria: string;
  peso_kg: string;
  proveedor: Proveedor;
}

export interface Bodega {
  id: number;
  nombre: string;
  ubicacion: string;
  tipo: 'principal' | 'sucursal';
  capacidad: number;
}

export interface EnvioListado {
  id: number;
  codigo: string;
  producto: Producto;
  proveedor: Proveedor;
  cliente: Cliente;
  destino: string;
  peso_total_kg: string;
  estado: EstadoEnvio;
  fecha_envio: string;
  fecha_estimada_entrega: string;
  fecha_real_entrega: string | null;
  ubicacion_actual: string;
}

export interface SeguimientoEvento {
  id: number;
  descripcion: string;
  ubicacion: string;
  fecha_hora: string;
}

export interface EnvioDetalle extends EnvioListado {
  eventos: SeguimientoEvento[];
}

/** Payload de creación/edición: las relaciones van por id, no anidadas. */
export interface EnvioPayload {
  codigo: string;
  producto: number | '';
  proveedor: number | '';
  cliente: number | '';
  destino: string;
  peso_total_kg: string;
  estado: EstadoEnvio;
  fecha_envio: string;
  fecha_estimada_entrega: string;
  fecha_real_entrega: string | null;
  ubicacion_actual: string;
}

export interface SeguimientoEventoPayload {
  descripcion: string;
  ubicacion: string;
  fecha_hora: string;
}

export interface ProveedorPayload {
  nombre: string;
  pais: string;
  email_contacto: string;
  telefono: string;
  tasa_puntualidad: string;
  activo: boolean;
}

export interface ClientePayload {
  nombre: string;
  ciudad: string;
  tipo: 'venue' | 'estudio';
  email_contacto: string;
  telefono: string;
}

export interface ProductoPayload {
  nombre: string;
  sku: string;
  categoria: string;
  peso_kg: string;
  proveedor: number | '';
}

export interface BodegaPayload {
  nombre: string;
  ubicacion: string;
  tipo: 'principal' | 'sucursal';
  capacidad: number | '';
}

export interface DashboardStats {
  total_envios: number;
  en_transito: number;
  en_aduana: number;
  entregados: number;
  preparando: number;
  total_proveedores: number;
  total_clientes: number;
  envios_recientes: EnvioListado[];
}
