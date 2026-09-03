import { useState } from 'react';
import { AxiosError } from 'axios';
import { apiClient } from './client';

export type FieldErrors = Record<string, string[]>;

interface MutationState {
  loading: boolean;
  fieldErrors: FieldErrors;
  generalError: string | null;
}

type MutationResult<T> = { ok: true; data: T } | { ok: false };

type Method = 'post' | 'patch' | 'delete';

/** Maneja el ciclo de una escritura contra la API (crear/editar/borrar):
 * loading, errores de validación por campo (los que devuelve DRF) y un
 * error general para fallos que no vienen desglosados por campo. El
 * resultado es explícito (`ok: true/false`) para no confundir un DELETE
 * exitoso (sin cuerpo) con un error. */
export function useApiMutation<TResponse = unknown>() {
  const [state, setState] = useState<MutationState>({ loading: false, fieldErrors: {}, generalError: null });

  const mutate = async (method: Method, url: string, data?: unknown): Promise<MutationResult<TResponse>> => {
    setState({ loading: true, fieldErrors: {}, generalError: null });
    try {
      const response = await apiClient.request<TResponse>({ method, url, data });
      setState({ loading: false, fieldErrors: {}, generalError: null });
      return { ok: true, data: response.data };
    } catch (err) {
      const axiosErr = err as AxiosError<Record<string, unknown>>;
      const payload = axiosErr.response?.data;

      if (payload && typeof payload === 'object') {
        const fieldErrors: FieldErrors = {};
        let generalError: string | null = null;
        for (const [key, value] of Object.entries(payload)) {
          const messages = Array.isArray(value) ? value.map(String) : [String(value)];
          if (key === 'detail' || key === 'non_field_errors') {
            generalError = messages.join(' ');
          } else {
            fieldErrors[key] = messages;
          }
        }
        setState({ loading: false, fieldErrors, generalError });
      } else {
        setState({ loading: false, fieldErrors: {}, generalError: 'No se pudo completar la operación. Intenta de nuevo.' });
      }
      return { ok: false };
    }
  };

  return {
    ...state,
    create: (url: string, data: unknown) => mutate('post', url, data),
    update: (url: string, data: unknown) => mutate('patch', url, data),
    remove: (url: string) => mutate('delete', url),
  };
}
