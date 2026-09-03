import { useState } from 'react';
import type { MouseEvent } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Stack,
  TextField,
  InputAdornment,
  Badge,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Divider,
  useTheme,
} from '@mui/material';
import SearchOutlinedIcon from '@mui/icons-material/SearchOutlined';
import NotificationsNoneOutlinedIcon from '@mui/icons-material/NotificationsNoneOutlined';
import LogoutOutlinedIcon from '@mui/icons-material/LogoutOutlined';
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined';
import MenuIcon from '@mui/icons-material/Menu';
import { useThemeMode } from '../context/ThemeModeContext';
import { useSidebar } from '../context/SidebarContext';
import { useAuth } from '../context/AuthContext';
import InitialsAvatar from '../components/InitialsAvatar';

interface HeaderProps {
  title: string;
}

export default function Header({ title }: HeaderProps) {
  const theme = useTheme();
  const { mode, toggleMode } = useThemeMode();
  const { openMobile } = useSidebar();
  const { usuario, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);

  const handleOpenMenu = (event: MouseEvent<HTMLElement>) => setAnchorEl(event.currentTarget);
  const handleCloseMenu = () => setAnchorEl(null);
  const handleLogout = () => {
    handleCloseMenu();
    logout();
  };

  return (
    <AppBar
      position="sticky"
      color="transparent"
      sx={{
        borderBottom: `1px solid ${theme.palette.divider}`,
        backgroundColor: theme.palette.background.default,
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between', gap: 2, px: { xs: 2, md: 4 } }}>
        <Stack direction="row" spacing={1.5} sx={{ alignItems: 'center', minWidth: 0, flex: 1 }}>
          <IconButton
            onClick={openMobile}
            aria-label="Abrir menú"
            sx={{ display: { xs: 'inline-flex', sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap sx={{ display: { xs: 'block', md: 'none' }, fontWeight: 600 }}>
            {title}
          </Typography>
          <TextField
            size="small"
            placeholder="Buscar…"
            sx={{
              display: { xs: 'none', md: 'flex' },
              maxWidth: 320,
              '& .MuiOutlinedInput-root': { borderRadius: 2.5, bgcolor: 'background.paper' },
            }}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchOutlinedIcon fontSize="small" sx={{ color: 'text.secondary' }} />
                  </InputAdornment>
                ),
              },
            }}
          />
        </Stack>

        <Typography variant="h6" noWrap sx={{ display: { xs: 'none', md: 'block' }, fontWeight: 600 }}>
          {title}
        </Typography>

        <Stack direction="row" spacing={1.5} sx={{ alignItems: 'center', justifyContent: 'flex-end', flex: 1 }}>
          <IconButton
            onClick={toggleMode}
            aria-label="Cambiar tema claro/oscuro"
            sx={{ border: `1px solid ${theme.palette.divider}` }}
          >
            {mode === 'dark' ? <LightModeOutlinedIcon fontSize="small" /> : <DarkModeOutlinedIcon fontSize="small" />}
          </IconButton>

          <IconButton aria-label="Notificaciones">
            <Badge color="error" variant="dot" overlap="circular">
              <NotificationsNoneOutlinedIcon />
            </Badge>
          </IconButton>

          <IconButton onClick={handleOpenMenu} aria-label="Cuenta" sx={{ p: 0.5 }}>
            <InitialsAvatar name={usuario ?? '?'} sx={{ width: 36, height: 36, fontSize: '0.9rem' }} />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleCloseMenu}
            transformOrigin={{ horizontal: 'right', vertical: 'top' }}
            anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
          >
            <MenuItem disabled sx={{ opacity: '1 !important' }}>
              <ListItemText
                primary={usuario}
                secondary="Cuenta de demostración"
                slotProps={{ primary: { sx: { fontWeight: 600 } } }}
              />
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <LogoutOutlinedIcon fontSize="small" color="error" />
              </ListItemIcon>
              <ListItemText sx={{ color: 'error.main' }}>Cerrar sesión</ListItemText>
            </MenuItem>
          </Menu>
        </Stack>
      </Toolbar>
    </AppBar>
  );
}
