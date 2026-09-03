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
import type { Cliente } from '../api/types';
import { LoadingState, ErrorState } from '../components/AsyncState';
import InitialsAvatar from '../components/InitialsAvatar';
import DotTag from '../components/DotTag';

const TIPO_LABEL: Record<Cliente['tipo'], string> = {
  venue: 'Recinto',
  estudio: 'Estudio',
};

const TIPO_COLOR: Record<Cliente['tipo'], string> = {
  venue: 'info.main',
  estudio: 'secondary.main',
};

function TipoTag({ tipo }: { tipo: Cliente['tipo'] }) {
  return <DotTag label={TIPO_LABEL[tipo] ?? tipo} color={TIPO_COLOR[tipo] ?? 'text.disabled'} />;
}

function SinResultados() {
  return (
    <Typography align="center" sx={{ color: 'text.secondary', py: 4 }}>
      No hay clientes registrados.
    </Typography>
  );
}

export default function Clientes() {
  const { data, loading, error, reload } = useApiResource<Cliente[]>('/clientes/');

  if (loading) return <LoadingState />;
  if (error || !data) return <ErrorState message={error ?? 'Sin datos'} onRetry={reload} />;

  return (
    <Box>
      {/* Tabla: visible desde sm hacia arriba, con scroll horizontal si falta espacio */}
      <Paper variant="outlined" sx={{ display: { xs: 'none', sm: 'block' }, overflow: 'hidden' }}>
        <TableContainer sx={{ overflowX: 'auto' }}>
          <Table size="small" sx={{ minWidth: 560 }}>
            <TableHead>
              <TableRow>
                <TableCell>Nombre</TableCell>
                <TableCell>Ciudad</TableCell>
                <TableCell>Tipo</TableCell>
                <TableCell>Contacto</TableCell>
                <TableCell>Teléfono</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.length === 0 && (
                <TableRow>
                  <TableCell colSpan={5}>
                    <SinResultados />
                  </TableCell>
                </TableRow>
              )}
              {data.map((cliente) => (
                <TableRow key={cliente.id} hover>
                  <TableCell sx={{ fontWeight: 500 }}>
                    <Stack direction="row" spacing={1.25} sx={{ alignItems: 'center' }}>
                      <InitialsAvatar name={cliente.nombre} sx={{ width: 30, height: 30, fontSize: '0.8rem' }} />
                      <span>{cliente.nombre}</span>
                    </Stack>
                  </TableCell>
                  <TableCell sx={{ color: 'text.secondary' }}>{cliente.ciudad}</TableCell>
                  <TableCell>
                    <TipoTag tipo={cliente.tipo} />
                  </TableCell>
                  <TableCell sx={{ color: 'text.secondary' }}>{cliente.email_contacto}</TableCell>
                  <TableCell sx={{ color: 'text.secondary' }}>{cliente.telefono}</TableCell>
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
        {data.map((cliente) => (
          <Paper key={cliente.id} variant="outlined" sx={{ p: 2 }}>
            <Stack direction="row" sx={{ mb: 1, justifyContent: 'space-between', alignItems: 'center' }}>
              <Stack direction="row" spacing={1.25} sx={{ alignItems: 'center' }}>
                <InitialsAvatar name={cliente.nombre} sx={{ width: 32, height: 32, fontSize: '0.85rem' }} />
                <Typography sx={{ fontWeight: 600 }}>{cliente.nombre}</Typography>
              </Stack>
              <TipoTag tipo={cliente.tipo} />
            </Stack>
            <Typography variant="body2" color="text.secondary">
              {cliente.ciudad}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {cliente.email_contacto} · {cliente.telefono}
            </Typography>
          </Paper>
        ))}
      </Stack>
    </Box>
  );
}
