import * as React from 'react';
import { Box, Grid } from '@mui/material';
import { SearchProvider } from '@elastic/react-search-ui';
import { SearchAppBar, UserHistoryContext } from '../Common';
import { WikiResults } from './WikiResults';
import { WikiFiltering } from './WikiFiltering';
import { History } from './History';
import { wiki_config } from '../../wikiConfig';

function Home() {
  const [histories, setHistories] = React.useState<string[]>([]);

  return (
    <UserHistoryContext.Provider value={{ histories, setHistories }}>
      <SearchProvider config={wiki_config}>
        <SearchAppBar />
        <Box sx={{ flexGrow: 1 }}>
          <Grid container spacing={2}>
            <Grid item xs={2}>
              <WikiFiltering />
              <History />
            </Grid>
            <Grid item xs={10}>
              <WikiResults />
            </Grid>
          </Grid>
        </Box>
      </SearchProvider>
    </UserHistoryContext.Provider>
  )
}
export { Home }