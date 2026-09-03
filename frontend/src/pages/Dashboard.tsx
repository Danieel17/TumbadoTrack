import type { ReactNode } from 'react';
import {
  Box,
  Grid,
  Paper,
  Stack,
  Divider,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Link as MuiLink,
} from '@mui/material';
import Inventory2OutlinedIcon from '@mui/icons-material/Inventory2Outlined';
import ApartmentOutlinedIcon from '@mui/icons-material/ApartmentOutlined';
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined';
import { Link as RouterLink } from 'react-router-dom';
import { useApiResource } from '../api/useApiResource';
import type { DashboardStats, Proveedor } from '../api/types';
import { LoadingState, ErrorState } from '../components/AsyncState';
import EstadoBadge from '../components/EstadoBadge';
import DotTag from '../components/DotTag';
import EstadoDonutChart from '../components/EstadoDonutChart';
import PuntualidadBarChart from '../components/PuntualidadBarChart';
import { useCountUp } from '../helpers/useCountUp';

const STAGGER_SX = (index: number) => ({
  opacity: 0,
  animation: 'dashboard-stagger 460ms cubic-bezier(0.22, 1, 0.36, 1) forwards',
  animationDelay: `${index * 80}ms`,
  '@keyframes dashboard-stagger': {
    from: { opacity: 0, transform: 'translateY(8px)' },
    to: { opacity: 1, transform: 'translateY(0)' },
  },
});

function HeroStat({ data }: { data: DashboardStats }) {
  const total = useCountUp(data.total_envios);
  const desglose = [
    { label: 'En tránsito', value: data.en_transito, color: 'info.main' },
    { label: 'En aduana', value: data.en_aduana, color: 'warning.main' },
    { label: 'Entregados', value: data.entregados, color: 'success.main' },
    { label: 'Preparando', value: data.preparando, color: 'text.disabled' },
  ];

  return (
    <Paper variant="outlined" sx={{ p: { xs: 3, md: 4 }, height: '100%', position: 'relative', overflow: 'hidden' }}>
      <Inventory2OutlinedIcon
        sx={{
          position: 'absolute',
          right: -16,
          top: -16,
          fontSize: 140,
          color: 'secondary.main',
          opacity: 0.07,
          pointerEvents: 'none',
        }}
      />
      <Box sx={{ position: 'relative' }}>
        <Typography variant="overline" color="text.secondary" sx={{ letterSpacing: 1.5 }}>
          Total envíos
        </Typography>
        <Typography variant="h1" sx={{ fontSize: { xs: '3.75rem', md: '5rem' }, lineHeight: 1, my: 1 }}>
          {total}
        </Typography>
        <Stack direction="row" spacing={2.5} sx={{ flexWrap: 'wrap', rowGap: 1, mt: 2.5 }}>
          {desglose.map((item, i) => (
            <Box key={item.label} sx={STAGGER_SX(i)}>
              <DotTag label={`${item.label} · ${item.value}`} color={item.color} />
            </Box>
          ))}
        </Stack>
      </Box>
    </Paper>
  );
}

function SplitStat({ data }: { data: DashboardStats }) {
  const proveedores = useCountUp(data.total_proveedores);
  const clientes = useCountUp(data.total_clientes);

  return (
    <Paper variant="outlined" sx={{ p: { xs: 3, md: 4 }, height: '100%' }}>
      <Stack direction="row" divider={<Divider orientation="vertical" flexItem />} spacing={3} sx={{ height: '100%' }}>
        <Box sx={{ flex: 1 }}>
          <Stack direction="row" spacing={1} sx={{ alignItems: 'center', mb: 1, color: 'text.secondary' }}>
            <ApartmentOutlinedIcon fontSize="small" />
            <Typography variant="overline" sx={{ letterSpacing: 1 }}>
              Proveedores
            </Typography>
          </Stack>
          <Typography variant="h2" sx={{ fontSize: '2.75rem', lineHeight: 1 }}>
            {proveedores}
          </Typography>
        </Box>
        <Box sx={{ flex: 1 }}>
          <Stack direction="row" spacing={1} sx={{ alignItems: 'center', mb: 1, color: 'text.secondary' }}>
            <PeopleOutlinedIcon fontSize="small" />
            <Typography variant="overline" sx={{ letterSpacing: 1 }}>
              Clientes
            </Typography>
          </Stack>
          <Typography variant="h2" sx={{ fontSize: '2.75rem', lineHeight: 1 }}>
            {clientes}
          </Typography>
        </Box>
      </Stack>
    </Paper>
  );
}

function ChartCard({ title, children, delay }: { title: string; children: ReactNode; delay: number }) {
  return (
    <Paper variant="outlined" sx={{ p: 2.5, height: '100%', ...STAGGER_SX(delay) }}>
      <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
        {title}
      </Typography>
      {children}
    </Paper>
  );
}

export default function Dashboard() {
  const { data, loading, error, reload } = useApiResource<DashboardStats>('/dashboard/');
  const { data: proveedores } = useApiResource<Proveedor[]>('/proveedores/');

  if (loading) return <LoadingState />;
  if (error || !data) return <ErrorState message={error ?? 'Sin datos'} onRetry={reload} />;

  return (
    <Box>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid size={{ xs: 12, md: 5 }} sx={STAGGER_SX(0)}>
          <HeroStat data={data} />
        </Grid>
        <Grid size={{ xs: 12, md: 7 }} sx={STAGGER_SX(1)}>
          <SplitStat data={data} />
        </Grid>
      </Grid>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, md: 6 }}>
          <ChartCard title="Distribución de envíos por estado" delay={2}>
            <EstadoDonutChart
              preparando={data.preparando}
              enTransito={data.en_transito}
              enAduana={data.en_aduana}
              entregados={data.entregados}
            />
          </ChartCard>
        </Grid>
        <Grid size={{ xs: 12, md: 6 }}>
          <ChartCard title="Puntualidad por proveedor" delay={3}>
            <PuntualidadBarChart proveedores={proveedores ?? []} />
          </ChartCard>
        </Grid>
      </Grid>

      <Paper variant="outlined" sx={STAGGER_SX(4)}>
        <Box sx={{ px: 2.5, py: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
            Envíos recientes
          </Typography>
        </Box>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Código</TableCell>
                <TableCell>Destino</TableCell>
                <TableCell>Estado</TableCell>
                <TableCell>Fecha envío</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.envios_recientes.length === 0 && (
                <TableRow>
                  <TableCell colSpan={4} align="center" sx={{ color: 'text.secondary', py: 4 }}>
                    No hay envíos registrados.
                  </TableCell>
                </TableRow>
              )}
              {data.envios_recientes.map((envio) => (
                <TableRow key={envio.id} hover>
                  <TableCell>
                    <MuiLink component={RouterLink} to={`/envios/${envio.id}`} underline="hover">
                      {envio.codigo}
                    </MuiLink>
                  </TableCell>
                  <TableCell>{envio.destino}</TableCell>
                  <TableCell>
                    <EstadoBadge estado={envio.estado} />
                  </TableCell>
                  <TableCell sx={{ color: 'text.secondary' }}>{envio.fecha_envio}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
}
