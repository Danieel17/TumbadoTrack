import { Box } from '@mui/material';
import { useLocation, Outlet } from 'react-router-dom';

/** Reinicia la animación de entrada (fade + slide sutil) cada vez que cambia
 * la ruta, usando `key` para forzar el remount del contenido de la página. */
export default function PageTransition() {
  const location = useLocation();

  return (
    <Box
      key={location.pathname}
      sx={{
        animation: 'page-enter 380ms cubic-bezier(0.22, 1, 0.36, 1)',
        '@keyframes page-enter': {
          from: { opacity: 0, transform: 'translateY(10px)' },
          to: { opacity: 1, transform: 'translateY(0)' },
        },
      }}
    >
      <Outlet />
    </Box>
  );
}
