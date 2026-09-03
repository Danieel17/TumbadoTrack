import type { PaletteOptions } from '@mui/material';
import { stone, green, yellowOrange, pinkishRed, bluishCyan, brandRed, brandTan } from './colors';

// La marca son los dos colores reales del logo: rojo (flechas) + tostado
// (perezoso). Antes `primary` era un teal genérico que no tenía relación
// con el logo — ahora sí. Los estados (en tránsito, aduana, entregado)
// usan colores semánticos independientes (info/warning/success) para que
// el significado no dependa del color de marca.
export const lightPalette: PaletteOptions = {
  mode: 'light',
  primary: {
    light: brandRed[300],
    main: brandRed[500],
    dark: brandRed[700],
    contrastText: '#FFFFFF',
  },
  secondary: {
    light: brandTan[300],
    main: brandTan[600],
    dark: brandTan[800],
    contrastText: '#FFFFFF',
  },
  success: {
    light: green[100],
    main: green[600],
    dark: green[800],
  },
  info: {
    light: bluishCyan[100],
    main: bluishCyan[600],
    dark: bluishCyan[800],
  },
  warning: {
    light: yellowOrange[100],
    main: yellowOrange[600],
    dark: yellowOrange[800],
  },
  error: {
    light: pinkishRed[100],
    main: pinkishRed[600],
    dark: pinkishRed[800],
  },
  background: {
    default: stone[100],
    paper: '#FFFFFF',
  },
  text: {
    primary: stone[900],
    secondary: stone[600],
    disabled: stone[400],
  },
  divider: stone[200],
};

export const darkPalette: PaletteOptions = {
  mode: 'dark',
  primary: {
    light: brandRed[200],
    main: brandRed[400],
    dark: brandRed[700],
    contrastText: '#FFFFFF',
  },
  secondary: {
    light: brandTan[200],
    main: brandTan[400],
    dark: brandTan[700],
    contrastText: '#2A2118',
  },
  success: {
    light: green[200],
    main: green[400],
    dark: green[700],
  },
  info: {
    light: bluishCyan[200],
    main: bluishCyan[400],
    dark: bluishCyan[700],
  },
  warning: {
    light: yellowOrange[200],
    main: yellowOrange[400],
    dark: yellowOrange[700],
  },
  error: {
    light: pinkishRed[200],
    main: pinkishRed[400],
    dark: pinkishRed[700],
  },
  background: {
    default: stone[900],
    paper: stone[800],
  },
  text: {
    primary: stone[100],
    secondary: stone[400],
    disabled: stone[600],
  },
  divider: stone[700],
};
