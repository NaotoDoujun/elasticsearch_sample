import { Paper, Typography, Box } from '@mui/material';
const recommends = ['Recommend1', 'Recommend2'];
function Recommend() {
  return (
    <>
      {recommends.map((recommend, index) => (
        <Paper key={index} sx={{
          p: 1, mt: 2, mr: 2,
          display: 'flex',
          flexDirection: 'column',
          height: 120
        }}>
          <Typography component="h2" variant="h6">{recommend}</Typography>
          <Box sx={{ my: 1 }}>
            {recommend}'s Context
          </Box>
        </Paper>
      ))}
    </>
  )
}
export { Recommend }