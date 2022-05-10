import { Routes, Route } from "react-router-dom";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import { Home, Test } from './components';

const lightTheme = createTheme({
  palette: {
    mode: 'light'
  },
})

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  const isDark = useMediaQuery('(prefers-color-scheme: dark)');
  return (
    <ThemeProvider theme={isDark ? darkTheme : lightTheme}>
      <Routes>
        <Route index element={<Home />} />
        <Route path="test" element={<Test />} />
      </Routes>
    </ThemeProvider>
  );
}

export default App;