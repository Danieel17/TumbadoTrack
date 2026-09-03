import { Avatar } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import { stringAvatarProps } from '../helpers/stringAvatar';

interface InitialsAvatarProps {
  name: string;
  sx?: SxProps<Theme>;
}

export default function InitialsAvatar({ name, sx }: InitialsAvatarProps) {
  const { sx: colorSx, children } = stringAvatarProps(name);
  return <Avatar sx={{ ...colorSx, ...sx }}>{children}</Avatar>;
}
