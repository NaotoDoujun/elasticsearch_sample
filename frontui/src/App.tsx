import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import { AppSettingsContext, Home, News } from './components';
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

function App() {
  const isDark = useMediaQuery('(prefers-color-scheme: dark)');
  const [isOpenDrawer, setIsOpenDrawer] = React.useState<boolean>(false);
  const [esIndex, setEsIndex] = React.useState<string>('jawiki');
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
        {esIndex === 'news' ? <News /> : <Home />}
      </AppSettingsContext.Provider>
    </ThemeProvider>
  );
}

export default App;