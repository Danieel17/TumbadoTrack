import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import {
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Stack,
  TextField,
  MenuItem,
  Alert,
  Grid,
} from '@mui/material';
import { useApiResource } from '../api/useApiResource';
import { useApiMutation } from '../api/useApiMutation';
import type { EnvioListado, EnvioPayload, EstadoEnvio, Producto, Proveedor, Cliente } from '../api/types';

const ESTADOS: { value: EstadoEnvio; label: string }[] = [
  { value: 'preparando', label: 'Preparando' },
  { value: 'en_transito', label: 'En tránsito' },
  { value: 'en_aduana', label: 'En aduana' },
  { value: 'entregado', label: 'Entregado' },
];

const VACIO: EnvioPayload = {
  codigo: '',
  producto: '',
  proveedor: '',
  cliente: '',
  destino: '',
  peso_total_kg: '',
  estado: 'preparando',
  fecha_envio: '',
  fecha_estimada_entrega: '',
  fecha_real_entrega: null,
  ubicacion_actual: '',
};

interface EnvioFormDialogProps {
  open: boolean;
  envio: EnvioListado | null;
  onClose: () => void;
  onSaved: () => void;
}

export default function EnvioFormDialog({ open, envio, onClose, onSaved }: EnvioFormDialogProps) {
  const { data: productos } = useApiResource<Producto[]>('/productos/');
  const { data: proveedores } = useApiResource<Proveedor[]>('/proveedores/');
  const { data: clientes } = useApiResource<Cliente[]>('/clientes/');
  const { loading, fieldErrors, generalError, create, update } = useApiMutation();

  const [form, setForm] = useState<EnvioPayload>(VACIO);

  useEffect(() => {
    if (!open) return;
    if (envio) {
      setForm({
        codigo: envio.codigo,
        producto: envio.producto.id,
        proveedor: envio.proveedor.id,
        cliente: envio.cliente.id,
        destino: envio.destino,
        peso_total_kg: envio.peso_total_kg,
        estado: envio.estado,
        fecha_envio: envio.fecha_envio,
        fecha_estimada_entrega: envio.fecha_estimada_entrega,
        fecha_real_entrega: envio.fecha_real_entrega,
        ubicacion_actual: envio.ubicacion_actual,
      });
    } else {
      setForm(VACIO);
    }
  }, [open, envio]);

  const setField = <K extends keyof EnvioPayload>(field: K, value: EnvioPayload[K]) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const payload = { ...form, fecha_real_entrega: form.fecha_real_entrega || null };
    const result = envio
      ? await update(`/envios/${envio.id}/`, payload)
      : await create('/envios/', payload);
    if (result.ok) {
      onSaved();
      onClose();
    }
  };

  const errorFor = (field: string) => fieldErrors[field]?.join(' ');

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{envio ? `Editar ${envio.codigo}` : 'Nuevo envío'}</DialogTitle>
      <Box component="form" onSubmit={handleSubmit}>
        <DialogContent>
          <Stack spacing={2}>
            {generalError && <Alert severity="error">{generalError}</Alert>}

            <TextField
              label="Código"
              value={form.codigo}
              onChange={(e) => setField('codigo', e.target.value)}
              error={!!errorFor('codigo')}
              helperText={errorFor('codigo') ?? 'Ej. MPC-2026-00007'}
              required
              fullWidth
            />

            <Grid container spacing={2}>
              <Grid size={{ xs: 12, sm: 4 }}>
                <TextField
                  select
                  label="Producto"
                  value={form.producto}
                  onChange={(e) => setField('producto', Number(e.target.value))}
                  error={!!errorFor('producto')}
                  helperText={errorFor('producto')}
                  required
                  fullWidth
                >
                  {(productos ?? []).map((p) => (
                    <MenuItem key={p.id} value={p.id}>
                      {p.nombre}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid size={{ xs: 12, sm: 4 }}>
                <TextField
                  select
                  label="Proveedor"
                  value={form.proveedor}
                  onChange={(e) => setField('proveedor', Number(e.target.value))}
                  error={!!errorFor('proveedor')}
                  helperText={errorFor('proveedor')}
                  required
                  fullWidth
                >
                  {(proveedores ?? []).map((p) => (
                    <MenuItem key={p.id} value={p.id}>
                      {p.nombre}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid size={{ xs: 12, sm: 4 }}>
                <TextField
                  select
                  label="Cliente"
                  value={form.cliente}
                  onChange={(e) => setField('cliente', Number(e.target.value))}
                  error={!!errorFor('cliente')}
                  helperText={errorFor('cliente')}
                  required
                  fullWidth
                >
                  {(clientes ?? []).map((c) => (
                    <MenuItem key={c.id} value={c.id}>
                      {c.nombre}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
            </Grid>

            <TextField
              label="Destino"
              value={form.destino}
              onChange={(e) => setField('destino', e.target.value)}
              error={!!errorFor('destino')}
              helperText={errorFor('destino')}
              required
              fullWidth
            />

            <Grid container spacing={2}>
              <Grid size={{ xs: 6 }}>
                <TextField
                  label="Peso total (kg)"
                  value={form.peso_total_kg}
                  onChange={(e) => setField('peso_total_kg', e.target.value)}
                  error={!!errorFor('peso_total_kg')}
                  helperText={errorFor('peso_total_kg')}
                  required
                  fullWidth
                />
              </Grid>
              <Grid size={{ xs: 6 }}>
                <TextField
                  select
                  label="Estado"
                  value={form.estado}
                  onChange={(e) => setField('estado', e.target.value as EstadoEnvio)}
                  error={!!errorFor('estado')}
                  helperText={errorFor('estado')}
                  required
                  fullWidth
                >
                  {ESTADOS.map((e) => (
                    <MenuItem key={e.value} value={e.value}>
                      {e.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
            </Grid>

            <Grid container spacing={2}>
              <Grid size={{ xs: 6 }}>
                <TextField
                  label="Fecha de envío"
                  type="date"
                  value={form.fecha_envio}
                  onChange={(e) => setField('fecha_envio', e.target.value)}
                  error={!!errorFor('fecha_envio')}
                  helperText={errorFor('fecha_envio')}
                  slotProps={{ inputLabel: { shrink: true } }}
                  required
                  fullWidth
                />
              </Grid>
              <Grid size={{ xs: 6 }}>
                <TextField
                  label="Entrega estimada"
                  type="date"
                  value={form.fecha_estimada_entrega}
                  onChange={(e) => setField('fecha_estimada_entrega', e.target.value)}
                  error={!!errorFor('fecha_estimada_entrega')}
                  helperText={errorFor('fecha_estimada_entrega')}
                  slotProps={{ inputLabel: { shrink: true } }}
                  required
                  fullWidth
                />
              </Grid>
            </Grid>

            <TextField
              label="Entrega real (opcional)"
              type="date"
              value={form.fecha_real_entrega ?? ''}
              onChange={(e) => setField('fecha_real_entrega', e.target.value || null)}
              error={!!errorFor('fecha_real_entrega')}
              helperText={errorFor('fecha_real_entrega')}
              slotProps={{ inputLabel: { shrink: true } }}
              fullWidth
            />

            <TextField
              label="Ubicación actual"
              value={form.ubicacion_actual}
              onChange={(e) => setField('ubicacion_actual', e.target.value)}
              error={!!errorFor('ubicacion_actual')}
              helperText={errorFor('ubicacion_actual')}
              required
              fullWidth
            />
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 3 }}>
          <Button onClick={onClose} color="inherit">
            Cancelar
          </Button>
          <Button type="submit" variant="contained" disabled={loading}>
            {loading ? 'Guardando…' : envio ? 'Guardar cambios' : 'Crear envío'}
          </Button>
        </DialogActions>
      </Box>
    </Dialog>
  );
}
