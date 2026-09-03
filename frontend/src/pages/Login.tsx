import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Stack,
  TextField,
  Typography,
  Button,
  Alert,
  IconButton,
  useTheme,
} from '@mui/material';
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined';
import { useAuth } from '../context/AuthContext';
import { useThemeMode } from '../context/ThemeModeContext';
import { brandRed } from '../theme/colors';

export default function Login() {
  const [usuario, setUsuario] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [cargando, setCargando] = useState(false);
  const { login } = useAuth();
  const { mode, toggleMode } = useThemeMode();
  const theme = useTheme();
  const navigate = useNavigate();

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setCargando(true);
    try {
      await login(usuario, password);
      navigate('/', { replace: true });
    } catch {
      setError('Usuario o contraseña incorrectos.');
    } finally {
      setCargando(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        px: 2,
        position: 'relative',
      }}
    >
      <IconButton
        onClick={toggleMode}
        sx={{ position: 'fixed', top: 20, right: 20, border: `1px solid ${theme.palette.divider}` }}
        aria-label="Cambiar tema claro/oscuro"
      >
        {mode === 'dark' ? <LightModeOutlinedIcon fontSize="small" /> : <DarkModeOutlinedIcon fontSize="small" />}
      </IconButton>

      <Box sx={{ width: '100%', maxWidth: 420 }}>
        <Stack spacing={1} sx={{ mb: 3, alignItems: 'center' }}>
          <Box component="img" src="/logo.png" alt="TumbadoTrack" sx={{ height: 64, width: 64, objectFit: 'contain' }} />
          <Typography
            sx={{
              fontFamily: "'Mogra', cursive",
              fontSize: '2rem',
              letterSpacing: '0.02em',
              color: brandRed[500],
            }}
          >
            TumbadoTrack
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Music Pro Company · Courier
          </Typography>
        </Stack>

        <Paper sx={{ p: 4, borderRadius: 3 }} variant="outlined">
          <Typography variant="h6" sx={{ mb: 3, textAlign: 'center', fontWeight: 600 }}>
            Iniciar sesión
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit}>
            <Stack spacing={2}>
              <TextField
                label="Usuario"
                autoComplete="username"
                value={usuario}
                onChange={(e) => setUsuario(e.target.value)}
                required
                fullWidth
              />
              <TextField
                label="Contraseña"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                fullWidth
              />
              <Button type="submit" variant="contained" size="large" disabled={cargando} fullWidth>
                {cargando ? 'Entrando…' : 'Entrar'}
              </Button>
            </Stack>
          </Box>

          <Typography variant="caption" color="text.secondary" sx={{ mt: 3, display: 'block', textAlign: 'center' }}>
            Acceso de demostración · usuario <code>admin</code> / contraseña <code>admin123</code>
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
}
