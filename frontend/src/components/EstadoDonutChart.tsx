import { useTheme } from '@mui/material';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';

interface EstadoDonutChartProps {
  preparando: number;
  enTransito: number;
  enAduana: number;
  entregados: number;
}

export default function EstadoDonutChart({ preparando, enTransito, enAduana, entregados }: EstadoDonutChartProps) {
  const theme = useTheme();

  const data = [
    { name: 'Preparando', value: preparando, color: theme.palette.grey[500] },
    { name: 'En tránsito', value: enTransito, color: theme.palette.info.main },
    { name: 'En aduana', value: enAduana, color: theme.palette.warning.main },
    { name: 'Entregados', value: entregados, color: theme.palette.success.main },
  ].filter((item) => item.value > 0);

  if (data.length === 0) {
    return null;
  }

  return (
    <ResponsiveContainer width="100%" height={260}>
      <PieChart>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          innerRadius={64}
          outerRadius={92}
          paddingAngle={3}
          isAnimationActive={false}
        >
          {data.map((entry) => (
            <Cell key={entry.name} fill={entry.color} stroke="none" />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: theme.palette.background.paper,
            border: `1px solid ${theme.palette.divider}`,
            borderRadius: 8,
            fontSize: 13,
          }}
        />
        <Legend verticalAlign="bottom" height={32} iconType="circle" wrapperStyle={{ fontSize: 12 }} />
      </PieChart>
    </ResponsiveContainer>
  );
}
