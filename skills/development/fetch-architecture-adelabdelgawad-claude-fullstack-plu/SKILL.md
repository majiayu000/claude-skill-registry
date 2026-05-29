# Fetch Architecture Skill

Client and server-side fetch utilities for Next.js applications with API route proxying to FastAPI backends.

## When to Use This Skill

Use this skill when asked to:
- Set up fetch utilities for Next.js
- Configure client-side API calls with auth refresh
- Implement server-side data fetching
- Create API route proxies to backend services
- Handle authentication tokens across layers

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Client)                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Client Components                                   │    │
│  │  • fetchClient.get/post/put/delete                  │    │
│  │  • SWR hooks with fetcher                           │    │
│  └──────────────────────────┬──────────────────────────┘    │
└─────────────────────────────┼───────────────────────────────┘
                              │ HTTP (cookies)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Next.js Server                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  API Routes (app/api/...)                           │    │
│  │  • withAuth() wrapper                               │    │
│  │  • backendGet/Post/Put/Delete helpers               │    │
│  └──────────────────────────┬──────────────────────────┘    │
│                             │                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Server Actions                                     │    │
│  │  • serverGet/Post/Put/Delete                        │    │
│  │  • Forwards cookies to API routes                   │    │
│  └──────────────────────────┬──────────────────────────┘    │
│                             │                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Server Components (pages)                          │    │
│  │  • auth() session check                             │    │
│  │  • Call server actions for SSR data                 │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────┼───────────────────────────────┘
                              │ HTTP (Bearer token)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  /api/v1/...                                                │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
lib/
├── fetch/
│   ├── index.ts              # Exports
│   ├── client.ts             # Client-side fetch (browser)
│   ├── server.ts             # Server-side fetch (actions, routes)
│   ├── api-route-helper.ts   # API route wrappers
│   ├── errors.ts             # Error classes
│   └── types.ts              # TypeScript types
└── auth/
    ├── server-auth.ts        # Server authentication
    └── auth-service.ts       # Client auth (token refresh)
```

## Core Files

### 1. Error Classes

```typescript
// lib/fetch/errors.ts
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export function extractErrorMessage(data: unknown): string {
  if (typeof data === 'string') return data;
  if (typeof data === 'object' && data !== null) {
    const obj = data as Record<string, unknown>;
    if (typeof obj.detail === 'string') return obj.detail;
    if (typeof obj.message === 'string') return obj.message;
    if (typeof obj.error === 'string') return obj.error;
  }
  return 'An error occurred';
}
```

### 2. Type Definitions

```typescript
// lib/fetch/types.ts
export interface FetchOptions {
  headers?: Record<string, string>;
  timeout?: number;
}

export interface FetchRequestOptions extends FetchOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: unknown;
}
```

### 3. Client Fetch (Browser)

```typescript
// lib/fetch/client.ts
"use client";

import { AuthService } from '@/lib/auth/auth-service';
import { ApiError, extractErrorMessage } from './errors';
import type { FetchOptions, FetchRequestOptions } from './types';

const DEFAULT_TIMEOUT = 30000;
const MAX_RETRIES = 2;

async function clientFetch<T>(
  url: string,
  options: FetchRequestOptions = {},
  attempt = 1,
  isRetryAfterRefresh = false
): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(
    () => controller.abort(),
    options.timeout || DEFAULT_TIMEOUT
  );

  try {
    const response = await fetch(url, {
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      body: options.body ? JSON.stringify(options.body) : undefined,
      signal: controller.signal,
      credentials: 'include',  // Include cookies
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      // Handle 401 - try token refresh
      if (response.status === 401 && !isRetryAfterRefresh) {
        clearTimeout(timeoutId);
        const newToken = await AuthService.refreshAccessToken();
        if (newToken) {
          return clientFetch<T>(url, options, attempt, true);
        }
        window.location.href = '/login';
        throw new ApiError('Session expired', 401);
      }

      // Retry on 429/503
      if ((response.status === 429 || response.status === 503) && attempt < MAX_RETRIES) {
        clearTimeout(timeoutId);
        await new Promise(r => setTimeout(r, 1000 * attempt));
        return clientFetch<T>(url, options, attempt + 1);
      }

      throw new ApiError(extractErrorMessage(data), response.status, data);
    }

    return data as T;
  } finally {
    clearTimeout(timeoutId);
  }
}

// Legacy wrapper (returns { data: T })
export const fetchClient = {
  get: async <T>(url: string, opts?: FetchOptions) => {
    const data = await clientFetch<T>(url, { ...opts, method: 'GET' });
    return { data };
  },
  post: async <T>(url: string, body?: unknown, opts?: FetchOptions) => {
    const data = await clientFetch<T>(url, { ...opts, method: 'POST', body });
    return { data };
  },
  put: async <T>(url: string, body?: unknown, opts?: FetchOptions) => {
    const data = await clientFetch<T>(url, { ...opts, method: 'PUT', body });
    return { data };
  },
  delete: async <T>(url: string, opts?: FetchOptions) => {
    const data = await clientFetch<T>(url, { ...opts, method: 'DELETE' });
    return { data };
  },
};
```

### 4. Server Fetch (Actions & Routes)

```typescript
// lib/fetch/server.ts
"use server";

import { cookies, headers } from 'next/headers';
import { ApiError, extractErrorMessage } from './errors';
import type { FetchRequestOptions } from './types';

// Server → Next.js API routes
export async function serverFetch<T>(
  url: string,
  options: FetchRequestOptions = {}
): Promise<T> {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';
  const cookieStore = await cookies();
  const cookieHeader = cookieStore.getAll().map(c => `${c.name}=${c.value}`).join('; ');

  const response = await fetch(`${baseUrl}${url}`, {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(cookieHeader && { Cookie: cookieHeader }),
      ...options.headers,
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new ApiError(extractErrorMessage(data), response.status, data);
  }
  return data as T;
}

// API routes → FastAPI backend
export async function backendFetch<T>(
  url: string,
  token: string,
  options: FetchRequestOptions = {}
): Promise<T> {
  const baseUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000';

  const response = await fetch(`${baseUrl}${url}`, {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new ApiError(extractErrorMessage(data), response.status, data);
  }
  return data as T;
}

// Convenience methods
export const serverGet = <T>(url: string) => serverFetch<T>(url, { method: 'GET' });
export const serverPost = <T>(url: string, body: unknown) => serverFetch<T>(url, { method: 'POST', body });
export const serverPut = <T>(url: string, body: unknown) => serverFetch<T>(url, { method: 'PUT', body });
export const serverDelete = <T>(url: string) => serverFetch<T>(url, { method: 'DELETE' });
```

### 5. API Route Helper

```typescript
// lib/fetch/api-route-helper.ts
import { NextResponse } from 'next/server';
import { auth } from '@/lib/auth/server-auth';
import { backendFetch } from './server';
import { ApiError } from './errors';

export async function withAuth<T>(
  handler: (token: string) => Promise<T>
): Promise<NextResponse> {
  try {
    const session = await auth();
    if (!session?.accessToken) {
      return NextResponse.json({ detail: 'Unauthorized' }, { status: 401 });
    }
    const data = await handler(session.accessToken);
    return NextResponse.json(data);
  } catch (error) {
    if (error instanceof ApiError) {
      return NextResponse.json({ detail: error.message }, { status: error.status });
    }
    return NextResponse.json({ detail: 'Internal server error' }, { status: 500 });
  }
}

export const backendGet = <T>(url: string, token: string) =>
  backendFetch<T>(url, token, { method: 'GET' });
export const backendPost = <T>(url: string, token: string, body: unknown) =>
  backendFetch<T>(url, token, { method: 'POST', body });
export const backendPut = <T>(url: string, token: string, body: unknown) =>
  backendFetch<T>(url, token, { method: 'PUT', body });
export const backendDelete = <T>(url: string, token: string) =>
  backendFetch<T>(url, token, { method: 'DELETE' });
```

## Request Flow

### Client-Side (Mutations)
```
Component → fetchClient → API Route → withAuth → backendFetch → FastAPI
```

### Server-Side (SSR)
```
Page → Server Action → serverFetch → API Route → withAuth → backendFetch → FastAPI
```

### SWR (Data Fetching)
```
useSWR(url, fetcher) → fetchClient.get → API Route → withAuth → backendFetch → FastAPI
```

## Key Patterns

1. **Client includes cookies** - `credentials: 'include'`
2. **Server forwards cookies** - Cookie header to API routes
3. **API routes use Bearer token** - Extract from session
4. **Auto token refresh** - On 401, try refresh once
5. **Consistent error format** - ApiError class
6. **Retry on rate limit** - 429/503 with backoff
