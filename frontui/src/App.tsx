import * as React from 'react';
import { Routes, Route, useLocation } from "react-router-dom";
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import { AppSettingsContext, Home, News, Tube } from './components';
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import "./components/Common/si-custom-styles.css";

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

const pathToIndex = (pathname: string) => {
  switch (pathname) {
    case "/news":
      return "news";
    case "/tube":
      return "tube";
    default:
      return "jawiki";
  }
}

function App() {
  const location = useLocation();
  const isDark = useMediaQuery('(prefers-color-scheme: dark)');
  const [isOpenDrawer, setIsOpenDrawer] = React.useState<boolean>(false);
  const [esIndex, setEsIndex] = React.useState<string>(pathToIndex(location.pathname));
  const [histories, setHistories] = React.useState<string[]>([]);
  return (
    <ThemeProvider theme={isDark ? darkTheme : lightTheme}>
      <CssBaseline />
      <AppSettingsContext.Provider value={{
        isOpenDrawer,
        setIsOpenDrawer,
        esIndex,
        setEsIndex,
        histories,
        setHistories
      }}>
        <Routes>
          <Route index element={<Home />} />
          <Route path='/news' element={<News />} />
          <Route path='/tube' element={<Tube />} />
        </Routes>
      </AppSettingsContext.Provider>
    </ThemeProvider>
  );
}

export default App;