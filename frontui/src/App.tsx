import * as React from 'react';
import { SearchProvider } from '@elastic/react-search-ui';
import { Routes, Route } from "react-router-dom";
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import { UserHistoryContext, SearchAppBar, Home } from './components';
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import "./components/Home/si-custom-styles.css";
import { wiki_config } from './wikiConfig';

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
  const [histories, setHistories] = React.useState<string[]>([]);

  return (
    <ThemeProvider theme={isDark ? darkTheme : lightTheme}>
      <CssBaseline />
      <SearchProvider config={wiki_config}>
        <UserHistoryContext.Provider value={{ histories, setHistories }}>
          <SearchAppBar />
          <Routes>
            <Route index element={<Home />} />
          </Routes>
        </UserHistoryContext.Provider>
      </SearchProvider>
    </ThemeProvider>
  );
}

export default App;