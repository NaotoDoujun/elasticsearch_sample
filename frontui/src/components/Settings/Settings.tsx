import {
  Card,
  CardHeader,
  IconButton,
  CardContent,
  Divider,
  FormGroup,
  FormControlLabel,
  Checkbox
} from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';

function Settings() {
  return (
    <Card>
      <CardHeader title="Settings" action={
        <IconButton aria-label="settings">
          <CloseIcon />
        </IconButton>
      } />
      <Divider />
      <CardContent>
        <FormGroup>
          <FormControlLabel control={<Checkbox />} label="Option1" />
          <FormControlLabel control={<Checkbox />} label="Option2" />
        </FormGroup>
      </CardContent>
    </Card>
  )
}

export { Settings }