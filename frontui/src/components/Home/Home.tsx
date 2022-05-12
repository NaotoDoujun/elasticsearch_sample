
import { Box, Grid } from '@mui/material';
import { SearchResults } from './Results';
import { Filtering } from './Filtering';
import { History } from './History';
import { Recommend } from './Recommend';

function Home() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={2}>
          <Filtering />
          <History />
        </Grid>
        <Grid item xs={7}>
          <SearchResults />
        </Grid>
        <Grid item xs={3}>
          <Recommend />
        </Grid>
      </Grid>
    </Box>
  )
}
export { Home }