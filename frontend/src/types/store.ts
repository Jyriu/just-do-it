interface User {
  id: number;
  username: string;
  email: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

interface RootState {
  auth: AuthState;
} 

export type { User, AuthState, RootState };