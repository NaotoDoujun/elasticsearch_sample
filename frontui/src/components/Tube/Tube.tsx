import { Box, Grid } from '@mui/material';
import { SearchProvider, WithSearch } from '@elastic/react-search-ui';
import { SearchAppBar, Filtering, History } from '../Common';
import { TubeResults } from './TubeResults';
import { tube_config } from '../../tubeConfig';

function Tube() {

  const tubeOrder = [
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
    <SearchProvider config={tube_config}>
      <WithSearch mapContextToProps={({ setSort }) => ({ setSort })}>
        {({ setSort }) => {
          setSort(tubeOrder)
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
                    <TubeResults />
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
export { Tube }