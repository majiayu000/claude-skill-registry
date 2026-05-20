---
name: monitoring
description: Observability patterns for production - logging, error tracking, analytics. Use when setting up monitoring.
triggers:
  - monitoring
  - logs
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: opus
user-invocable: true
---

# Monitoring Skill

## Quick Commands

| Say | Action |
|-----|--------|
| `add logging` | Set up structured logging |
| `add error tracking` | Integrate Sentry/error boundary |
| `add analytics` | Add Vercel Analytics |

## Structured Logging

```typescript
// lib/logger.ts
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogContext {
  userId?: string;
  action?: string;
  [key: string]: unknown;
}

export function log(level: LogLevel, message: string, context?: LogContext) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    ...context
  };

  if (process.env.NODE_ENV === 'production') {
    console[level](JSON.stringify(entry));
  } else {
    console[level](message, context);
  }
}
```

## Error Boundary

```tsx
// components/error-boundary.tsx
'use client';

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log to external service
    log('error', 'React error boundary caught error', {
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack
    });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <div>Something went wrong</div>;
    }
    return this.props.children;
  }
}
```

## Vercel Analytics

```tsx
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

## API Route Monitoring

```typescript
// lib/api-monitor.ts
export function withMonitoring<T>(
  handler: () => Promise<T>,
  context: { route: string; method: string }
): Promise<T> {
  const start = Date.now();

  return handler()
    .then(result => {
      log('info', 'API request completed', {
        ...context,
        duration: Date.now() - start,
        status: 'success'
      });
      return result;
    })
    .catch(error => {
      log('error', 'API request failed', {
        ...context,
        duration: Date.now() - start,
        error: error.message
      });
      throw error;
    });
}
```

## Health Check Endpoint

```typescript
// app/api/health/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    version: process.env.VERCEL_GIT_COMMIT_SHA?.slice(0, 7) ?? 'dev'
  };

  return NextResponse.json(health);
}
```

## Key Metrics to Track

| Metric | Why |
|--------|-----|
| Response time (p50, p95, p99) | User experience |
| Error rate | Reliability |
| Request count | Traffic patterns |
| Memory usage | Resource leaks |
| Cold start duration | Serverless performance |

## Best Practices

**DO:**
- Use structured JSON logs in production
- Include request IDs for tracing
- Set up alerting thresholds
- Monitor Core Web Vitals
- Track user-facing errors separately

**DON'T:**
- Log sensitive data (passwords, tokens)
- Log every request in detail (costs)
- Ignore client-side errors
- Skip error context
