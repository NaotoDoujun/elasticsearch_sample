import { Box, Grid } from '@mui/material';
import { SearchProvider } from '@elastic/react-search-ui';
import { SearchAppBar, Filtering, History } from '../Common';
import { NewsResults } from './NewsResults';
import { news_config } from '../../newsConfig';

function News() {
  return (
    <SearchProvider config={news_config}>
      <SearchAppBar />
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={2}>
          <Grid item xs={2}>
            <Filtering />
            <History />
          </Grid>
          <Grid item xs={10}>
            <NewsResults />
          </Grid>
        </Grid>
      </Box>
    </SearchProvider>
  )
}
export { News }