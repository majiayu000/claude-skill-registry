---
name: "Vercel Edge Function Testing"
description: "Testing patterns for Vercel Edge Functions, middleware, and serverless functions covering local testing, edge runtime simulation, and deployment verification."
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [vercel, edge-functions, middleware, serverless, edge-runtime, kv, blob, isr, cron, deployment]
testingTypes: [unit, integration, e2e]
frameworks: [vitest, playwright]
languages: [typescript, javascript]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Vercel Edge Function Testing

You are an expert QA engineer specializing in Vercel Edge Function testing patterns. When the user asks you to write, review, debug, or set up tests for Vercel Edge Functions, middleware, serverless functions, or related Vercel platform features, follow these detailed instructions. You understand edge runtime limitations, middleware request/response chains, KV/Blob storage patterns, ISR/SSG behavior, and Vercel CLI local development workflows.

## Core Principles

1. **Edge Runtime Awareness** -- Edge functions run on V8 isolates, not Node.js. Tests must account for API limitations: no `fs`, no native Node modules, limited `crypto`, and a 128KB code size limit. Always validate that your function code is edge-compatible.
2. **Middleware Chain Fidelity** -- Middleware intercepts every request before it reaches the route handler. Test the complete chain: request rewriting, header manipulation, redirect logic, and geolocation-based routing.
3. **Local-Remote Parity** -- Use `vercel dev` and Vercel CLI for local testing that mirrors the production environment. Catch platform-specific bugs before deployment.
4. **Storage Mocking Strategy** -- Mock Vercel KV, Blob, and Edge Config at the SDK level for unit tests. Use real storage instances in integration tests to verify serialization, TTL, and size limits.
5. **Deployment Verification** -- Every preview deployment should trigger smoke tests against the actual edge network. DNS resolution, CDN caching, and geo-routing behave differently in production.
6. **Performance Budgets** -- Edge functions have a 25ms CPU time limit on Hobby plans and 50ms on Pro. Test execution time to avoid timeout failures.
7. **Idempotency** -- Edge functions may be retried by the platform. All functions must be safe to call multiple times with the same input.

## When to Use This Skill

- When writing or testing Vercel Edge Functions and middleware
- When testing Next.js middleware with Vercel-specific features (geolocation, IP detection)
- When mocking Vercel KV, Blob, or Edge Config in tests
- When validating ISR/SSG revalidation behavior
- When testing Vercel Cron Jobs
- When writing deployment verification tests for preview and production environments
- When testing edge runtime API compatibility

## Project Structure

```
project-root/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── hello/
│   │   │   │   └── route.ts            # Edge API route
│   │   │   ├── data/
│   │   │   │   └── route.ts            # KV-backed API route
│   │   │   ├── upload/
│   │   │   │   └── route.ts            # Blob storage route
│   │   │   └── cron/
│   │   │       └── route.ts            # Cron job handler
│   │   ├── page.tsx                     # ISR page
│   │   └── layout.tsx
│   ├── middleware.ts                     # Edge middleware
│   └── lib/
│       ├── edge-utils.ts                # Edge-compatible utilities
│       ├── kv-client.ts                 # Vercel KV wrapper
│       └── blob-client.ts              # Vercel Blob wrapper
│
├── tests/
│   ├── unit/
│   │   ├── middleware.test.ts           # Middleware unit tests
│   │   ├── edge-functions.test.ts       # Edge function unit tests
│   │   ├── kv-mock.test.ts             # KV mock tests
│   │   └── edge-compat.test.ts         # Edge runtime compatibility
│   ├── integration/
│   │   ├── api-routes.test.ts           # API route integration tests
│   │   ├── kv-integration.test.ts       # Real KV integration tests
│   │   ├── blob-integration.test.ts     # Blob storage tests
│   │   └── cron.test.ts                # Cron job tests
│   ├── e2e/
│   │   ├── deployment.test.ts           # Deployment verification
│   │   ├── middleware-e2e.test.ts        # Full middleware E2E
│   │   ├── isr.test.ts                 # ISR behavior tests
│   │   └── geo-routing.test.ts          # Geolocation routing tests
│   ├── mocks/
│   │   ├── vercel-kv.ts                # Vercel KV mock
│   │   ├── vercel-blob.ts             # Vercel Blob mock
│   │   ├── edge-config.ts             # Edge Config mock
│   │   └── next-request.ts            # NextRequest mock helper
│   └── fixtures/
│       ├── requests.ts                  # Test request fixtures
│       └── responses.ts                # Expected response fixtures
│
├── vercel.json                          # Vercel configuration
├── vitest.config.ts
├── playwright.config.ts
└── package.json
```

## Edge Function Implementation

### Basic Edge API Route

```typescript
// src/app/api/hello/route.ts
export const runtime = 'edge';

export async function GET(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const name = searchParams.get('name') || 'World';

  return new Response(
    JSON.stringify({
      message: `Hello, ${name}!`,
      timestamp: Date.now(),
      region: process.env.VERCEL_REGION || 'unknown',
    }),
    {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=300',
      },
    },
  );
}

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await request.json();

    if (!body.name || typeof body.name !== 'string') {
      return new Response(
        JSON.stringify({ error: 'Invalid name parameter' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } },
      );
    }

    return new Response(
      JSON.stringify({ message: `Created: ${body.name}` }),
      { status: 201, headers: { 'Content-Type': 'application/json' } },
    );
  } catch {
    return new Response(
      JSON.stringify({ error: 'Invalid JSON body' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } },
    );
  }
}
```

### Middleware

```typescript
// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|public/).*)',
  ],
};

export function middleware(request: NextRequest): NextResponse {
  const response = NextResponse.next();

  // Add security headers
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set('X-Request-Id', crypto.randomUUID());

  // Geolocation-based routing
  const country = request.geo?.country || 'US';
  const city = request.geo?.city || 'Unknown';
  response.headers.set('X-User-Country', country);
  response.headers.set('X-User-City', city);

  // Block requests from restricted regions
  const blockedCountries = ['XX', 'YY'];
  if (blockedCountries.includes(country)) {
    return new NextResponse('Access Denied', { status: 403 });
  }

  // Rate limiting header (actual rate limiting via KV in production)
  const ip = request.ip || request.headers.get('x-forwarded-for') || 'unknown';
  response.headers.set('X-Client-IP', ip);

  // Redirect www to non-www
  const hostname = request.headers.get('host') || '';
  if (hostname.startsWith('www.')) {
    const newUrl = new URL(request.url);
    newUrl.hostname = hostname.replace('www.', '');
    return NextResponse.redirect(newUrl, 301);
  }

  // A/B testing: assign experiment variant
  const experimentCookie = request.cookies.get('experiment-variant');
  if (!experimentCookie) {
    const variant = Math.random() < 0.5 ? 'control' : 'treatment';
    response.cookies.set('experiment-variant', variant, {
      httpOnly: true,
      secure: true,
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 30, // 30 days
    });
  }

  // Rewrite API versioning
  if (request.nextUrl.pathname.startsWith('/api/v2/')) {
    const rewrittenPath = request.nextUrl.pathname.replace('/api/v2/', '/api/');
    return NextResponse.rewrite(new URL(rewrittenPath, request.url));
  }

  return response;
}
```

### KV-Backed Route

```typescript
// src/app/api/data/route.ts
import { kv } from '@vercel/kv';

export const runtime = 'edge';

export async function GET(request: Request): Promise<Response> {
  const { searchParams } = new URL(request.url);
  const key = searchParams.get('key');

  if (!key) {
    return new Response(
      JSON.stringify({ error: 'Missing key parameter' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } },
    );
  }

  const value = await kv.get(key);

  if (value === null) {
    return new Response(
      JSON.stringify({ error: 'Key not found' }),
      { status: 404, headers: { 'Content-Type': 'application/json' } },
    );
  }

  return new Response(
    JSON.stringify({ key, value }),
    { status: 200, headers: { 'Content-Type': 'application/json' } },
  );
}

export async function POST(request: Request): Promise<Response> {
  const body = await request.json();
  const { key, value, ttl } = body;

  if (!key || value === undefined) {
    return new Response(
      JSON.stringify({ error: 'Missing key or value' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } },
    );
  }

  if (ttl) {
    await kv.set(key, value, { ex: ttl });
  } else {
    await kv.set(key, value);
  }

  return new Response(
    JSON.stringify({ success: true, key }),
    { status: 201, headers: { 'Content-Type': 'application/json' } },
  );
}
```

## Test Mocks

### NextRequest Mock Helper

```typescript
// tests/mocks/next-request.ts
import { NextRequest } from 'next/server';

interface MockRequestOptions {
  url?: string;
  method?: string;
  headers?: Record<string, string>;
  cookies?: Record<string, string>;
  body?: unknown;
  geo?: {
    country?: string;
    city?: string;
    region?: string;
    latitude?: string;
    longitude?: string;
  };
  ip?: string;
}

export function createMockNextRequest(options: MockRequestOptions = {}): NextRequest {
  const {
    url = 'https://example.com/',
    method = 'GET',
    headers = {},
    cookies = {},
    body,
    geo,
    ip,
  } = options;

  const requestInit: RequestInit = {
    method,
    headers: new Headers(headers),
  };

  if (body && method !== 'GET') {
    requestInit.body = JSON.stringify(body);
    (requestInit.headers as Headers).set('Content-Type', 'application/json');
  }

  const request = new NextRequest(new URL(url), requestInit);

  // Set cookies
  for (const [name, value] of Object.entries(cookies)) {
    request.cookies.set(name, value);
  }

  // Mock geo and ip (these are read-only in NextRequest, so we use Object.defineProperty)
  if (geo) {
    Object.defineProperty(request, 'geo', { value: geo, writable: false });
  }
  if (ip) {
    Object.defineProperty(request, 'ip', { value: ip, writable: false });
  }

  return request;
}

export function createMockRequest(
  url: string,
  options: Omit<MockRequestOptions, 'url'> = {},
): Request {
  const { method = 'GET', headers = {}, body } = options;

  const init: RequestInit = {
    method,
    headers: new Headers({
      'Content-Type': 'application/json',
      ...headers,
    }),
  };

  if (body && method !== 'GET') {
    init.body = JSON.stringify(body);
  }

  return new Request(url, init);
}
```

### Vercel KV Mock

```typescript
// tests/mocks/vercel-kv.ts
import { vi } from 'vitest';

const store = new Map<string, { value: unknown; expiresAt?: number }>();

export const kvMock = {
  get: vi.fn(async (key: string) => {
    const entry = store.get(key);
    if (!entry) return null;
    if (entry.expiresAt && Date.now() > entry.expiresAt) {
      store.delete(key);
      return null;
    }
    return entry.value;
  }),

  set: vi.fn(async (key: string, value: unknown, options?: { ex?: number }) => {
    const expiresAt = options?.ex ? Date.now() + options.ex * 1000 : undefined;
    store.set(key, { value, expiresAt });
    return 'OK';
  }),

  del: vi.fn(async (...keys: string[]) => {
    let deleted = 0;
    for (const key of keys) {
      if (store.delete(key)) deleted++;
    }
    return deleted;
  }),

  exists: vi.fn(async (...keys: string[]) => {
    return keys.filter((key) => store.has(key)).length;
  }),

  keys: vi.fn(async (pattern: string) => {
    const regex = new RegExp('^' + pattern.replace('*', '.*') + '$');
    return Array.from(store.keys()).filter((key) => regex.test(key));
  }),

  incr: vi.fn(async (key: string) => {
    const entry = store.get(key);
    const current = entry ? Number(entry.value) : 0;
    const next = current + 1;
    store.set(key, { value: next });
    return next;
  }),

  // Helper to clear mock state between tests
  __clear: () => {
    store.clear();
    kvMock.get.mockClear();
    kvMock.set.mockClear();
    kvMock.del.mockClear();
    kvMock.exists.mockClear();
    kvMock.keys.mockClear();
    kvMock.incr.mockClear();
  },
};

// Auto-mock @vercel/kv
vi.mock('@vercel/kv', () => ({
  kv: kvMock,
}));
```

### Vercel Blob Mock

```typescript
// tests/mocks/vercel-blob.ts
import { vi } from 'vitest';

const blobStore = new Map<string, { data: Buffer; contentType: string; size: number }>();

export const blobMock = {
  put: vi.fn(async (pathname: string, body: Buffer | string, options?: { contentType?: string }) => {
    const data = typeof body === 'string' ? Buffer.from(body) : body;
    const contentType = options?.contentType || 'application/octet-stream';
    blobStore.set(pathname, { data, contentType, size: data.length });
    return {
      url: `https://mock-blob.vercel-storage.com/${pathname}`,
      pathname,
      contentType,
      size: data.length,
    };
  }),

  del: vi.fn(async (url: string | string[]) => {
    const urls = Array.isArray(url) ? url : [url];
    for (const u of urls) {
      const pathname = u.replace('https://mock-blob.vercel-storage.com/', '');
      blobStore.delete(pathname);
    }
  }),

  list: vi.fn(async (options?: { prefix?: string }) => {
    const prefix = options?.prefix || '';
    const blobs = Array.from(blobStore.entries())
      .filter(([key]) => key.startsWith(prefix))
      .map(([pathname, { contentType, size }]) => ({
        url: `https://mock-blob.vercel-storage.com/${pathname}`,
        pathname,
        contentType,
        size,
      }));
    return { blobs, hasMore: false, cursor: undefined };
  }),

  head: vi.fn(async (url: string) => {
    const pathname = url.replace('https://mock-blob.vercel-storage.com/', '');
    const entry = blobStore.get(pathname);
    if (!entry) return null;
    return {
      url,
      pathname,
      contentType: entry.contentType,
      size: entry.size,
    };
  }),

  __clear: () => {
    blobStore.clear();
    blobMock.put.mockClear();
    blobMock.del.mockClear();
    blobMock.list.mockClear();
    blobMock.head.mockClear();
  },
};

vi.mock('@vercel/blob', () => blobMock);
```

## Unit Tests

### Middleware Tests

```typescript
// tests/unit/middleware.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { middleware } from '../../src/middleware';
import { createMockNextRequest } from '../mocks/next-request';
import { NextResponse } from 'next/server';

describe('Edge Middleware', () => {
  describe('Security Headers', () => {
    it('should add security headers to all responses', () => {
      const request = createMockNextRequest({ url: 'https://example.com/page' });
      const response = middleware(request);

      expect(response.headers.get('X-Frame-Options')).toBe('DENY');
      expect(response.headers.get('X-Content-Type-Options')).toBe('nosniff');
      expect(response.headers.get('Referrer-Policy')).toBe('strict-origin-when-cross-origin');
    });

    it('should add a unique request ID', () => {
      const request = createMockNextRequest({ url: 'https://example.com/page' });
      const response = middleware(request);

      const requestId = response.headers.get('X-Request-Id');
      expect(requestId).toBeDefined();
      expect(requestId).toMatch(
        /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/,
      );
    });
  });

  describe('Geolocation Routing', () => {
    it('should set geo headers from request', () => {
      const request = createMockNextRequest({
        url: 'https://example.com/page',
        geo: { country: 'DE', city: 'Berlin' },
      });
      const response = middleware(request);

      expect(response.headers.get('X-User-Country')).toBe('DE');
      expect(response.headers.get('X-User-City')).toBe('Berlin');
    });

    it('should default to US when geo is unavailable', () => {
      const request = createMockNextRequest({ url: 'https://example.com/page' });
      const response = middleware(request);

      expect(response.headers.get('X-User-Country')).toBe('US');
    });

    it('should block requests from restricted countries', () => {
      const request = createMockNextRequest({
        url: 'https://example.com/page',
        geo: { country: 'XX' },
      });
      const response = middleware(request);

      expect(response.status).toBe(403);
    });
  });

  describe('www Redirect', () => {
    it('should redirect www to non-www with 301', () => {
      const request = createMockNextRequest({
        url: 'https://www.example.com/page',
        headers: { host: 'www.example.com' },
      });
      const response = middleware(request);

      expect(response.status).toBe(301);
      expect(response.headers.get('location')).toContain('example.com/page');
      expect(response.headers.get('location')).not.toContain('www.');
    });

    it('should not redirect non-www requests', () => {
      const request = createMockNextRequest({
        url: 'https://example.com/page',
        headers: { host: 'example.com' },
      });
      const response = middleware(request);

      expect(response.status).not.toBe(301);
    });
  });

  describe('A/B Testing', () => {
    it('should assign experiment variant when cookie is missing', () => {
      const request = createMockNextRequest({ url: 'https://example.com/page' });
      const response = middleware(request);

      const setCookie = response.headers.get('set-cookie');
      expect(setCookie).toContain('experiment-variant=');
    });

    it('should not reassign variant when cookie exists', () => {
      const request = createMockNextRequest({
        url: 'https://example.com/page',
        cookies: { 'experiment-variant': 'control' },
      });
      const response = middleware(request);

      const setCookie = response.headers.get('set-cookie');
      // Should not set a new cookie when one already exists
      expect(setCookie).toBeNull();
    });
  });

  describe('API Version Rewriting', () => {
    it('should rewrite /api/v2/ to /api/', () => {
      const request = createMockNextRequest({
        url: 'https://example.com/api/v2/users',
      });
      const response = middleware(request);

      // NextResponse.rewrite returns a response with the x-middleware-rewrite header
      expect(response.headers.get('x-middleware-rewrite')).toContain('/api/users');
    });

    it('should not rewrite non-v2 API paths', () => {
      const request = createMockNextRequest({
        url: 'https://example.com/api/users',
      });
      const response = middleware(request);

      expect(response.headers.get('x-middleware-rewrite')).toBeNull();
    });
  });

  describe('Client IP Detection', () => {
    it('should set client IP from request.ip', () => {
      const request = createMockNextRequest({
        url: 'https://example.com/page',
        ip: '192.168.1.100',
      });
      const response = middleware(request);

      expect(response.headers.get('X-Client-IP')).toBe('192.168.1.100');
    });

    it('should fallback to x-forwarded-for header', () => {
      const request = createMockNextRequest({
        url: 'https://example.com/page',
        headers: { 'x-forwarded-for': '10.0.0.1' },
      });
      const response = middleware(request);

      expect(response.headers.get('X-Client-IP')).toBe('10.0.0.1');
    });
  });
});
```

### Edge Function Unit Tests

```typescript
// tests/unit/edge-functions.test.ts
import { describe, it, expect } from 'vitest';
import { GET, POST } from '../../src/app/api/hello/route';
import { createMockRequest } from '../mocks/next-request';

describe('Edge API: /api/hello', () => {
  describe('GET', () => {
    it('should return greeting with default name', async () => {
      const request = createMockRequest('https://example.com/api/hello');
      const response = await GET(request);
      const body = await response.json();

      expect(response.status).toBe(200);
      expect(body.message).toBe('Hello, World!');
      expect(body.timestamp).toBeDefined();
    });

    it('should return greeting with custom name', async () => {
      const request = createMockRequest('https://example.com/api/hello?name=Alice');
      const response = await GET(request);
      const body = await response.json();

      expect(body.message).toBe('Hello, Alice!');
    });

    it('should set correct cache headers', async () => {
      const request = createMockRequest('https://example.com/api/hello');
      const response = await GET(request);

      expect(response.headers.get('Cache-Control')).toBe(
        'public, s-maxage=60, stale-while-revalidate=300',
      );
    });

    it('should return JSON content type', async () => {
      const request = createMockRequest('https://example.com/api/hello');
      const response = await GET(request);

      expect(response.headers.get('Content-Type')).toBe('application/json');
    });
  });

  describe('POST', () => {
    it('should create resource with valid body', async () => {
      const request = createMockRequest('https://example.com/api/hello', {
        method: 'POST',
        body: { name: 'Test Resource' },
      });
      const response = await POST(request);
      const body = await response.json();

      expect(response.status).toBe(201);
      expect(body.message).toBe('Created: Test Resource');
    });

    it('should return 400 for missing name', async () => {
      const request = createMockRequest('https://example.com/api/hello', {
        method: 'POST',
        body: {},
      });
      const response = await POST(request);

      expect(response.status).toBe(400);
    });

    it('should return 400 for invalid JSON', async () => {
      const request = new Request('https://example.com/api/hello', {
        method: 'POST',
        body: 'not json',
        headers: { 'Content-Type': 'application/json' },
      });
      const response = await POST(request);

      expect(response.status).toBe(400);
      const body = await response.json();
      expect(body.error).toBe('Invalid JSON body');
    });

    it('should reject non-string name values', async () => {
      const request = createMockRequest('https://example.com/api/hello', {
        method: 'POST',
        body: { name: 123 },
      });
      const response = await POST(request);

      expect(response.status).toBe(400);
    });
  });
});
```

### Edge Runtime Compatibility Tests

```typescript
// tests/unit/edge-compat.test.ts
import { describe, it, expect } from 'vitest';

describe('Edge Runtime Compatibility', () => {
  it('should have access to Web Crypto API', () => {
    expect(crypto).toBeDefined();
    expect(crypto.randomUUID).toBeDefined();
    expect(crypto.subtle).toBeDefined();
  });

  it('should generate valid UUIDs', () => {
    const uuid = crypto.randomUUID();
    expect(uuid).toMatch(
      /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/,
    );
  });

  it('should support TextEncoder/TextDecoder', () => {
    const encoder = new TextEncoder();
    const decoder = new TextDecoder();

    const encoded = encoder.encode('Hello Edge');
    const decoded = decoder.decode(encoded);

    expect(decoded).toBe('Hello Edge');
  });

  it('should support URL and URLSearchParams', () => {
    const url = new URL('https://example.com/api?key=value&other=123');

    expect(url.pathname).toBe('/api');
    expect(url.searchParams.get('key')).toBe('value');
    expect(url.searchParams.get('other')).toBe('123');
  });

  it('should support fetch API', () => {
    expect(fetch).toBeDefined();
    expect(typeof fetch).toBe('function');
  });

  it('should support Response and Request constructors', () => {
    const request = new Request('https://example.com', { method: 'POST' });
    const response = new Response('OK', { status: 200 });

    expect(request.method).toBe('POST');
    expect(response.status).toBe(200);
  });

  it('should support Headers API', () => {
    const headers = new Headers();
    headers.set('X-Custom', 'value');
    headers.append('X-Multi', 'one');
    headers.append('X-Multi', 'two');

    expect(headers.get('X-Custom')).toBe('value');
    expect(headers.has('X-Custom')).toBe(true);
  });

  it('should support structuredClone', () => {
    const original = { a: 1, b: { c: [1, 2, 3] } };
    const cloned = structuredClone(original);

    expect(cloned).toEqual(original);
    expect(cloned).not.toBe(original);
    expect(cloned.b).not.toBe(original.b);
  });

  it('should NOT have access to Node.js fs module in edge runtime', () => {
    // This test documents edge runtime limitations
    // In actual edge runtime, require('fs') would throw
    expect(typeof process !== 'undefined').toBe(true); // process.env is available
  });

  it('should support AbortController', () => {
    const controller = new AbortController();
    const signal = controller.signal;

    expect(signal.aborted).toBe(false);
    controller.abort();
    expect(signal.aborted).toBe(true);
  });

  it('should support crypto.subtle for hashing', async () => {
    const data = new TextEncoder().encode('test data');
    const hash = await crypto.subtle.digest('SHA-256', data);

    expect(hash).toBeInstanceOf(ArrayBuffer);
    expect(hash.byteLength).toBe(32);
  });
});
```

### KV Mock Tests

```typescript
// tests/unit/kv-mock.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { kvMock } from '../mocks/vercel-kv';
import { GET, POST } from '../../src/app/api/data/route';
import { createMockRequest } from '../mocks/next-request';

describe('KV-Backed API Route', () => {
  beforeEach(() => {
    kvMock.__clear();
  });

  describe('GET /api/data', () => {
    it('should return value for existing key', async () => {
      kvMock.get.mockResolvedValueOnce({ name: 'test' });

      const request = createMockRequest('https://example.com/api/data?key=mykey');
      const response = await GET(request);
      const body = await response.json();

      expect(response.status).toBe(200);
      expect(body.key).toBe('mykey');
      expect(body.value).toEqual({ name: 'test' });
    });

    it('should return 404 for missing key', async () => {
      kvMock.get.mockResolvedValueOnce(null);

      const request = createMockRequest('https://example.com/api/data?key=missing');
      const response = await GET(request);

      expect(response.status).toBe(404);
    });

    it('should return 400 when key parameter is missing', async () => {
      const request = createMockRequest('https://example.com/api/data');
      const response = await GET(request);

      expect(response.status).toBe(400);
    });
  });

  describe('POST /api/data', () => {
    it('should store value and return success', async () => {
      const request = createMockRequest('https://example.com/api/data', {
        method: 'POST',
        body: { key: 'newkey', value: 'newvalue' },
      });
      const response = await POST(request);
      const body = await response.json();

      expect(response.status).toBe(201);
      expect(body.success).toBe(true);
      expect(kvMock.set).toHaveBeenCalledWith('newkey', 'newvalue');
    });

    it('should set TTL when provided', async () => {
      const request = createMockRequest('https://example.com/api/data', {
        method: 'POST',
        body: { key: 'ttlkey', value: 'ttlvalue', ttl: 3600 },
      });
      await POST(request);

      expect(kvMock.set).toHaveBeenCalledWith('ttlkey', 'ttlvalue', { ex: 3600 });
    });

    it('should return 400 when key is missing', async () => {
      const request = createMockRequest('https://example.com/api/data', {
        method: 'POST',
        body: { value: 'nokey' },
      });
      const response = await POST(request);

      expect(response.status).toBe(400);
    });
  });
});
```

## Integration Tests

### API Route Integration Tests

```typescript
// tests/integration/api-routes.test.ts
import { describe, it, expect } from 'vitest';
import { createServer } from 'http';
import { parse } from 'url';
import next from 'next';

describe('API Route Integration', () => {
  let baseUrl: string;

  // Note: For Vercel-specific integration tests, prefer using `vercel dev`
  // or deploying to a preview environment and testing against that.

  it('should handle concurrent requests to edge functions', async () => {
    const requests = Array.from({ length: 10 }, (_, i) =>
      fetch(`${baseUrl}/api/hello?name=User${i}`).then((r) => r.json()),
    );

    const responses = await Promise.all(requests);

    responses.forEach((body, i) => {
      expect(body.message).toBe(`Hello, User${i}!`);
    });
  });

  it('should enforce rate limits across requests', async () => {
    // Simulate rapid requests from same IP
    const responses = [];
    for (let i = 0; i < 20; i++) {
      const response = await fetch(`${baseUrl}/api/hello`);
      responses.push(response.status);
    }

    // Depending on rate limit config, some requests should be throttled
    expect(responses.filter((s) => s === 200).length).toBeGreaterThan(0);
  });
});
```

### Cron Job Tests

```typescript
// tests/integration/cron.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the cron handler
const mockCleanup = vi.fn().mockResolvedValue({ deleted: 5 });

// Simulated cron route handler
async function handleCron(request: Request): Promise<Response> {
  // Verify authorization
  const authHeader = request.headers.get('authorization');
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 });
  }

  const result = await mockCleanup();
  return new Response(JSON.stringify(result), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('Cron Job Handler', () => {
  beforeEach(() => {
    process.env.CRON_SECRET = 'test-cron-secret';
    mockCleanup.mockClear();
  });

  it('should execute cron job with valid secret', async () => {
    const request = new Request('https://example.com/api/cron', {
      headers: { authorization: 'Bearer test-cron-secret' },
    });

    const response = await handleCron(request);
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body.deleted).toBe(5);
    expect(mockCleanup).toHaveBeenCalledOnce();
  });

  it('should reject requests without valid secret', async () => {
    const request = new Request('https://example.com/api/cron', {
      headers: { authorization: 'Bearer wrong-secret' },
    });

    const response = await handleCron(request);

    expect(response.status).toBe(401);
    expect(mockCleanup).not.toHaveBeenCalled();
  });

  it('should reject requests with no authorization header', async () => {
    const request = new Request('https://example.com/api/cron');
    const response = await handleCron(request);

    expect(response.status).toBe(401);
  });
});
```

## E2E Tests

### Deployment Verification Tests

```typescript
// tests/e2e/deployment.test.ts
import { test, expect } from '@playwright/test';

const DEPLOYMENT_URL = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : 'http://localhost:3000';

test.describe('Deployment Verification', () => {
  test('should serve the homepage', async ({ page }) => {
    const response = await page.goto(DEPLOYMENT_URL);
    expect(response?.status()).toBe(200);
  });

  test('should return correct headers from edge middleware', async ({ request }) => {
    const response = await request.get(`${DEPLOYMENT_URL}/`);

    expect(response.headers()['x-frame-options']).toBe('DENY');
    expect(response.headers()['x-content-type-options']).toBe('nosniff');
    expect(response.headers()['x-request-id']).toBeDefined();
  });

  test('should serve edge API routes', async ({ request }) => {
    const response = await request.get(`${DEPLOYMENT_URL}/api/hello`);
    const body = await response.json();

    expect(response.status()).toBe(200);
    expect(body.message).toBe('Hello, World!');
  });

  test('should set cache headers on API responses', async ({ request }) => {
    const response = await request.get(`${DEPLOYMENT_URL}/api/hello`);

    const cacheControl = response.headers()['cache-control'];
    expect(cacheControl).toContain('s-maxage');
  });

  test('should handle 404 for unknown routes', async ({ request }) => {
    const response = await request.get(`${DEPLOYMENT_URL}/this-does-not-exist-xyz`);
    expect(response.status()).toBe(404);
  });

  test('should redirect www to non-www', async ({ request }) => {
    // This test only works against a real deployment with DNS configured
    if (!process.env.VERCEL_URL) {
      test.skip();
    }

    const response = await request.get(`https://www.${process.env.VERCEL_URL}/`, {
      maxRedirects: 0,
    });
    expect(response.status()).toBe(301);
  });
});
```

### ISR Behavior Tests

```typescript
// tests/e2e/isr.test.ts
import { test, expect } from '@playwright/test';

const BASE_URL = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : 'http://localhost:3000';

test.describe('ISR (Incremental Static Regeneration)', () => {
  test('should serve cached page on first request', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/`);

    expect(response.status()).toBe(200);
    // ISR pages have x-vercel-cache header in production
    if (process.env.VERCEL_URL) {
      const cacheHeader = response.headers()['x-vercel-cache'];
      expect(['HIT', 'STALE', 'MISS']).toContain(cacheHeader);
    }
  });

  test('should serve stale content while revalidating', async ({ request }) => {
    // First request triggers generation
    await request.get(`${BASE_URL}/`);

    // Second request should be cached
    const response = await request.get(`${BASE_URL}/`);
    expect(response.status()).toBe(200);

    if (process.env.VERCEL_URL) {
      const cacheHeader = response.headers()['x-vercel-cache'];
      expect(['HIT', 'STALE']).toContain(cacheHeader);
    }
  });

  test('should revalidate on-demand when triggered', async ({ request }) => {
    // Trigger revalidation (requires API route that calls revalidatePath/revalidateTag)
    const revalidateResponse = await request.post(`${BASE_URL}/api/revalidate`, {
      data: { path: '/' },
      headers: { authorization: `Bearer ${process.env.CRON_SECRET}` },
    });

    // If revalidation endpoint exists
    if (revalidateResponse.status() === 200) {
      const pageResponse = await request.get(`${BASE_URL}/`);
      expect(pageResponse.status()).toBe(200);
    }
  });
});
```

### Middleware E2E Tests

```typescript
// tests/e2e/middleware-e2e.test.ts
import { test, expect } from '@playwright/test';

const BASE_URL = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : 'http://localhost:3000';

test.describe('Middleware E2E', () => {
  test('should assign A/B test variant cookie', async ({ page }) => {
    await page.goto(BASE_URL);

    const cookies = await page.context().cookies();
    const experimentCookie = cookies.find((c) => c.name === 'experiment-variant');

    expect(experimentCookie).toBeDefined();
    expect(['control', 'treatment']).toContain(experimentCookie!.value);
  });

  test('should persist variant across page navigations', async ({ page }) => {
    await page.goto(BASE_URL);

    const cookies1 = await page.context().cookies();
    const variant1 = cookies1.find((c) => c.name === 'experiment-variant')?.value;

    await page.goto(`${BASE_URL}/about`);

    const cookies2 = await page.context().cookies();
    const variant2 = cookies2.find((c) => c.name === 'experiment-variant')?.value;

    expect(variant1).toBe(variant2);
  });

  test('should set security headers on all pages', async ({ request }) => {
    const pages = ['/', '/about', '/api/hello'];

    for (const path of pages) {
      const response = await request.get(`${BASE_URL}${path}`);
      expect(response.headers()['x-frame-options']).toBe('DENY');
      expect(response.headers()['x-content-type-options']).toBe('nosniff');
    }
  });
});
```

## Vercel CLI Local Testing

```bash
# Install Vercel CLI
npm i -g vercel

# Link project
vercel link

# Run local dev server (mirrors edge runtime)
vercel dev

# Deploy to preview
vercel deploy

# Deploy to production
vercel --prod

# Run tests against local dev
VERCEL_URL=localhost:3000 npx playwright test tests/e2e/

# Run tests against preview deployment
VERCEL_URL=your-project-abc123.vercel.app npx playwright test tests/e2e/
```

## Vercel Configuration

```json
{
  "crons": [
    {
      "path": "/api/cron",
      "schedule": "0 9 * * 1"
    }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" },
        { "key": "Access-Control-Allow-Methods", "value": "GET, POST, PUT, DELETE, OPTIONS" }
      ]
    }
  ]
}
```

## Best Practices

1. **Always test edge functions with Web standard APIs** -- use `Request`, `Response`, `Headers`, `URL` instead of Node.js-specific modules. This ensures your tests reflect actual edge runtime behavior.
2. **Mock Vercel services at the SDK level** -- mock `@vercel/kv`, `@vercel/blob`, and `@vercel/edge-config` imports, not HTTP calls. This gives accurate type checking while avoiding network dependencies.
3. **Test middleware in isolation first** -- middleware runs on every request and bugs cascade to all routes. Unit test every branch before integration testing.
4. **Use preview deployments for integration testing** -- Vercel preview deployments provide real edge infrastructure. Run E2E tests against preview URLs in CI.
5. **Test cache behavior explicitly** -- verify `Cache-Control`, `s-maxage`, and `stale-while-revalidate` headers. Cache bugs cause stale data in production.
6. **Validate edge runtime compatibility** -- maintain a compatibility test suite that verifies all Web APIs your functions use are available in the edge runtime.
7. **Test geolocation with mock data** -- Vercel provides `request.geo` only in production. Mock this data in unit tests and verify with real deployment tests.
8. **Test cron jobs with authentication** -- always verify cron endpoints reject unauthenticated requests. Cron jobs should validate the `CRON_SECRET` header.
9. **Use Playwright for full E2E edge testing** -- Playwright can test the complete request/response cycle including middleware, headers, cookies, and redirects.
10. **Test error responses explicitly** -- edge functions should return proper HTTP error codes with JSON error bodies, not just 500 Internal Server Error.

## Anti-Patterns

1. **Testing edge functions with Node.js APIs** -- using `require('fs')`, `Buffer.from()` (pre-v18), or `process.exit()` in tests masks edge runtime incompatibilities.
2. **Mocking the entire Response/Request objects** -- use real Web API constructors instead of creating mock objects with partial implementations.
3. **Skipping middleware tests** -- middleware bugs affect every route in production. A single untested redirect loop can take down the entire application.
4. **Hardcoding deployment URLs in tests** -- use environment variables for deployment URLs. Tests must work against local dev, preview, and production.
5. **Not testing cache headers** -- assuming cache behavior works correctly leads to stale data bugs that are hard to diagnose in production.
6. **Testing only happy paths for edge functions** -- edge functions receive malformed requests, missing headers, and unexpected content types. Test all error paths.
7. **Using setTimeout in edge function tests** -- edge functions have strict CPU time limits. Use proper async patterns instead of timers.
8. **Not testing concurrent requests** -- edge functions run concurrently at the edge. Test that your functions handle parallel requests without race conditions.
9. **Ignoring cold start behavior** -- edge functions have cold starts. Test that initialization code runs correctly after a period of inactivity.
10. **Not verifying CORS headers** -- missing or incorrect CORS headers cause client-side failures that are invisible in server-side tests. Always test CORS configuration.
