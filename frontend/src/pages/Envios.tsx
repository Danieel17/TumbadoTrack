import { useState } from 'react';
import { useSearchParams, Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Chip,
  Stack,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Divider,
  IconButton,
  Button,
  Link as MuiLink,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutlineOutlined';
import { useApiResource } from '../api/useApiResource';
import { useApiMutation } from '../api/useApiMutation';
import type { EnvioListado, EstadoEnvio } from '../api/types';
import { LoadingState, ErrorState } from '../components/AsyncState';
import EstadoBadge from '../components/EstadoBadge';
import InitialsAvatar from '../components/InitialsAvatar';
import EnvioFormDialog from '../components/EnvioFormDialog';
import ConfirmDialog from '../components/ConfirmDialog';

const FILTROS: { label: string; value: EstadoEnvio | null }[] = [
  { label: 'Todos', value: null },
  { label: 'Preparando', value: 'preparando' },
  { label: 'En tránsito', value: 'en_transito' },
  { label: 'En aduana', value: 'en_aduana' },
  { label: 'Entregados', value: 'entregado' },
];

function SinResultados({ mensaje }: { mensaje: string }) {
  return (
    <Typography align="center" sx={{ color: 'text.secondary', py: 4 }}>
      {mensaje}
    </Typography>
  );
}

export default function Envios() {
  const [searchParams, setSearchParams] = useSearchParams();
  const estadoFiltro = searchParams.get('estado');

  const url = estadoFiltro ? `/envios/?estado=${estadoFiltro}` : '/envios/';
  const { data, loading, error, reload } = useApiResource<EnvioListado[]>(url, [estadoFiltro]);
  const { remove, loading: eliminando, generalError: errorEliminacion } = useApiMutation();

  const [formAbierto, setFormAbierto] = useState(false);
  const [envioEditando, setEnvioEditando] = useState<EnvioListado | null>(null);
  const [envioAEliminar, setEnvioAEliminar] = useState<EnvioListado | null>(null);

  const aplicarFiltro = (valor: string | null) => {
    if (valor) {
      setSearchParams({ estado: valor });
    } else {
      setSearchParams({});
    }
  };

  const abrirCreacion = () => {
    setEnvioEditando(null);
    setFormAbierto(true);
  };

  const abrirEdicion = (envio: EnvioListado) => {
    setEnvioEditando(envio);
    setFormAbierto(true);
  };

  const confirmarEliminacion = async () => {
    if (!envioAEliminar) return;
    const result = await remove(`/envios/${envioAEliminar.id}/`);
    if (result.ok) {
      setEnvioAEliminar(null);
      reload();
    }
  };

  return (
    <Box>
      <Stack direction="row" sx={{ mb: 2.5, justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', rowGap: 1.5 }}>
        <Stack direction="row" spacing={1} sx={{ flexWrap: 'wrap', rowGap: 1 }}>
          {FILTROS.map(({ label, value }) => (
            <Chip
              key={label}
              label={label}
              onClick={() => aplicarFiltro(value)}
              variant={estadoFiltro === value ? 'filled' : 'outlined'}
              color={estadoFiltro === value ? 'primary' : 'default'}
            />
          ))}
        </Stack>
        <Button startIcon={<AddIcon />} variant="contained" onClick={abrirCreacion}>
          Nuevo envío
        </Button>
      </Stack>

      {loading && <LoadingState />}
      {!loading && error && <ErrorState message={error} onRetry={reload} />}

      {!loading && !error && data && (
        <>
          {/* Tabla: visible desde sm hacia arriba, con scroll horizontal si falta espacio */}
          <Paper variant="outlined" sx={{ display: { xs: 'none', sm: 'block' }, overflow: 'hidden' }}>
            <TableContainer sx={{ overflowX: 'auto' }}>
              <Table size="small" sx={{ minWidth: 780 }}>
                <TableHead>
                  <TableRow>
                    <TableCell>Código</TableCell>
                    <TableCell>Producto</TableCell>
                    <TableCell>Proveedor</TableCell>
                    <TableCell>Cliente</TableCell>
                    <TableCell>Destino</TableCell>
                    <TableCell>Estado</TableCell>
                    <TableCell align="right"></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={7}>
                        <SinResultados mensaje="No hay envíos con este estado." />
                      </TableCell>
                    </TableRow>
                  )}
                  {data.map((envio) => (
                    <TableRow key={envio.id} hover>
                      <TableCell sx={{ fontWeight: 500 }}>{envio.codigo}</TableCell>
                      <TableCell>{envio.producto.nombre}</TableCell>
                      <TableCell sx={{ color: 'text.secondary' }}>{envio.proveedor.nombre}</TableCell>
                      <TableCell sx={{ color: 'text.secondary' }}>
                        <Stack direction="row" spacing={1} sx={{ alignItems: 'center' }}>
                          <InitialsAvatar name={envio.cliente.nombre} sx={{ width: 26, height: 26, fontSize: '0.7rem' }} />
                          <span>{envio.cliente.nombre}</span>
                        </Stack>
                      </TableCell>
                      <TableCell sx={{ color: 'text.secondary' }}>{envio.destino}</TableCell>
                      <TableCell>
                        <EstadoBadge estado={envio.estado} />
                      </TableCell>
                      <TableCell align="right">
                        <Stack direction="row" spacing={0.5} sx={{ justifyContent: 'flex-end', alignItems: 'center' }}>
                          <MuiLink component={RouterLink} to={`/envios/${envio.id}`} underline="hover" sx={{ whiteSpace: 'nowrap', mr: 1 }}>
                            Ver tracking
                          </MuiLink>
                          <IconButton size="small" aria-label="Editar" onClick={() => abrirEdicion(envio)}>
                            <EditOutlinedIcon fontSize="small" />
                          </IconButton>
                          <IconButton size="small" aria-label="Eliminar" onClick={() => setEnvioAEliminar(envio)}>
                            <DeleteOutlineIcon fontSize="small" color="error" />
                          </IconButton>
                        </Stack>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>

          {/* Tarjetas: solo en xs, una por envío, más fácil de leer que una tabla angosta */}
          <Stack spacing={1.5} sx={{ display: { xs: 'flex', sm: 'none' } }}>
            {data.length === 0 && (
              <Paper variant="outlined">
                <SinResultados mensaje="No hay envíos con este estado." />
              </Paper>
            )}
            {data.map((envio) => (
              <Paper key={envio.id} variant="outlined" sx={{ p: 2 }}>
                <Stack direction="row" sx={{ mb: 1, justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Typography sx={{ fontWeight: 600 }}>{envio.codigo}</Typography>
                  <EstadoBadge estado={envio.estado} />
                </Stack>
                <Typography variant="body2" sx={{ mb: 0.25 }}>
                  {envio.producto.nombre}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0.25 }}>
                  {envio.proveedor.nombre} → {envio.cliente.nombre}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Destino: {envio.destino}
                </Typography>
                <Divider sx={{ my: 1.5 }} />
                <Stack direction="row" sx={{ justifyContent: 'space-between', alignItems: 'center' }}>
                  <MuiLink component={RouterLink} to={`/envios/${envio.id}`} underline="hover" variant="body2">
                    Ver tracking →
                  </MuiLink>
                  <Stack direction="row" spacing={0.5}>
                    <IconButton size="small" aria-label="Editar" onClick={() => abrirEdicion(envio)}>
                      <EditOutlinedIcon fontSize="small" />
                    </IconButton>
                    <IconButton size="small" aria-label="Eliminar" onClick={() => setEnvioAEliminar(envio)}>
                      <DeleteOutlineIcon fontSize="small" color="error" />
                    </IconButton>
                  </Stack>
                </Stack>
              </Paper>
            ))}
          </Stack>
        </>
      )}

      <EnvioFormDialog
        open={formAbierto}
        envio={envioEditando}
        onClose={() => setFormAbierto(false)}
        onSaved={reload}
      />

      <ConfirmDialog
        open={!!envioAEliminar}
        title="Eliminar envío"
        description={`¿Seguro que quieres eliminar el envío ${envioAEliminar?.codigo}? Esta acción no se puede deshacer.`}
        loading={eliminando}
        error={errorEliminacion}
        onCancel={() => setEnvioAEliminar(null)}
        onConfirm={confirmarEliminacion}
      />
    </Box>
  );
}
