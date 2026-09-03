import { NavLink } from 'react-router-dom';
import {
  Box,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
  Tooltip,
  Typography,
  useTheme,
  useMediaQuery,
  alpha,
} from '@mui/material';
import SpaceDashboardOutlinedIcon from '@mui/icons-material/SpaceDashboardOutlined';
import LocalShippingOutlinedIcon from '@mui/icons-material/LocalShippingOutlined';
import ApartmentOutlinedIcon from '@mui/icons-material/ApartmentOutlined';
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined';
import Inventory2OutlinedIcon from '@mui/icons-material/Inventory2Outlined';
import WarehouseOutlinedIcon from '@mui/icons-material/WarehouseOutlined';
import LogoutOutlinedIcon from '@mui/icons-material/LogoutOutlined';
import MenuIcon from '@mui/icons-material/Menu';
import { useSidebar } from '../context/SidebarContext';
import { useAuth } from '../context/AuthContext';
import { brandRed } from '../theme/colors';

export const SIDEBAR_WIDTH_EXPANDED = 260;
export const SIDEBAR_WIDTH_COLLAPSED = 80;

const NAV_ITEMS = [
  { label: 'Dashboard', to: '/', icon: SpaceDashboardOutlinedIcon },
  { label: 'Envíos', to: '/envios', icon: LocalShippingOutlinedIcon },
  { label: 'Proveedores', to: '/proveedores', icon: ApartmentOutlinedIcon },
  { label: 'Clientes', to: '/clientes', icon: PeopleOutlinedIcon },
  { label: 'Productos', to: '/productos', icon: Inventory2OutlinedIcon },
  { label: 'Bodegas', to: '/bodegas', icon: WarehouseOutlinedIcon },
];

export default function Sidebar() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const { collapsed, toggleCollapsed, mobileOpen, closeMobile } = useSidebar();
  const { usuario } = useAuth();
  // En mobile el drawer es temporal (overlay) y siempre muestra las etiquetas;
  // el "colapsado" solo aplica al drawer permanente de escritorio.
  const collapsedEffective = isMobile ? false : collapsed;
  const width = collapsedEffective ? SIDEBAR_WIDTH_COLLAPSED : SIDEBAR_WIDTH_EXPANDED;

  const contenido = (
    <>
      <Stack
        direction="row"
        sx={{ px: 2.5, py: 2.5, gap: 1.5, alignItems: 'center', borderBottom: `1px solid ${theme.palette.divider}` }}
      >
        <Box
          component="img"
          src="/logo.png"
          alt="TumbadoTrack"
          sx={{ height: 40, width: 40, objectFit: 'contain', flexShrink: 0 }}
        />
        {!collapsedEffective && (
          <Box sx={{ minWidth: 0 }}>
            <Typography
              noWrap
              sx={{
                fontFamily: "'Mogra', cursive",
                fontSize: '1.3rem',
                lineHeight: 1.2,
                letterSpacing: '0.02em',
                // Rojo exacto del logo (no primary.light/dark, que cambian
                // de tono según el modo) — así el título siempre combina
                // con el ícono, en claro y en oscuro.
                color: brandRed[500],
              }}
            >
              TumbadoTrack
            </Typography>
            <Typography noWrap variant="caption" color="text.secondary">
              Music Pro Company · Courier
            </Typography>
          </Box>
        )}
      </Stack>

      {!isMobile && (
        <Box sx={{ px: 1.5, pt: 1.5 }}>
          <Tooltip title={collapsedEffective ? 'Expandir menú' : ''} placement="right">
            <IconButton onClick={toggleCollapsed} sx={{ width: '100%', borderRadius: 2 }}>
              <MenuIcon />
            </IconButton>
          </Tooltip>
        </Box>
      )}

      <List sx={{ flex: 1, px: 1.5, py: 1 }}>
        {NAV_ITEMS.map(({ label, to, icon: Icon }) => (
          <Tooltip key={to} title={collapsedEffective ? label : ''} placement="right">
            <ListItemButton
              component={NavLink}
              to={to}
              end={to === '/'}
              onClick={isMobile ? closeMobile : undefined}
              sx={{
                position: 'relative',
                borderRadius: 2,
                mb: 0.5,
                justifyContent: collapsedEffective ? 'center' : 'flex-start',
                '&.active': {
                  backgroundColor: alpha(theme.palette.primary.main, theme.palette.mode === 'dark' ? 0.16 : 0.1),
                  color: theme.palette.primary.main,
                  '& .MuiListItemIcon-root': { color: theme.palette.primary.main },
                  // Barra de acento en tostado de marca (no el mismo rojo
                  // del texto/fondo) — dos colores de identidad, no uno solo.
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    left: -12,
                    top: '20%',
                    height: '60%',
                    width: 3,
                    borderRadius: 4,
                    backgroundColor: theme.palette.secondary.main,
                  },
                },
              }}
            >
              <ListItemIcon sx={{ minWidth: collapsedEffective ? 0 : 40, justifyContent: 'center' }}>
                <Icon fontSize="small" />
              </ListItemIcon>
              {!collapsedEffective && (
                <ListItemText primary={label} slotProps={{ primary: { sx: { fontSize: '0.9rem', fontWeight: 500 } } }} />
              )}
            </ListItemButton>
          </Tooltip>
        ))}
      </List>

      <Box sx={{ px: 1.5, py: 1.5, borderTop: `1px solid ${theme.palette.divider}` }}>
        {!collapsedEffective && usuario && (
          <Typography noWrap variant="caption" color="text.secondary" sx={{ px: 1.5, display: 'block', mb: 0.5 }}>
            {usuario}
          </Typography>
        )}
        <LogoutButton collapsed={collapsedEffective} onNavigate={isMobile ? closeMobile : undefined} />
        {!collapsedEffective && (
          <Typography variant="caption" color="text.disabled" sx={{ px: 1.5, pt: 1, display: 'block' }}>
            Tour Natanael Cano 2026
          </Typography>
        )}
      </Box>
    </>
  );

  if (isMobile) {
    return (
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={closeMobile}
        ModalProps={{ keepMounted: true }}
        sx={{
          '& .MuiDrawer-paper': {
            width: SIDEBAR_WIDTH_EXPANDED,
            boxSizing: 'border-box',
            backgroundColor: theme.palette.background.paper,
          },
        }}
      >
        {contenido}
      </Drawer>
    );
  }

  return (
    <Drawer
      variant="permanent"
      sx={{
        width,
        flexShrink: 0,
        whiteSpace: 'nowrap',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.enteringScreen,
        }),
        '& .MuiDrawer-paper': {
          width,
          overflowX: 'hidden',
          boxSizing: 'border-box',
          transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
          }),
          borderRight: `1px solid ${theme.palette.divider}`,
          backgroundColor: theme.palette.background.paper,
        },
      }}
    >
      {contenido}
    </Drawer>
  );
}

function LogoutButton({ collapsed, onNavigate }: { collapsed: boolean; onNavigate?: () => void }) {
  const theme = useTheme();
  const { logout } = useAuth();

  const handleClick = () => {
    onNavigate?.();
    logout();
  };

  return (
    <Tooltip title={collapsed ? 'Cerrar sesión' : ''} placement="right">
      <ListItemButton
        onClick={handleClick}
        sx={{
          borderRadius: 2,
          justifyContent: collapsed ? 'center' : 'flex-start',
          color: theme.palette.error.main,
        }}
      >
        <ListItemIcon sx={{ minWidth: collapsed ? 0 : 40, justifyContent: 'center', color: 'inherit' }}>
          <LogoutOutlinedIcon fontSize="small" />
        </ListItemIcon>
        {!collapsed && <ListItemText primary="Cerrar sesión" slotProps={{ primary: { sx: { fontSize: '0.9rem', fontWeight: 500 } } }} />}
      </ListItemButton>
    </Tooltip>
  );
}
