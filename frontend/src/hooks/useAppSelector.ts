import { useSelector, TypedUseSelectorHook } from 'react-redux';
import type { AppState } from '../store';

export const useAppSelector: TypedUseSelectorHook<AppState> = useSelector; 