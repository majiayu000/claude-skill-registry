---
name: better-auth-sso
description: Integrate with Better Auth SSO for OAuth2/OIDC authentication. Use this skill when implementing SSO login flows, PKCE authentication, token management, JWKS verification, or global logout in Next.js applications connecting to a Better Auth server.
---

# Better Auth SSO Integration

Integrate Next.js applications with Better Auth SSO using OAuth 2.1 / OIDC with PKCE flow.

## When to Use

- Implementing SSO login in Next.js apps
- Setting up PKCE-based OAuth flow (public clients)
- Managing tokens in httpOnly cookies
- Verifying JWTs using JWKS
- Implementing global logout across apps

## Architecture Overview

```
┌─────────────────┐
│ Better Auth SSO │ ← Central auth server
│  (Auth Server)  │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌───────┐
│ App 1 │  │ App 2 │ ← Tenant apps (SSO clients)
└───────┘  └───────┘
```

## Quick Start

```bash
# Dependencies
npm install jose

# Environment
NEXT_PUBLIC_SSO_URL=http://localhost:3001
NEXT_PUBLIC_SSO_CLIENT_ID=your-client-id
```

## Core Patterns

### 1. PKCE Authentication Client

```typescript
// lib/auth-client.ts
const SSO_URL = process.env.NEXT_PUBLIC_SSO_URL!;
const CLIENT_ID = process.env.NEXT_PUBLIC_SSO_CLIENT_ID!;

// Base64URL encoding helper
function base64UrlEncode(buffer: Uint8Array): string {
  const base64 = btoa(String.fromCharCode(...buffer));
  return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

// Generate cryptographically secure code verifier
export function generateCodeVerifier(): string {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64UrlEncode(array);
}

// Generate SHA-256 code challenge
export async function generateCodeChallenge(verifier: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return base64UrlEncode(new Uint8Array(hash));
}

// Build OAuth authorization URL with PKCE
export async function getOAuthAuthorizationUrl(
  callbackUrl?: string
): Promise<string> {
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = await generateCodeChallenge(codeVerifier);
  const state = generateCodeVerifier(); // Random state

  // Store for token exchange
  sessionStorage.setItem('pkce_code_verifier', codeVerifier);
  sessionStorage.setItem('oauth_state', state);
  if (callbackUrl) {
    sessionStorage.setItem('oauth_callback_url', callbackUrl);
  }

  const params = new URLSearchParams({
    client_id: CLIENT_ID,
    redirect_uri: `${window.location.origin}/api/auth/callback`,
    response_type: 'code',
    scope: 'openid profile email',
    state,
    code_challenge: codeChallenge,
    code_challenge_method: 'S256',
  });

  return `${SSO_URL}/api/auth/oauth2/authorize?${params}`;
}

// Get stored PKCE verifier
export function getStoredCodeVerifier(): string | null {
  return sessionStorage.getItem('pkce_code_verifier');
}

// Clear PKCE storage
export function clearPKCEStorage(): void {
  sessionStorage.removeItem('pkce_code_verifier');
  sessionStorage.removeItem('oauth_state');
  sessionStorage.removeItem('oauth_callback_url');
}
```

### 2. OAuth Callback Route

```typescript
// app/api/auth/callback/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const SSO_URL = process.env.NEXT_PUBLIC_SSO_URL!;
const CLIENT_ID = process.env.NEXT_PUBLIC_SSO_CLIENT_ID!;

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const code = searchParams.get('code');
  const state = searchParams.get('state');
  const error = searchParams.get('error');

  if (error) {
    return NextResponse.redirect(new URL(`/login?error=${error}`, request.url));
  }

  if (!code) {
    return NextResponse.redirect(new URL('/login?error=no_code', request.url));
  }

  // Get code verifier from cookie (set by client before redirect)
  const cookieStore = await cookies();
  const codeVerifier = cookieStore.get('pkce_code_verifier')?.value;

  if (!codeVerifier) {
    return NextResponse.redirect(
      new URL('/login?error=no_verifier', request.url)
    );
  }

  try {
    // Exchange code for tokens (PKCE - no client secret!)
    const tokenResponse = await fetch(`${SSO_URL}/api/auth/oauth2/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        redirect_uri: `${new URL(request.url).origin}/api/auth/callback`,
        client_id: CLIENT_ID,
        code_verifier: codeVerifier,
      }),
    });

    if (!tokenResponse.ok) {
      const error = await tokenResponse.text();
      console.error('Token exchange failed:', error);
      return NextResponse.redirect(
        new URL('/login?error=token_exchange', request.url)
      );
    }

    const tokens = await tokenResponse.json();

    // Create response with redirect
    const callbackUrl = cookieStore.get('oauth_callback_url')?.value || '/dashboard';
    const response = NextResponse.redirect(new URL(callbackUrl, request.url));

    // Set httpOnly cookies for tokens
    const cookieOptions = {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax' as const,
      path: '/',
    };

    response.cookies.set('access_token', tokens.access_token, {
      ...cookieOptions,
      maxAge: 60 * 60 * 6, // 6 hours
    });

    response.cookies.set('refresh_token', tokens.refresh_token, {
      ...cookieOptions,
      maxAge: 60 * 60 * 24 * 7, // 7 days
    });

    response.cookies.set('id_token', tokens.id_token, {
      ...cookieOptions,
      maxAge: 60 * 60 * 6, // 6 hours
    });

    // Clear PKCE cookies
    response.cookies.delete('pkce_code_verifier');
    response.cookies.delete('oauth_state');
    response.cookies.delete('oauth_callback_url');

    return response;
  } catch (error) {
    console.error('Callback error:', error);
    return NextResponse.redirect(
      new URL('/login?error=callback_failed', request.url)
    );
  }
}
```

### 3. Session Route

```typescript
// app/api/auth/session/route.ts
import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { jwtVerify, createRemoteJWKSet } from 'jose';

const SSO_URL = process.env.NEXT_PUBLIC_SSO_URL!;
const JWKS = createRemoteJWKSet(new URL(`${SSO_URL}/api/auth/jwks`));

export async function GET() {
  const cookieStore = await cookies();
  const idToken = cookieStore.get('id_token')?.value;

  if (!idToken) {
    return NextResponse.json({ user: null });
  }

  try {
    const { payload } = await jwtVerify(idToken, JWKS, {
      algorithms: ['RS256'],
    });

    return NextResponse.json({
      user: {
        id: payload.sub,
        email: payload.email,
        name: payload.name,
        role: payload.role || 'user',
        emailVerified: payload.email_verified,
      },
      expires: new Date((payload.exp as number) * 1000).toISOString(),
    });
  } catch (error) {
    // Token invalid or expired
    return NextResponse.json({ user: null });
  }
}
```

### 4. Auth Context Provider

```typescript
// contexts/AuthContext.tsx
'use client';

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { getOAuthAuthorizationUrl, clearPKCEStorage } from '@/lib/auth-client';

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  emailVerified: boolean;
}

interface Session {
  user: User | null;
  expires?: string;
}

interface AuthContextValue {
  session: Session | null;
  status: 'loading' | 'authenticated' | 'unauthenticated';
  signIn: (options?: { callbackUrl?: string }) => Promise<void>;
  signOut: (options?: { redirect?: boolean }) => Promise<void>;
  update: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);
  const [status, setStatus] = useState<'loading' | 'authenticated' | 'unauthenticated'>('loading');

  const fetchSession = useCallback(async () => {
    try {
      const response = await fetch('/api/auth/session');
      const data = await response.json();

      if (data.user) {
        setSession(data);
        setStatus('authenticated');
      } else {
        setSession(null);
        setStatus('unauthenticated');
      }
    } catch (error) {
      console.error('Failed to fetch session:', error);
      setSession(null);
      setStatus('unauthenticated');
    }
  }, []);

  useEffect(() => {
    fetchSession();
  }, [fetchSession]);

  const signIn = async (options?: { callbackUrl?: string }) => {
    const callbackUrl = options?.callbackUrl || window.location.pathname;

    // Store callback URL in cookie for server-side access
    document.cookie = `oauth_callback_url=${encodeURIComponent(callbackUrl)}; path=/; max-age=300`;

    const authUrl = await getOAuthAuthorizationUrl(callbackUrl);

    // Store code verifier in cookie for server-side access
    const codeVerifier = sessionStorage.getItem('pkce_code_verifier');
    if (codeVerifier) {
      document.cookie = `pkce_code_verifier=${codeVerifier}; path=/; max-age=300`;
    }

    window.location.href = authUrl;
  };

  const signOut = async (options?: { redirect?: boolean }) => {
    const { redirect = true } = options || {};

    try {
      const response = await fetch('/api/auth/signout', {
        method: 'POST',
        credentials: 'include',
      });

      const data = await response.json();
      clearPKCEStorage();

      if (redirect && data.redirectUrl) {
        window.location.href = data.redirectUrl;
      } else {
        setSession(null);
        setStatus('unauthenticated');
      }
    } catch (error) {
      console.error('Sign out error:', error);
      if (redirect) {
        window.location.href = '/';
      }
    }
  };

  return (
    <AuthContext.Provider value={{ session, status, signIn, signOut, update: fetchSession }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useSession() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useSession must be used within AuthProvider');
  }
  return {
    data: context.session,
    status: context.status,
    update: context.update,
  };
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### 5. Global Logout

```typescript
// app/api/auth/signout/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const SSO_URL = process.env.NEXT_PUBLIC_SSO_URL;

export async function POST(request: NextRequest) {
  const cookieStore = await cookies();
  const idToken = cookieStore.get('id_token')?.value;

  // Build SSO logout URL
  const appUrl = new URL(request.url).origin;
  const postLogoutRedirectUri = `${appUrl}/logged-out`;

  let redirectUrl = '/logged-out';

  if (SSO_URL) {
    const endsessionUrl = new URL('/api/auth/oauth2/endsession', SSO_URL);
    endsessionUrl.searchParams.set('post_logout_redirect_uri', postLogoutRedirectUri);
    if (idToken) {
      endsessionUrl.searchParams.set('id_token_hint', idToken);
    }
    redirectUrl = endsessionUrl.toString();
  }

  const response = NextResponse.json({ success: true, redirectUrl });

  // Clear all auth cookies
  response.cookies.delete('access_token');
  response.cookies.delete('refresh_token');
  response.cookies.delete('id_token');

  return response;
}
```

### 6. Proxy Protection (Next.js 16)

```typescript
// proxy.ts (Next.js 16 - replaces middleware.ts)
import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify, createRemoteJWKSet } from 'jose';

const SSO_URL = process.env.NEXT_PUBLIC_SSO_URL!;
const JWKS = createRemoteJWKSet(new URL(`${SSO_URL}/api/auth/jwks`));

const publicPaths = ['/', '/login', '/register', '/api/auth', '/logged-out'];

async function isTokenValid(token: string): Promise<boolean> {
  try {
    await jwtVerify(token, JWKS, { algorithms: ['RS256'] });
    return true;
  } catch {
    return false;
  }
}

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow public paths
  if (publicPaths.some(p => pathname === p || pathname.startsWith(`${p}/`))) {
    return NextResponse.next();
  }

  // Allow static assets
  if (pathname.startsWith('/_next') || pathname.includes('.')) {
    return NextResponse.next();
  }

  // Check for valid token
  const idToken = request.cookies.get('id_token')?.value;
  const refreshToken = request.cookies.get('refresh_token')?.value;

  if (!idToken) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  const isValid = await isTokenValid(idToken);

  if (!isValid && refreshToken) {
    // Redirect to refresh endpoint
    const refreshUrl = new URL('/api/auth/refresh', request.url);
    refreshUrl.searchParams.set('returnTo', pathname);
    return NextResponse.redirect(refreshUrl);
  }

  if (!isValid) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

### 7. Token Refresh

```typescript
// app/api/auth/refresh/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const SSO_URL = process.env.NEXT_PUBLIC_SSO_URL!;
const CLIENT_ID = process.env.NEXT_PUBLIC_SSO_CLIENT_ID!;

export async function GET(request: NextRequest) {
  const returnTo = request.nextUrl.searchParams.get('returnTo') || '/dashboard';
  const cookieStore = await cookies();
  const refreshToken = cookieStore.get('refresh_token')?.value;

  if (!refreshToken) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  try {
    const tokenResponse = await fetch(`${SSO_URL}/api/auth/oauth2/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: refreshToken,
        client_id: CLIENT_ID,
      }),
    });

    if (!tokenResponse.ok) {
      return NextResponse.redirect(new URL('/login', request.url));
    }

    const tokens = await tokenResponse.json();
    const response = NextResponse.redirect(new URL(returnTo, request.url));

    const cookieOptions = {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax' as const,
      path: '/',
    };

    response.cookies.set('access_token', tokens.access_token, {
      ...cookieOptions,
      maxAge: 60 * 60 * 6,
    });

    if (tokens.id_token) {
      response.cookies.set('id_token', tokens.id_token, {
        ...cookieOptions,
        maxAge: 60 * 60 * 6,
      });
    }

    if (tokens.refresh_token) {
      response.cookies.set('refresh_token', tokens.refresh_token, {
        ...cookieOptions,
        maxAge: 60 * 60 * 24 * 7,
      });
    }

    return response;
  } catch (error) {
    console.error('Token refresh failed:', error);
    return NextResponse.redirect(new URL('/login', request.url));
  }
}

export async function POST() {
  const cookieStore = await cookies();
  const refreshToken = cookieStore.get('refresh_token')?.value;

  if (!refreshToken) {
    return NextResponse.json({ error: 'No refresh token' }, { status: 401 });
  }

  try {
    const tokenResponse = await fetch(`${SSO_URL}/api/auth/oauth2/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: refreshToken,
        client_id: CLIENT_ID,
      }),
    });

    if (!tokenResponse.ok) {
      return NextResponse.json({ error: 'Refresh failed' }, { status: 401 });
    }

    const tokens = await tokenResponse.json();
    const response = NextResponse.json({ success: true });

    // Update cookies with new tokens
    // ... same cookie setting logic

    return response;
  } catch (error) {
    return NextResponse.json({ error: 'Refresh error' }, { status: 500 });
  }
}
```

## Environment Variables

```env
# Public (exposed to client)
NEXT_PUBLIC_SSO_URL=http://localhost:3001
NEXT_PUBLIC_SSO_CLIENT_ID=your-client-id

# Private (server-side only)
SSO_JWKS_URL=http://localhost:3001/api/auth/jwks
```

## Security Checklist

- [ ] PKCE uses `crypto.getRandomValues()` for code verifier
- [ ] State parameter is random and verified
- [ ] Cookies are httpOnly, Secure (prod), SameSite=Lax
- [ ] No tokens in localStorage
- [ ] No tokens exposed in API responses
- [ ] Token refresh is server-side only
- [ ] Global logout clears SSO session
- [ ] Error messages don't leak secrets

## Common Pitfalls

### 1. "code verification failed" Error

**Cause**: PKCE code_verifier lost during sign-in redirect
**Fix**: Store in cookie before redirect, not just sessionStorage

### 2. Auto-Login After Logout

**Cause**: Only cleared local tokens, not SSO session
**Fix**: Redirect to SSO `/endsession` endpoint

### 3. Token Not Refreshing

**Cause**: Refresh happening client-side (blocked by httpOnly)
**Fix**: Use server-side API route for refresh

## References

For backend integration, see:
- `fastapi-backend/references/jwt-verification.md`
- `fastapi-backend/references/better-auth-sso-integration.md`

Better Auth docs: https://www.better-auth.com/docs
