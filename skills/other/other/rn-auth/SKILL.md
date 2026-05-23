---
name: rn-auth
description: React Native authentication patterns for Expo apps. Use when implementing login flows, Google/Apple sign-in, token management, session handling, or debugging auth issues in Expo/React Native.
---

# React Native Authentication (Expo)

## Core Patterns

### Expo AuthSession for OAuth

Use `expo-auth-session` with `expo-web-browser` for OAuth flows:

```typescript
import * as AuthSession from 'expo-auth-session';
import * as WebBrowser from 'expo-web-browser';
import * as Google from 'expo-auth-session/providers/google';

// Critical: Call this at module level for proper redirect handling
WebBrowser.maybeCompleteAuthSession();

// Inside component
const [request, response, promptAsync] = Google.useAuthRequest({
  iosClientId: 'YOUR_IOS_CLIENT_ID.apps.googleusercontent.com',
  webClientId: 'YOUR_WEB_CLIENT_ID.apps.googleusercontent.com', // For backend verification
  scopes: ['profile', 'email'],
});
```

### Common Pitfalls

1. **Missing `maybeCompleteAuthSession()`** - Auth redirects fail silently without this at module level
2. **Wrong client ID** - iOS needs the iOS client ID, but backend verification needs the web client ID
3. **Scheme mismatch** - `app.json` scheme must match Google Cloud Console redirect URI
4. **Expo Go vs standalone** - Different redirect URIs; use `AuthSession.makeRedirectUri()` to handle both

### Token Storage

Use `expo-secure-store` for tokens (not AsyncStorage):

```typescript
import * as SecureStore from 'expo-secure-store';

const TOKEN_KEY = 'auth_token';
const REFRESH_KEY = 'refresh_token';

export const tokenStorage = {
  async save(token: string, refresh?: string) {
    await SecureStore.setItemAsync(TOKEN_KEY, token);
    if (refresh) {
      await SecureStore.setItemAsync(REFRESH_KEY, refresh);
    }
  },
  
  async get() {
    return SecureStore.getItemAsync(TOKEN_KEY);
  },
  
  async getRefresh() {
    return SecureStore.getItemAsync(REFRESH_KEY);
  },
  
  async clear() {
    await SecureStore.deleteItemAsync(TOKEN_KEY);
    await SecureStore.deleteItemAsync(REFRESH_KEY);
  },
};
```

### Auth Context Pattern

```typescript
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

type AuthState = {
  token: string | null;
  user: User | null;
  isLoading: boolean;
  signIn: (token: string, user: User) => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Restore session on mount
    async function restore() {
      try {
        const savedToken = await tokenStorage.get();
        if (savedToken) {
          // Validate token with backend before trusting it
          const userData = await validateToken(savedToken);
          setToken(savedToken);
          setUser(userData);
        }
      } catch {
        await tokenStorage.clear();
      } finally {
        setIsLoading(false);
      }
    }
    restore();
  }, []);

  const signIn = async (newToken: string, userData: User) => {
    await tokenStorage.save(newToken);
    setToken(newToken);
    setUser(userData);
  };

  const signOut = async () => {
    await tokenStorage.clear();
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, isLoading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be inside AuthProvider');
  return ctx;
};
```

### Protected Routes with Expo Router

```typescript
// app/_layout.tsx
import { Slot, useRouter, useSegments } from 'expo-router';
import { useAuth } from '@/contexts/auth';
import { useEffect } from 'react';

export default function RootLayout() {
  const { token, isLoading } = useAuth();
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) return;

    const inAuthGroup = segments[0] === '(auth)';

    if (!token && !inAuthGroup) {
      router.replace('/(auth)/login');
    } else if (token && inAuthGroup) {
      router.replace('/(app)/home');
    }
  }, [token, isLoading, segments]);

  if (isLoading) {
    return <LoadingScreen />;
  }

  return <Slot />;
}
```

## Backend Integration

### Sending Auth Headers

```typescript
// api/client.ts
import { tokenStorage } from '@/utils/tokenStorage';

const API_BASE = process.env.EXPO_PUBLIC_API_URL;

async function authFetch(path: string, options: RequestInit = {}) {
  const token = await tokenStorage.get();
  
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  if (response.status === 401) {
    // Token expired - try refresh or force logout
    const refreshed = await attemptTokenRefresh();
    if (!refreshed) {
      await tokenStorage.clear();
      // Trigger auth state update (emit event or use callback)
    }
  }

  return response;
}
```

### Google Token Verification (FastAPI backend)

```python
# For reference: backend should verify Google tokens like this
from google.oauth2 import id_token
from google.auth.transport import requests

def verify_google_token(token: str, client_id: str) -> dict:
    """Verify Google ID token and return user info."""
    idinfo = id_token.verify_oauth2_token(
        token, 
        requests.Request(), 
        client_id  # Use WEB client ID here, not iOS
    )
    return {
        "google_id": idinfo["sub"],
        "email": idinfo["email"],
        "name": idinfo.get("name"),
    }
```

## Debugging Auth Issues

### Check redirect URI configuration

```typescript
// Log the redirect URI being used
console.log('Redirect URI:', AuthSession.makeRedirectUri());
```

Compare this with what's configured in:
- Google Cloud Console > Credentials > OAuth 2.0 Client IDs
- `app.json` scheme field

### Common error patterns

| Error | Likely Cause |
|-------|--------------|
| "redirect_uri_mismatch" | Redirect URI in console doesn't match app |
| Auth popup opens but nothing happens | Missing `maybeCompleteAuthSession()` |
| Works in Expo Go, fails in build | Using Expo Go redirect URI in standalone config |
| Token validation fails on backend | Using iOS client ID instead of web client ID for verification |

### Test auth flow

1. Clear all tokens: `await tokenStorage.clear()`
2. Force kill app
3. Reopen and verify redirect to login
4. Complete sign-in flow
5. Force kill and reopen - should stay logged in
