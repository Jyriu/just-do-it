import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import { RootState } from '../types/store';

const store = configureStore({
  reducer: {
    auth: authReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore ces actions pour la vérification de sérialisation
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export { store };
export type AppState = RootState;
export type AppDispatch = typeof store.dispatch; 