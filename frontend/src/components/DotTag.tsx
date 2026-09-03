import { Box, Typography } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';

interface DotTagProps {
  label: string;
  color: string;
  sx?: SxProps<Theme>;
}

/** Reemplazo del Chip "outlined" default de MUI: un punto de color + texto,
 * sin contorno ni fondo — menos "plantilla de admin dashboard". */
export default function DotTag({ label, color, sx }: DotTagProps) {
  return (
    <Box sx={{ display: 'inline-flex', alignItems: 'center', gap: 0.75, ...sx }}>
      <Box sx={{ width: 7, height: 7, borderRadius: '50%', bgcolor: color, flexShrink: 0 }} />
      <Typography variant="body2" sx={{ color, fontWeight: 600, whiteSpace: 'nowrap' }}>
        {label}
      </Typography>
    </Box>
  );
}
