
import { Paper, Typography, List, ListItem, ListItemButton, ListItemText } from '@mui/material';
const histories = ['History1', 'History2'];
function History() {
  return (
    <Paper sx={{
      p: 1, mt: 2, ml: 2,
      display: 'flex',
      flexDirection: 'column'
    }}>
      <Typography>History</Typography>
      <List>
        {histories.map(history => (
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemText primary={history} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Paper>
  )
}
export { History }