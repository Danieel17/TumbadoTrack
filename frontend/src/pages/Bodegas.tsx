import { Box, Grid, Paper, Stack, Typography } from '@mui/material';
import DotTag from '../components/DotTag';
import WarehouseOutlinedIcon from '@mui/icons-material/WarehouseOutlined';
import { useApiResource } from '../api/useApiResource';
import type { Bodega } from '../api/types';
import { LoadingState, ErrorState } from '../components/AsyncState';

export default function Bodegas() {
  const { data, loading, error, reload } = useApiResource<Bodega[]>('/bodegas/');

  if (loading) return <LoadingState />;
  if (error || !data) return <ErrorState message={error ?? 'Sin datos'} onRetry={reload} />;

  if (data.length === 0) {
    return (
      <Paper variant="outlined">
        <Typography align="center" sx={{ color: 'text.secondary', py: 4 }}>
          No hay bodegas registradas.
        </Typography>
      </Paper>
    );
  }

  return (
    <Grid container spacing={2}>
      {data.map((bodega) => (
        <Grid key={bodega.id} size={{ xs: 12, sm: 6, md: 4 }}>
          <Paper
            variant="outlined"
            sx={{
              p: 3,
              borderRadius: 2,
              height: '100%',
              transition: 'transform 200ms ease, box-shadow 200ms ease',
              '&:hover': { transform: 'translateY(-3px)', boxShadow: 4 },
            }}
          >
            <Stack direction="row" spacing={2} sx={{ alignItems: 'center', mb: 2 }}>
              <Box
                sx={{
                  width: 48,
                  height: 48,
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  background: (theme) =>
                    `linear-gradient(135deg, ${theme.palette.info.main}, ${theme.palette.info.dark})`,
                  color: 'info.contrastText',
                }}
              >
                <WarehouseOutlinedIcon />
              </Box>
              <Box sx={{ minWidth: 0 }}>
                <Typography sx={{ fontWeight: 600 }} noWrap>
                  {bodega.nombre}
                </Typography>
                <Typography variant="body2" color="text.secondary" noWrap>
                  {bodega.ubicacion}
                </Typography>
              </Box>
            </Stack>
            <Stack direction="row" spacing={1} sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
              <DotTag
                label={bodega.tipo === 'principal' ? 'Principal' : 'Sucursal'}
                color={bodega.tipo === 'principal' ? 'primary.main' : 'text.disabled'}
              />
              <Typography variant="body2" color="text.secondary">
                Capacidad: <strong>{bodega.capacidad.toLocaleString('es-CL')}</strong>
              </Typography>
            </Stack>
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
}
