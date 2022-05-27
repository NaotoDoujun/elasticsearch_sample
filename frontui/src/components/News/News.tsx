import { Box, Grid } from '@mui/material';
import { SearchProvider, WithSearch } from '@elastic/react-search-ui';
import { SearchAppBar, Filtering, History } from '../Common';
import { NewsResults } from './NewsResults';
import { news_config } from '../../newsConfig';

function News() {

  const newsOrder = [
    {
      field: "url",
      direction: "desc"
    },
    {
      field: "title",
      direction: "asc"
    }
  ];

  return (
    <SearchProvider config={news_config}>
      <WithSearch mapContextToProps={({ setSort }) => ({ setSort })}>
        {({ setSort }) => {
          setSort(newsOrder)
          return (
            <>
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
            </>
          )
        }}
      </WithSearch>
    </SearchProvider>
  )
}
export { News }