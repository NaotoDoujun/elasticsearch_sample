import * as React from 'react';
import {
  Card,
  CardHeader,
  IconButton,
  CardContent,
  Divider,
  FormControl,
  InputLabel,
  MenuItem
} from '@mui/material';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { AppSettingsContext } from '../Common';
import { Close as CloseIcon } from '@mui/icons-material';
import { useNavigate } from "react-router-dom";

function Settings() {
  const navigate = useNavigate();
  const { setIsOpenDrawer, esIndex, setEsIndex, setHistories } = React.useContext(AppSettingsContext);

  const toggleDrawer = (open: boolean) =>
    (event: React.KeyboardEvent | React.MouseEvent) => {
      if (
        event.type === 'keydown' &&
        ((event as React.KeyboardEvent).key === 'Tab' ||
          (event as React.KeyboardEvent).key === 'Shift')
      ) {
        return;
      }
      setIsOpenDrawer(open);
    };

  const handleChange = (event: SelectChangeEvent) => {
    const index = event.target.value as string;
    setEsIndex(index);
    setHistories([]);
    navigate(index === "jawiki" ? "/" : "/news", { replace: true });
  };

  return (
    <Card>
      <CardHeader title="Settings" action={
        <IconButton aria-label="settings" onClick={toggleDrawer(false)}>
          <CloseIcon />
        </IconButton>
      } />
      <Divider />
      <CardContent>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel id="esindex-select-label">Es Index</InputLabel>
          <Select
            labelId="esindex-select-label"
            id="esindex-select"
            value={esIndex}
            label="ES Index"
            onChange={handleChange}
          >
            <MenuItem value="jawiki">jawiki</MenuItem>
            <MenuItem value="news">news</MenuItem>
          </Select>
        </FormControl>
      </CardContent>
    </Card>
  )
}

export { Settings }