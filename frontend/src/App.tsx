import { Routes, Route } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import RequireAuth from './components/RequireAuth';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Envios from './pages/Envios';
import EnvioDetalle from './pages/EnvioDetalle';
import Proveedores from './pages/Proveedores';
import Clientes from './pages/Clientes';
import Productos from './pages/Productos';
import Bodegas from './pages/Bodegas';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        element={
          <RequireAuth>
            <AppLayout />
          </RequireAuth>
        }
      >
        <Route path="/" element={<Dashboard />} />
        <Route path="/envios" element={<Envios />} />
        <Route path="/envios/:id" element={<EnvioDetalle />} />
        <Route path="/proveedores" element={<Proveedores />} />
        <Route path="/clientes" element={<Clientes />} />
        <Route path="/productos" element={<Productos />} />
        <Route path="/bodegas" element={<Bodegas />} />
      </Route>
    </Routes>
  );
}

export default App;
