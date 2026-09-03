// Adaptado de nickelfox-v1.0.0/src/helpers/string-avatar.ts — genera un color
// determinístico a partir del nombre, para los avatares de las tablas.
function stringToColorAndContrast(name: string): { hex: string; contrastColor: string } {
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }

  let hex = '#';
  for (let i = 0; i < 3; i++) {
    const value = (hash >> (i * 8)) & 0xff;
    hex += `00${value.toString(16)}`.slice(-2);
  }

  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  const contrastColor = luminance > 0.5 ? '#000000' : '#FFFFFF';

  return { hex, contrastColor };
}

export function stringAvatarProps(name: string) {
  const { hex, contrastColor } = stringToColorAndContrast(name);
  return {
    sx: { bgcolor: hex, color: contrastColor },
    children: name.trim().charAt(0).toUpperCase(),
  };
}
