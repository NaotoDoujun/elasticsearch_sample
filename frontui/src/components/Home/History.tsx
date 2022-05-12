
import { Paper, Typography, List, ListItem, ListItemButton, ListItemText } from '@mui/material';
const histories = ['History1', 'History2'];
function History() {
  return (
    <Paper sx={{
      p: 1, mt: 2, ml: 2,
      display: 'flex',
      flexDirection: 'column'
    }}>
      <Typography component="h2" variant="h6">History</Typography>
      <List component="nav">
        {histories.map(history => (
          <>
            <ListItem disablePadding divider>
              <ListItemButton>
                <ListItemText primary={history} />
              </ListItemButton>
            </ListItem>
          </>
        ))}
      </List>
    </Paper>
  )
}
export { History }