import { createTheme } from '@mui/material';
import type { Theme } from '@mui/material';
import { darkPalette, lightPalette } from './palette';

export type ThemeMode = 'light' | 'dark';

const HEADING_FONT = "'Bebas Neue', 'Inter', sans-serif";

export function buildTheme(mode: ThemeMode): Theme {
  const isDark = mode === 'dark';

  return createTheme({
    palette: isDark ? darkPalette : lightPalette,
    // Radio base más grande que el "8px de manual" — junto con las sombras
    // de MuiPaper de abajo, es lo que le da a las tarjetas una sensación
    // más propia y menos "admin template por defecto".
    shape: {
      borderRadius: 14,
    },
    typography: {
      fontFamily: ['Inter', 'Roboto', 'sans-serif'].join(', '),
      // Los títulos usan una fuente condensada de trazo grueso (afiche de
      // concierto) en vez de heredar Inter — la identidad tipográfica no
      // vive solo en el logotipo.
      h1: { fontFamily: HEADING_FONT, letterSpacing: '0.02em' },
      h2: { fontFamily: HEADING_FONT, letterSpacing: '0.02em' },
      h3: { fontFamily: HEADING_FONT, letterSpacing: '0.02em' },
      h4: { fontFamily: HEADING_FONT, letterSpacing: '0.03em' },
      h5: { fontFamily: HEADING_FONT, letterSpacing: '0.03em' },
      h6: { fontFamily: HEADING_FONT, letterSpacing: '0.04em', textTransform: 'uppercase' },
      button: {
        textTransform: 'none',
        fontWeight: 600,
      },
    },
    components: {
      MuiPaper: {
        styleOverrides: {
          root: {
            backgroundImage: 'none',
          },
        },
        variants: [
          {
            props: { variant: 'outlined' },
            style: {
              borderColor: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(15,23,42,0.08)',
              boxShadow: isDark
                ? '0 12px 32px -20px rgba(0,0,0,0.6)'
                : '0 1px 2px rgba(15,23,42,0.03), 0 12px 28px -16px rgba(15,23,42,0.12)',
            },
          },
        ],
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 10,
          },
        },
      },
      MuiChip: {
        styleOverrides: {
          root: {
            borderRadius: 6,
          },
        },
      },
      MuiAppBar: {
        styleOverrides: {
          root: {
            boxShadow: 'none',
          },
        },
      },
      // MuiLink hereda "primary" por defecto — como primary es el rojo de
      // marca, todos los enlaces (códigos de envío, "Ver tracking", etc.)
      // salían en rojo vivo sin que nadie lo pidiera, dando una sensación
      // de alerta/error repetida por toda la app. Se cambia el color por
      // defecto a `secondary` (el tostado del logo), más cálido y neutro.
      MuiLink: {
        defaultProps: {
          color: 'secondary',
        },
        styleOverrides: {
          root: {
            fontWeight: 600,
          },
        },
      },
    },
  });
}
