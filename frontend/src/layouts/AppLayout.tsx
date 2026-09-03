import { Box } from '@mui/material';
import { useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import PageTransition from '../components/PageTransition';

const TITLES: Record<string, string> = {
  '/': 'Dashboard',
  '/envios': 'Envíos',
  '/proveedores': 'Proveedores',
  '/clientes': 'Clientes',
  '/productos': 'Productos',
  '/bodegas': 'Bodegas',
};

function resolveTitle(pathname: string): string {
  if (TITLES[pathname]) return TITLES[pathname];
  if (pathname.startsWith('/envios/')) return 'Tracking';
  return 'TumbadoTrack';
}

export default function AppLayout() {
  const location = useLocation();

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        <Header title={resolveTitle(location.pathname)} />
        <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, md: 4 } }}>
          <PageTransition />
        </Box>
      </Box>
    </Box>
  );
}
