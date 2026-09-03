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
import type { ProductoListado } from '../api/types';
import { LoadingState, ErrorState } from '../components/AsyncState';
import DotTag from '../components/DotTag';

const CATEGORIA_COLOR: Record<string, string> = {
  instrumento: 'primary.main',
  sonido: 'secondary.main',
  iluminacion: 'warning.main',
};

const CATEGORIA_LABEL: Record<string, string> = {
  instrumento: 'Instrumento',
  sonido: 'Sonido',
  iluminacion: 'Iluminación',
};

function CategoriaChip({ categoria }: { categoria: string }) {
  return <DotTag label={CATEGORIA_LABEL[categoria] ?? categoria} color={CATEGORIA_COLOR[categoria] ?? 'text.disabled'} />;
}

function SinResultados() {
  return (
    <Typography align="center" sx={{ color: 'text.secondary', py: 4 }}>
      No hay productos registrados.
    </Typography>
  );
}

export default function Productos() {
  const { data, loading, error, reload } = useApiResource<ProductoListado[]>('/productos/');

  if (loading) return <LoadingState />;
  if (error || !data) return <ErrorState message={error ?? 'Sin datos'} onRetry={reload} />;

  return (
    <Box>
      {/* Tabla: visible desde sm hacia arriba */}
      <Paper variant="outlined" sx={{ display: { xs: 'none', sm: 'block' }, overflow: 'hidden' }}>
        <TableContainer sx={{ overflowX: 'auto' }}>
          <Table size="small" sx={{ minWidth: 640 }}>
            <TableHead>
              <TableRow>
                <TableCell>Producto</TableCell>
                <TableCell>SKU</TableCell>
                <TableCell>Categoría</TableCell>
                <TableCell>Peso</TableCell>
                <TableCell>Proveedor</TableCell>
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
              {data.map((producto) => (
                <TableRow key={producto.id} hover>
                  <TableCell sx={{ fontWeight: 500 }}>{producto.nombre}</TableCell>
                  <TableCell sx={{ color: 'text.secondary', fontFamily: 'monospace', fontSize: '0.8rem' }}>
                    {producto.sku}
                  </TableCell>
                  <TableCell>
                    <CategoriaChip categoria={producto.categoria} />
                  </TableCell>
                  <TableCell sx={{ color: 'text.secondary' }}>{producto.peso_kg} kg</TableCell>
                  <TableCell sx={{ color: 'text.secondary' }}>{producto.proveedor.nombre}</TableCell>
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
        {data.map((producto) => (
          <Paper key={producto.id} variant="outlined" sx={{ p: 2 }}>
            <Stack direction="row" sx={{ mb: 1, justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <Typography sx={{ fontWeight: 600 }}>{producto.nombre}</Typography>
              <CategoriaChip categoria={producto.categoria} />
            </Stack>
            <Typography variant="body2" color="text.secondary" sx={{ fontFamily: 'monospace' }}>
              {producto.sku}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {producto.peso_kg} kg · {producto.proveedor.nombre}
            </Typography>
          </Paper>
        ))}
      </Stack>
    </Box>
  );
}
