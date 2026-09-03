import { useEffect, useState } from 'react';

/** Anima un número de 0 hasta `target` con easing, cada vez que `target`
 * cambia (por ejemplo al cargar los datos del dashboard). */
export function useCountUp(target: number, durationMs = 800): number {
  const [valor, setValor] = useState(0);

  useEffect(() => {
    let frame = 0;
    let inicio: number | null = null;
    setValor(0);

    function paso(timestamp: number) {
      if (inicio === null) inicio = timestamp;
      const progreso = Math.min((timestamp - inicio) / durationMs, 1);
      const facilitado = 1 - Math.pow(1 - progreso, 3);
      setValor(Math.round(target * facilitado));
      if (progreso < 1) {
        frame = requestAnimationFrame(paso);
      }
    }

    frame = requestAnimationFrame(paso);
    return () => cancelAnimationFrame(frame);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, durationMs]);

  return valor;
}
