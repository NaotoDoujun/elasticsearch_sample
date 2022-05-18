import { WithSearch, Result } from '@elastic/react-search-ui';
import { Paper, Typography, Box } from '@mui/material';
type WikiResult = {
  id: {
    raw: string
  }
  title: {
    raw: string
    snippet: string
  }
  text: {
    raw: string
    snippet: string
  }
}
function Recommend() {
  return (
    <WithSearch mapContextToProps={({ results }) => ({ results })}>
      {({ results }) => {
        return (
          results.map((result: WikiResult) => (
            <Result key={result.id.raw}
              result={result}
              view={() => (
                <Paper key={result.id.raw} sx={{
                  p: 1, mt: 2, mr: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 120
                }}>
                  <Typography component="h2" variant="h6">{result.title.raw}</Typography>
                  <Box fontSize="fontSize" sx={{ my: 1, overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis" }}>
                    {result.text.raw}
                  </Box>
                </Paper>
              )}
            />
          ))
        )
      }}
    </WithSearch>
  )
}
export { Recommend }