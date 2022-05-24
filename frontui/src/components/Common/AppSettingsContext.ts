import * as React from 'react';

export type AppSettingsContextType = {
  isOpenDrawer: boolean
  setIsOpenDrawer: React.Dispatch<React.SetStateAction<boolean>>
  esIndex: string
  setEsIndex: React.Dispatch<React.SetStateAction<string>>
  histories: Array<string>
  setHistories: React.Dispatch<React.SetStateAction<string[]>>
};

export const AppSettingsContext = React.createContext<AppSettingsContextType>({
  isOpenDrawer: false,
  setIsOpenDrawer: () => undefined,
  esIndex: '',
  setEsIndex: () => undefined,
  histories: [],
  setHistories: () => undefined
});