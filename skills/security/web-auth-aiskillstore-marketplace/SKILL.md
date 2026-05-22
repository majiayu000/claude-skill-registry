---
name: web-auth
description: Authentication patterns for React web applications. Use when implementing login flows, OAuth, JWT handling, session management, or protected routes in React web apps.
---

# Web Authentication (React)

## Core Patterns

### JWT Token Storage

**Options and trade-offs:**

| Storage | XSS Safe | CSRF Safe | Best For |
|---------|----------|-----------|----------|
| httpOnly cookie | Yes | No (needs CSRF token) | Most secure for tokens |
| localStorage | No | Yes | Simple apps, short-lived tokens |
| Memory (state) | Yes | Yes | Very short-lived tokens with refresh |

### Cookie-Based Auth (Recommended)

```typescript
// API client setup
const api = {
  async login(email: string, password: string) {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include', // Important: send/receive cookies
      body: JSON.stringify({ email, password }),
    });
    return response.json();
  },

  async logout() {
    await fetch('/api/auth/logout', {
      method: 'POST',
      credentials: 'include',
    });
  },

  async getUser() {
    const response = await fetch('/api/auth/me', {
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Not authenticated');
    return response.json();
  },
};
```

### Auth Context Pattern

```typescript
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check auth status on mount
    checkAuth();
  }, []);

  async function checkAuth() {
    try {
      const userData = await api.getUser();
      setUser(userData);
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }

  async function login(email: string, password: string) {
    const { user } = await api.login(email, password);
    setUser(user);
  }

  async function logout() {
    await api.logout();
    setUser(null);
  }

  async function refresh() {
    await checkAuth();
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        logout,
        refresh,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

---

## OAuth Patterns

### Google OAuth (Web)

```typescript
// Using Google Identity Services
import { useEffect } from 'react';

declare global {
  interface Window {
    google: any;
  }
}

function GoogleLoginButton() {
  useEffect(() => {
    // Load Google Identity Services script
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    document.body.appendChild(script);

    script.onload = () => {
      window.google.accounts.id.initialize({
        client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID,
        callback: handleGoogleResponse,
      });

      window.google.accounts.id.renderButton(
        document.getElementById('google-signin'),
        { theme: 'outline', size: 'large' }
      );
    };

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  async function handleGoogleResponse(response: { credential: string }) {
    // Send token to backend for verification
    const result = await fetch('/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ token: response.credential }),
    });

    if (result.ok) {
      window.location.href = '/dashboard';
    }
  }

  return <div id="google-signin" />;
}
```

### NextAuth.js (Recommended for Next.js)

```typescript
// pages/api/auth/[...nextauth].ts or app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import CredentialsProvider from 'next-auth/providers/credentials';

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        // Verify credentials against your database
        const user = await verifyCredentials(
          credentials?.email,
          credentials?.password
        );
        return user ?? null;
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      session.user.id = token.id;
      return session;
    },
  },
};

export default NextAuth(authOptions);
```

```typescript
// Usage in components
import { useSession, signIn, signOut } from 'next-auth/react';

function AuthButton() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <Spinner />;
  }

  if (session) {
    return (
      <div>
        <span>Signed in as {session.user?.email}</span>
        <button onClick={() => signOut()}>Sign out</button>
      </div>
    );
  }

  return (
    <div>
      <button onClick={() => signIn('google')}>Sign in with Google</button>
      <button onClick={() => signIn('credentials')}>Sign in</button>
    </div>
  );
}
```

---

## Protected Routes

### React Router

```typescript
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/auth';

function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    // Redirect to login, preserving intended destination
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
}

// Usage in router
<Routes>
  <Route path="/login" element={<LoginPage />} />
  <Route element={<ProtectedRoute />}>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/settings" element={<Settings />} />
  </Route>
</Routes>
```

### Next.js App Router

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/settings/:path*'],
};
```

```typescript
// app/dashboard/layout.tsx
import { redirect } from 'next/navigation';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/app/api/auth/[...nextauth]/route';

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getServerSession(authOptions);

  if (!session) {
    redirect('/login');
  }

  return <>{children}</>;
}
```

---

## Token Refresh Pattern

```typescript
// API client with automatic token refresh
class ApiClient {
  private refreshPromise: Promise<void> | null = null;

  async fetch(url: string, options: RequestInit = {}) {
    const response = await fetch(url, {
      ...options,
      credentials: 'include',
    });

    if (response.status === 401) {
      // Token expired, try refresh
      await this.refreshToken();
      // Retry original request
      return fetch(url, { ...options, credentials: 'include' });
    }

    return response;
  }

  private async refreshToken() {
    // Deduplicate refresh requests
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    this.refreshPromise = fetch('/api/auth/refresh', {
      method: 'POST',
      credentials: 'include',
    }).then(async (response) => {
      if (!response.ok) {
        // Refresh failed, logout user
        window.location.href = '/login';
        throw new Error('Session expired');
      }
    }).finally(() => {
      this.refreshPromise = null;
    });

    return this.refreshPromise;
  }
}

export const api = new ApiClient();
```

---

## Form Handling

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginForm = z.infer<typeof loginSchema>;

function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
  });

  async function onSubmit(data: LoginForm) {
    try {
      await login(data.email, data.password);
      // Redirect to intended page or dashboard
      const from = location.state?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
    } catch (error) {
      setError('root', {
        message: 'Invalid email or password',
      });
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="email">Email</label>
        <input {...register('email')} type="email" id="email" />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input {...register('password')} type="password" id="password" />
        {errors.password && <span>{errors.password.message}</span>}
      </div>

      {errors.root && <div className="error">{errors.root.message}</div>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Signing in...' : 'Sign in'}
      </button>
    </form>
  );
}
```

---

## Security Best Practices

### CSRF Protection

```typescript
// Server: Include CSRF token in response
// Client: Send with requests
async function fetchWithCSRF(url: string, options: RequestInit = {}) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'X-CSRF-Token': csrfToken || '',
    },
    credentials: 'include',
  });
}
```

### Security Headers (Server)

```typescript
// Next.js next.config.js
const securityHeaders = [
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY',
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block',
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=31536000; includeSubDomains',
  },
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Cookie not sent | Add `credentials: 'include'` to fetch |
| CORS error with cookies | Server must set `Access-Control-Allow-Credentials: true` |
| Session lost on refresh | Verify cookie settings (domain, path, secure) |
| OAuth redirect fails | Check redirect URI in provider console |
| Token in localStorage stolen | Move to httpOnly cookies |

---

## Backend Integration (FastAPI)

```python
# For reference: FastAPI auth endpoints
from fastapi import FastAPI, Response, Depends, HTTPException
from fastapi.security import HTTPBearer

@app.post("/api/auth/login")
async def login(credentials: LoginRequest, response: Response):
    user = await verify_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token(user.id)
    response.set_cookie(
        key="auth-token",
        value=token,
        httponly=True,
        secure=True,  # HTTPS only
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )
    return {"user": user}

@app.post("/api/auth/logout")
async def logout(response: Response):
    response.delete_cookie("auth-token")
    return {"success": True}
```
