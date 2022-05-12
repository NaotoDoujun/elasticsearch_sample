import { Paper, Typography, Box } from '@mui/material';
const recommends = ['Recommend1', 'Recommend2'];
function Recommend() {
  return (
    <>
      {recommends.map(recommend => (

        <Paper sx={{
          p: 1, mt: 2, mr: 2,
          display: 'flex',
          flexDirection: 'column',
          height: 120
        }}>
          <Typography>{recommend}</Typography>
          <Box sx={{ my: 1 }}>
            {recommend}Contents
          </Box>
        </Paper>
      ))}
    </>
  )
}
export { Recommend }