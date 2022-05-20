
import { Box, Grid } from '@mui/material';
import { SearchResults } from './Results';
import { Filtering } from './Filtering';
import { History } from './History';

function Home() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={2}>
          <Filtering />
          <History />
        </Grid>
        <Grid item xs={10}>
          <SearchResults />
        </Grid>
      </Grid>
    </Box>
  )
}
export { Home }