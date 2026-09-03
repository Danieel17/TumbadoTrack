import { useEffect, useState, useCallback } from 'react';
import { apiClient } from './client';

interface ApiResourceState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  reload: () => void;
}

/** Trae un recurso GET del backend y expone loading/error, listo para usar
 * en cualquier página. `deps` re-dispara el fetch (ej. al cambiar un filtro). */
export function useApiResource<T>(url: string, deps: unknown[] = []): ApiResourceState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  const reload = useCallback(() => setTick((t) => t + 1), []);

  useEffect(() => {
    let cancelado = false;
    setLoading(true);
    setError(null);

    apiClient
      .get<T>(url)
      .then((res) => {
        if (!cancelado) setData(res.data);
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar la información. Intenta de nuevo.');
      })
      .finally(() => {
        if (!cancelado) setLoading(false);
      });

    return () => {
      cancelado = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url, tick, ...deps]);

  return { data, loading, error, reload };
}
