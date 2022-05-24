
import { Facet } from "@elastic/react-search-ui";
import { Paper, Typography } from '@mui/material';
function Filtering() {
  return (
    <Paper sx={{
      p: 1, mt: 2, ml: 2,
      display: 'flex',
      flexDirection: 'column'
    }}>
      <Typography component="h2" variant="h6">Filter</Typography>
      <Facet field="title.keyword" label="Title" />
    </Paper>
  )
}
export { Filtering }