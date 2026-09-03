import DotTag from './DotTag';
import type { EstadoEnvio } from '../api/types';

const ESTADO_CONFIG: Record<EstadoEnvio, { label: string; color: string }> = {
  entregado: { label: 'Entregado', color: 'success.main' },
  en_transito: { label: 'En tránsito', color: 'info.main' },
  en_aduana: { label: 'En aduana', color: 'warning.main' },
  preparando: { label: 'Preparando', color: 'text.disabled' },
};

export default function EstadoBadge({ estado }: { estado: EstadoEnvio }) {
  const config = ESTADO_CONFIG[estado] ?? { label: estado, color: 'text.disabled' };
  return <DotTag label={config.label} color={config.color} />;
}
