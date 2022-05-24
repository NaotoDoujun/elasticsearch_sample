import { Box, Grid } from '@mui/material';
import { SearchProvider } from '@elastic/react-search-ui';
import { SearchAppBar, Filtering, History } from '../Common';
import { WikiResults } from './WikiResults';
import { wiki_config } from '../../wikiConfig';

function Home() {
  return (
    <SearchProvider config={wiki_config}>
      <SearchAppBar />
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={2}>
          <Grid item xs={2}>
            <Filtering />
            <History />
          </Grid>
          <Grid item xs={10}>
            <WikiResults />
          </Grid>
        </Grid>
      </Box>
    </SearchProvider>
  )
}
export { Home }