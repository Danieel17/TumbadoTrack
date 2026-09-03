import { useTheme } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import type { Proveedor } from '../api/types';

export default function PuntualidadBarChart({ proveedores }: { proveedores: Proveedor[] }) {
  const theme = useTheme();

  const data = proveedores
    .map((p) => ({ nombre: p.nombre.split(' ')[0], puntualidad: Number(p.tasa_puntualidad) }))
    .sort((a, b) => b.puntualidad - a.puntualidad);

  if (data.length === 0) {
    return null;
  }

  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} vertical={false} />
        <XAxis dataKey="nombre" tick={{ fontSize: 12, fill: theme.palette.text.secondary }} axisLine={false} tickLine={false} />
        <YAxis
          domain={[0, 100]}
          tick={{ fontSize: 12, fill: theme.palette.text.secondary }}
          axisLine={false}
          tickLine={false}
          width={36}
        />
        <Tooltip
          cursor={{ fill: theme.palette.action.hover }}
          contentStyle={{
            backgroundColor: theme.palette.background.paper,
            border: `1px solid ${theme.palette.divider}`,
            borderRadius: 8,
            fontSize: 13,
          }}
          formatter={(value) => [`${value}%`, 'Puntualidad']}
        />
        <Bar dataKey="puntualidad" radius={[6, 6, 0, 0]} isAnimationActive={false}>
          {data.map((entry) => (
            <Cell key={entry.nombre} fill={theme.palette.secondary.main} opacity={0.6 + (entry.puntualidad / 100) * 0.4} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
