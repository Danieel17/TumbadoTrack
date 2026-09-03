import {
  Box,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';
import { useApiResource } from '../api/useApiResource';
import type { Proveedor } from '../api/types';
import { LoadingState, ErrorState } from '../components/AsyncState';
import InitialsAvatar from '../components/InitialsAvatar';
import DotTag from '../components/DotTag';

function SinResultados() {
  return (
    <Typography align="center" sx={{ color: 'text.secondary', py: 4 }}>
      No hay proveedores registrados.
    </Typography>
  );
}

function EstadoActivo({ activo }: { activo: boolean }) {
  return <DotTag label={activo ? 'Activo' : 'Inactivo'} color={activo ? 'success.main' : 'text.disabled'} />;
}

export default function Proveedores() {
  const { data, loading, error, reload } = useApiResource<Proveedor[]>('/proveedores/');

  if (loading) return <LoadingState />;
  if (error || !data) return <ErrorState message={error ?? 'Sin datos'} onRetry={reload} />;

  return (
    <Box>
      {/* Tabla: visible desde sm hacia arriba, con scroll horizontal si falta espacio */}
      <Paper variant="outlined" sx={{ display: { xs: 'none', sm: 'block' }, overflow: 'hidden' }}>
        <TableContainer sx={{ overflowX: 'auto' }}>
          <Table size="small" sx={{ minWidth: 640 }}>
            <TableHead>
              <TableRow>
                <TableCell>Nombre</TableCell>
                <TableCell>País</TableCell>
                <TableCell>Contacto</TableCell>
                <TableCell>Teléfono</TableCell>
                <TableCell>Puntualidad</TableCell>
                <TableCell>Estado</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.length === 0 && (
                <TableRow>
                  <TableCell colSpan={6}>
                    <SinResultados />
                  </TableCell>
                </TableRow>
              )}
              {data.map((proveedor) => (
                <TableRow key={proveedor.id} hover>
                  <TableCell sx={{ fontWeight: 500 }}>
                    <Stack direction="row" spacing={1.25} sx={{ alignItems: 'center' }}>
                      <InitialsAvatar name={proveedor.nombre} sx={{ width: 30, height: 30, fontSize: '0.8rem' }} />
                      <span>{proveedor.nombre}</span>
                    </Stack>
                  </TableCell>
                  <TableCell sx={{ color: 'text.secondary' }}>{proveedor.pais}</TableCell>
                  <TableCell sx={{ color: 'text.secondary' }}>{proveedor.email_contacto}</TableCell>
                  <TableCell sx={{ color: 'text.secondary' }}>{proveedor.telefono}</TableCell>
                  <TableCell sx={{ color: 'secondary.dark' }}>{proveedor.tasa_puntualidad}%</TableCell>
                  <TableCell>
                    <EstadoActivo activo={proveedor.activo} />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Tarjetas: solo en xs */}
      <Stack spacing={1.5} sx={{ display: { xs: 'flex', sm: 'none' } }}>
        {data.length === 0 && (
          <Paper variant="outlined">
            <SinResultados />
          </Paper>
        )}
        {data.map((proveedor) => (
          <Paper key={proveedor.id} variant="outlined" sx={{ p: 2 }}>
            <Stack direction="row" sx={{ mb: 1, justifyContent: 'space-between', alignItems: 'center' }}>
              <Stack direction="row" spacing={1.25} sx={{ alignItems: 'center' }}>
                <InitialsAvatar name={proveedor.nombre} sx={{ width: 32, height: 32, fontSize: '0.85rem' }} />
                <Typography sx={{ fontWeight: 600 }}>{proveedor.nombre}</Typography>
              </Stack>
              <EstadoActivo activo={proveedor.activo} />
            </Stack>
            <Typography variant="body2" color="text.secondary">
              {proveedor.pais}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {proveedor.email_contacto} · {proveedor.telefono}
            </Typography>
            <Typography variant="body2" sx={{ color: 'secondary.dark', mt: 0.5 }}>
              Puntualidad: {proveedor.tasa_puntualidad}%
            </Typography>
          </Paper>
        ))}
      </Stack>
    </Box>
  );
}
