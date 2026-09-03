import { useState } from 'react';
import type { FormEvent } from 'react';
import { useParams, useNavigate, Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Grid,
  Paper,
  Stack,
  Typography,
  TextField,
  Button,
  IconButton,
  Alert,
  Link as MuiLink,
} from '@mui/material';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutlineOutlined';
import { useApiResource } from '../api/useApiResource';
import { useApiMutation } from '../api/useApiMutation';
import type { EnvioDetalle as EnvioDetalleType, SeguimientoEventoPayload } from '../api/types';
import { LoadingState, ErrorState } from '../components/AsyncState';
import EstadoBadge from '../components/EstadoBadge';
import EnvioFormDialog from '../components/EnvioFormDialog';
import ConfirmDialog from '../components/ConfirmDialog';

function formatFechaHora(iso: string): string {
  const fecha = new Date(iso);
  if (Number.isNaN(fecha.getTime())) return iso;
  return fecha.toLocaleString('es-CL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function Campo({ label, value, color }: { label: string; value: string; color?: string }) {
  return (
    <Box>
      <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase', letterSpacing: 0.5 }}>
        {label}
      </Typography>
      <Typography variant="body2" sx={{ color: color ?? 'text.primary' }}>
        {value}
      </Typography>
    </Box>
  );
}

const EVENTO_VACIO: SeguimientoEventoPayload = { descripcion: '', ubicacion: '', fecha_hora: '' };

function NuevoEventoForm({ envioId, onCreado }: { envioId: number; onCreado: () => void }) {
  const [form, setForm] = useState<SeguimientoEventoPayload>(EVENTO_VACIO);
  const { create, loading, fieldErrors, generalError } = useApiMutation();

  const setField = <K extends keyof SeguimientoEventoPayload>(field: K, value: SeguimientoEventoPayload[K]) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const result = await create(`/envios/${envioId}/eventos/`, form);
    if (result.ok) {
      setForm(EVENTO_VACIO);
      onCreado();
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3, pt: 3, borderTop: 1, borderColor: 'divider' }}>
      <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1.5 }}>
        Agregar evento
      </Typography>
      {generalError && (
        <Alert severity="error" sx={{ mb: 1.5 }}>
          {generalError}
        </Alert>
      )}
      <Stack spacing={1.5}>
        <TextField
          label="Descripción"
          value={form.descripcion}
          onChange={(e) => setField('descripcion', e.target.value)}
          error={!!fieldErrors.descripcion}
          helperText={fieldErrors.descripcion?.join(' ')}
          size="small"
          required
          fullWidth
        />
        <Stack direction="row" spacing={1.5}>
          <TextField
            label="Ubicación"
            value={form.ubicacion}
            onChange={(e) => setField('ubicacion', e.target.value)}
            error={!!fieldErrors.ubicacion}
            helperText={fieldErrors.ubicacion?.join(' ')}
            size="small"
            required
            fullWidth
          />
          <TextField
            label="Fecha y hora"
            type="datetime-local"
            value={form.fecha_hora}
            onChange={(e) => setField('fecha_hora', e.target.value)}
            error={!!fieldErrors.fecha_hora}
            helperText={fieldErrors.fecha_hora?.join(' ')}
            slotProps={{ inputLabel: { shrink: true } }}
            size="small"
            required
            fullWidth
          />
        </Stack>
        <Button type="submit" variant="outlined" disabled={loading} sx={{ alignSelf: 'flex-start' }}>
          {loading ? 'Agregando…' : 'Agregar evento'}
        </Button>
      </Stack>
    </Box>
  );
}

export default function EnvioDetalle() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: envio, loading, error, reload } = useApiResource<EnvioDetalleType>(`/envios/${id}/`);
  const { remove, loading: eliminando, generalError: errorEliminacion } = useApiMutation();

  const [editando, setEditando] = useState(false);
  const [confirmandoEliminar, setConfirmandoEliminar] = useState(false);

  const confirmarEliminacion = async () => {
    if (!envio) return;
    const result = await remove(`/envios/${envio.id}/`);
    if (result.ok) {
      navigate('/envios');
    }
  };

  return (
    <Box>
      <MuiLink component={RouterLink} to="/envios" underline="hover" variant="body2">
        ← Volver a envíos
      </MuiLink>

      {loading && <LoadingState />}
      {!loading && (error || !envio) && (
        <Box sx={{ mt: 2 }}>
          <ErrorState message={error ?? 'Envío no encontrado.'} onRetry={reload} />
        </Box>
      )}

      {!loading && envio && (
        <Grid container spacing={3} sx={{ mt: 0.5 }}>
          <Grid size={{ xs: 12, md: 4 }}>
            <Paper variant="outlined" sx={{ p: 2.5 }}>
              <Stack direction="row" sx={{ mb: 2, justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  {envio.codigo}
                </Typography>
                <Stack direction="row" spacing={0.5} sx={{ alignItems: 'center' }}>
                  <EstadoBadge estado={envio.estado} />
                  <IconButton size="small" aria-label="Editar" onClick={() => setEditando(true)}>
                    <EditOutlinedIcon fontSize="small" />
                  </IconButton>
                  <IconButton size="small" aria-label="Eliminar" onClick={() => setConfirmandoEliminar(true)}>
                    <DeleteOutlineIcon fontSize="small" color="error" />
                  </IconButton>
                </Stack>
              </Stack>

              <Stack spacing={1.5}>
                <Campo label="Producto" value={`${envio.producto.nombre} (${envio.producto.categoria})`} />
                <Campo label="Proveedor" value={`${envio.proveedor.nombre} · ${envio.proveedor.pais}`} />
                <Campo label="Cliente" value={`${envio.cliente.nombre} · ${envio.cliente.ciudad}`} />
                <Campo label="Destino" value={envio.destino} />
                <Campo label="Ubicación actual" value={envio.ubicacion_actual} color="info.main" />
                <Campo label="Peso total" value={`${envio.peso_total_kg} kg`} />
                <Grid container spacing={1}>
                  <Grid size={6}>
                    <Campo label="Fecha envío" value={envio.fecha_envio} />
                  </Grid>
                  <Grid size={6}>
                    <Campo label="Entrega estimada" value={envio.fecha_estimada_entrega} />
                  </Grid>
                </Grid>
                {envio.fecha_real_entrega && (
                  <Campo label="Entrega real" value={envio.fecha_real_entrega} color="success.main" />
                )}
              </Stack>
            </Paper>
          </Grid>

          <Grid size={{ xs: 12, md: 8 }}>
            <Paper variant="outlined" sx={{ p: 2.5 }}>
              <Typography variant="subtitle2" sx={{ mb: 2.5, fontWeight: 600 }}>
                Historial de seguimiento
              </Typography>

              {envio.eventos.length === 0 && (
                <Typography variant="body2" color="text.secondary">
                  Aún no hay eventos registrados para este envío.
                </Typography>
              )}

              <Stack spacing={0} sx={{ borderLeft: 1, borderColor: 'divider', ml: 1 }}>
                {envio.eventos.map((evento) => (
                  <Box key={evento.id} sx={{ pl: 3, pb: 3, position: 'relative' }}>
                    <Box
                      sx={{
                        position: 'absolute',
                        left: -6,
                        top: 4,
                        width: 11,
                        height: 11,
                        borderRadius: '50%',
                        bgcolor: 'info.main',
                      }}
                    />
                    <Typography variant="body2">{evento.descripcion}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {evento.ubicacion} · {formatFechaHora(evento.fecha_hora)}
                    </Typography>
                  </Box>
                ))}
              </Stack>

              <NuevoEventoForm envioId={envio.id} onCreado={reload} />
            </Paper>
          </Grid>
        </Grid>
      )}

      {envio && (
        <EnvioFormDialog
          open={editando}
          envio={envio}
          onClose={() => setEditando(false)}
          onSaved={reload}
        />
      )}

      <ConfirmDialog
        open={confirmandoEliminar}
        title="Eliminar envío"
        description={`¿Seguro que quieres eliminar el envío ${envio?.codigo}? Esta acción no se puede deshacer.`}
        loading={eliminando}
        error={errorEliminacion}
        onCancel={() => setConfirmandoEliminar(false)}
        onConfirm={confirmarEliminacion}
      />
    </Box>
  );
}
