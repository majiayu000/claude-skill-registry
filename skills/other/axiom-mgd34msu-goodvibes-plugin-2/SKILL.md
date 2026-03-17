---
name: axiom
description: Implements structured logging and observability with Axiom for serverless applications. Use when adding logging, tracing, and Web Vitals monitoring to Next.js and Vercel applications.
---

# Axiom

Observability platform for logs, metrics, and traces. Native Vercel integration with structured logging for Next.js applications.

## Quick Start

```bash
npm install @axiomhq/js @axiomhq/logging @axiomhq/nextjs @axiomhq/react
```

## Next.js Setup (2025 API)

### Create Axiom Client

```typescript
// lib/axiom/client.ts
import { Axiom } from '@axiomhq/js';

export const axiom = new Axiom({
  token: process.env.AXIOM_TOKEN!,
  orgId: process.env.AXIOM_ORG_ID,
});
```

### Create Logger

```typescript
// lib/axiom/logger.ts
import { Logger, ConsoleTransport, AxiomJSTransport } from '@axiomhq/logging';
import { nextJsFormatters } from '@axiomhq/nextjs';
import { axiom } from './client';

export const logger = new Logger({
  transports: [
    new AxiomJSTransport({
      axiom,
      dataset: process.env.AXIOM_DATASET!,
    }),
    new ConsoleTransport(),
  ],
  formatters: nextJsFormatters,
});
```

### Create Route Handler

```typescript
// lib/axiom/route.ts
import { createAxiomRouteHandler } from '@axiomhq/nextjs';
import { axiom } from './client';
import { logger } from './logger';

export const axiomRouteHandler = createAxiomRouteHandler({
  axiom,
  logger,
  dataset: process.env.AXIOM_DATASET!,
});
```

### API Route Handler

```typescript
// app/api/axiom/route.ts
import { axiomRouteHandler } from '@/lib/axiom/route';

export const POST = axiomRouteHandler;
```

## Logging

### Server Components

```typescript
// app/page.tsx
import { logger } from '@/lib/axiom/logger';

export default async function Page() {
  logger.info('Page rendered', { page: 'home' });

  try {
    const data = await fetchData();
    logger.debug('Data fetched', { count: data.length });
    return <div>{/* render */}</div>;
  } catch (error) {
    logger.error('Failed to fetch data', { error });
    throw error;
  } finally {
    await logger.flush();
  }
}
```

### API Routes

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/axiom/logger';

export async function POST(request: NextRequest) {
  const body = await request.json();

  logger.info('Creating user', {
    email: body.email,
    source: request.headers.get('referer'),
  });

  try {
    const user = await createUser(body);
    logger.info('User created', { userId: user.id });
    return NextResponse.json(user);
  } catch (error) {
    logger.error('User creation failed', {
      error: error instanceof Error ? error.message : 'Unknown error',
      email: body.email,
    });
    return NextResponse.json({ error: 'Failed' }, { status: 500 });
  } finally {
    await logger.flush();
  }
}
```

### Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { logger } from '@/lib/axiom/logger';

export async function middleware(request: NextRequest) {
  const start = Date.now();

  logger.info('Request started', {
    path: request.nextUrl.pathname,
    method: request.method,
  });

  const response = NextResponse.next();

  logger.info('Request completed', {
    path: request.nextUrl.pathname,
    duration: Date.now() - start,
  });

  await logger.flush();
  return response;
}
```

## Client-Side Logging

```tsx
// app/providers.tsx
'use client';

import { AxiomWebVitals } from '@axiomhq/react';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <>
      <AxiomWebVitals />
      {children}
    </>
  );
}
```

### Client Logger (Proxy Method)

Send logs through your API to avoid exposing tokens:

```typescript
// lib/axiom/client-logger.ts
class ClientLogger {
  private queue: Array<{ level: string; message: string; data?: object }> = [];

  log(level: string, message: string, data?: object) {
    this.queue.push({ level, message, data });
  }

  info(message: string, data?: object) {
    this.log('info', message, data);
  }

  error(message: string, data?: object) {
    this.log('error', message, data);
  }

  async flush() {
    if (this.queue.length === 0) return;

    const logs = [...this.queue];
    this.queue = [];

    await fetch('/api/axiom', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ logs }),
    });
  }
}

export const clientLogger = new ClientLogger();
```

### Client Component Usage

```tsx
'use client';

import { useEffect } from 'react';
import { clientLogger } from '@/lib/axiom/client-logger';

export function TrackableButton() {
  const handleClick = () => {
    clientLogger.info('Button clicked', { buttonId: 'cta' });
    clientLogger.flush();
  };

  useEffect(() => {
    clientLogger.info('Component mounted');
    return () => {
      clientLogger.info('Component unmounted');
      clientLogger.flush();
    };
  }, []);

  return <button onClick={handleClick}>Click me</button>;
}
```

## Web Vitals

Automatic Core Web Vitals tracking:

```tsx
// app/layout.tsx
import { AxiomWebVitals } from '@axiomhq/react';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AxiomWebVitals />
        {children}
      </body>
    </html>
  );
}
```

## Legacy API (next-axiom)

The older `next-axiom` package is still supported:

```bash
npm install next-axiom
```

### Setup

```typescript
// next.config.js
const { withAxiom } = require('next-axiom');

module.exports = withAxiom({
  // your next config
});
```

### Server Component Logging

```typescript
import { Logger } from 'next-axiom';

export default async function Page() {
  const log = new Logger();
  log.info('Page rendered');
  await log.flush();

  return <div>Content</div>;
}
```

### Client Component Logging

```tsx
'use client';

import { useLogger } from 'next-axiom';

export function ClientComponent() {
  const log = useLogger();

  const handleClick = () => {
    log.info('Button clicked');
  };

  return <button onClick={handleClick}>Click</button>;
}
```

## Structured Logging Patterns

### Request Context

```typescript
function createRequestLogger(request: NextRequest) {
  return {
    info: (message: string, data?: object) => {
      logger.info(message, {
        ...data,
        requestId: request.headers.get('x-request-id'),
        path: request.nextUrl.pathname,
        method: request.method,
        userAgent: request.headers.get('user-agent'),
      });
    },
    error: (message: string, data?: object) => {
      logger.error(message, {
        ...data,
        requestId: request.headers.get('x-request-id'),
        path: request.nextUrl.pathname,
      });
    },
  };
}
```

### Timing

```typescript
async function withTiming<T>(
  name: string,
  fn: () => Promise<T>
): Promise<T> {
  const start = Date.now();
  try {
    const result = await fn();
    logger.info(`${name} completed`, {
      duration: Date.now() - start,
      success: true,
    });
    return result;
  } catch (error) {
    logger.error(`${name} failed`, {
      duration: Date.now() - start,
      error: error instanceof Error ? error.message : 'Unknown',
    });
    throw error;
  }
}

// Usage
const users = await withTiming('fetchUsers', () => db.user.findMany());
```

### Error Logging

```typescript
function logError(error: unknown, context?: object) {
  if (error instanceof Error) {
    logger.error(error.message, {
      ...context,
      name: error.name,
      stack: error.stack,
      cause: error.cause,
    });
  } else {
    logger.error('Unknown error', {
      ...context,
      error: String(error),
    });
  }
}
```

## Vercel Integration

Enable the Axiom integration in Vercel for automatic log drains:

1. Go to Vercel Dashboard > Integrations
2. Install Axiom integration
3. Connect your Axiom organization
4. Logs from `console.log`, `console.error`, etc. are automatically sent

## Environment Variables

```bash
AXIOM_TOKEN=xaat-xxxxxxxx
AXIOM_ORG_ID=your-org-id
AXIOM_DATASET=your-dataset

# For next-axiom
NEXT_PUBLIC_AXIOM_INGEST_ENDPOINT=https://api.axiom.co/v1/datasets/your-dataset/ingest
```

## Query Examples (APL)

```
// Recent errors
dataset
| where level == "error"
| order by _time desc
| limit 100

// Request latency by path
dataset
| where message == "Request completed"
| summarize avg(duration), p95(duration), count() by path
| order by count_ desc

// Errors by type
dataset
| where level == "error"
| summarize count() by ['error.name']
| order by count_ desc
```

## Best Practices

1. **Flush before returning** - Always call flush() in server components
2. **Use structured data** - Pass objects, not strings
3. **Add request context** - Include requestId, path, method
4. **Log at appropriate levels** - debug, info, warn, error
5. **Proxy client logs** - Don't expose tokens to browser
6. **Use Vercel integration** - For automatic console.log capture
7. **Add timing** - Track duration for performance monitoring
