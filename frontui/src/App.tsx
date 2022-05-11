import { SearchProvider } from '@elastic/react-search-ui';
import { Routes, Route } from "react-router-dom";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import { SearchAppBar, Home } from './components';
import { wiki_config } from './wikiConfig'

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
      <SearchProvider config={wiki_config}>
        <SearchAppBar />
        <Routes>
          <Route index element={<Home />} />
        </Routes>
      </SearchProvider>
    </ThemeProvider>
  );
}

export default App;