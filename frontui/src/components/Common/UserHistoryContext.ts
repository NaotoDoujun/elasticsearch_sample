import * as React from 'react';

export type UserHistoryContextType = {
  histories: Array<string>
  setHistories: React.Dispatch<React.SetStateAction<string[]>>
};

export const UserHistoryContext = React.createContext<UserHistoryContextType>({
  histories: [],
  setHistories: () => undefined
});