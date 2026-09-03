import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import { apiClient, getStoredAuth, setStoredAuth } from '../api/client';
import type { StoredAuth } from '../api/client';

interface AuthContextValue {
  usuario: string | null;
  isAuthenticated: boolean;
  login: (usuario: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [auth, setAuth] = useState<StoredAuth | null>(getStoredAuth);

  const login = async (usuario: string, password: string) => {
    const { data } = await apiClient.post<{ access: string; refresh: string }>('/token/', {
      username: usuario,
      password,
    });
    const nextAuth: StoredAuth = { access: data.access, refresh: data.refresh, usuario };
    setStoredAuth(nextAuth);
    setAuth(nextAuth);
  };

  const logout = () => {
    setStoredAuth(null);
    setAuth(null);
  };

  return (
    <AuthContext.Provider
      value={{ usuario: auth?.usuario ?? null, isAuthenticated: !!auth, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider');
  return ctx;
}
