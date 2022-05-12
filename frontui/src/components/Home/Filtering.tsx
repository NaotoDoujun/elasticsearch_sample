
import { Paper, Typography, List, ListItem, ListItemButton, ListItemText } from '@mui/material';
const filters = ['Filter1', 'Filter2'];
function Filtering() {
  return (
    <Paper sx={{
      p: 1, mt: 2, ml: 2,
      display: 'flex',
      flexDirection: 'column'
    }}>
      <Typography>Filter</Typography>
      <List>
        {filters.map(filter => (
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemText primary={filter} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Paper>
  )
}
export { Filtering }