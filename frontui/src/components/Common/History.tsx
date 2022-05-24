import * as React from 'react';
import { Paper, Typography, IconButton, List, ListItem, ListItemText } from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';
import { AppSettingsContext } from '.';
function History() {

  const { histories, setHistories } = React.useContext(AppSettingsContext);
  const reversed = [...histories].reverse();

  const handleDeleteHistories = () => {
    setHistories([]);
  }

  return (
    <Paper sx={{
      p: 1, mt: 2, ml: 2,
      display: 'flex',
      flexDirection: 'column'
    }}>
      <Typography component="h2" variant="h6">History
        <IconButton onClick={handleDeleteHistories}><DeleteIcon /></IconButton>
      </Typography>
      <List component="nav">
        {reversed.map((history, index) => (
          <ListItem key={index} disablePadding divider>
            <ListItemText primary={history} />
          </ListItem>
        ))}
      </List>
    </Paper>
  )
}
export { History }