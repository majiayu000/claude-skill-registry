---
name: sentry
description: Monitors applications with Sentry including error tracking, performance monitoring, and alerting. Use when tracking errors, monitoring performance, setting up alerts, or debugging production issues.
---

# Sentry

Application monitoring platform for error tracking and performance monitoring.

## Quick Start

**Install (Next.js):**
```bash
npx @sentry/wizard@latest -i nextjs
```

**Manual install:**
```bash
npm install @sentry/nextjs
```

## Configuration

### Environment Variables

```bash
# .env.local
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
SENTRY_AUTH_TOKEN=sntrys_...
SENTRY_ORG=your-org
SENTRY_PROJECT=your-project
```

### Sentry Config

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,

  // Performance Monitoring
  tracesSampleRate: 1.0, // 100% in dev, lower in prod

  // Session Replay
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,

  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],

  // Release tracking
  release: process.env.NEXT_PUBLIC_SENTRY_RELEASE,

  // Ignore specific errors
  ignoreErrors: [
    'ResizeObserver loop limit exceeded',
    'Non-Error promise rejection',
  ],

  // Filter breadcrumbs
  beforeBreadcrumb(breadcrumb) {
    if (breadcrumb.category === 'console') {
      return null; // Don't capture console logs
    }
    return breadcrumb;
  },
});
```

### Server Config

```typescript
// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,

  // Additional server-side options
  profilesSampleRate: 1.0,
});
```

### Edge Config

```typescript
// sentry.edge.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
});
```

### Next.js Config

```typescript
// next.config.js
const { withSentryConfig } = require('@sentry/nextjs');

const nextConfig = {
  // Your Next.js config
};

module.exports = withSentryConfig(nextConfig, {
  // Sentry webpack plugin options
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,
  authToken: process.env.SENTRY_AUTH_TOKEN,

  // Upload source maps
  silent: true,
  widenClientFileUpload: true,
  hideSourceMaps: true,

  // Disable Sentry during builds
  disableLogger: true,
});
```

## Error Tracking

### Automatic Capture

Sentry automatically captures:
- Unhandled exceptions
- Unhandled promise rejections
- Console errors

### Manual Capture

```typescript
import * as Sentry from '@sentry/nextjs';

// Capture exception
try {
  riskyOperation();
} catch (error) {
  Sentry.captureException(error);
}

// Capture message
Sentry.captureMessage('Something happened');

// With severity
Sentry.captureMessage('Warning message', 'warning');
Sentry.captureMessage('Info message', 'info');
```

### Add Context

```typescript
// Set user context
Sentry.setUser({
  id: user.id,
  email: user.email,
  username: user.username,
});

// Clear user on logout
Sentry.setUser(null);

// Add tags
Sentry.setTag('feature', 'checkout');
Sentry.setTag('plan', 'premium');

// Add extra data
Sentry.setExtra('cart_items', cartItems);

// Set context
Sentry.setContext('order', {
  orderId: order.id,
  total: order.total,
  items: order.items.length,
});
```

### Scopes

```typescript
// Configure scope for specific capture
Sentry.withScope((scope) => {
  scope.setTag('section', 'payments');
  scope.setLevel('error');
  scope.setExtra('paymentData', paymentData);
  Sentry.captureException(error);
});
```

## Error Boundaries

### React Error Boundary

```tsx
'use client';

import * as Sentry from '@sentry/nextjs';
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    Sentry.withScope((scope) => {
      scope.setExtra('componentStack', errorInfo.componentStack);
      Sentry.captureException(error);
    });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}
```

### Sentry Error Boundary

```tsx
import * as Sentry from '@sentry/nextjs';

<Sentry.ErrorBoundary
  fallback={<p>Something went wrong</p>}
  showDialog
>
  <App />
</Sentry.ErrorBoundary>
```

## API Routes

### App Router

```typescript
// app/api/example/route.ts
import * as Sentry from '@sentry/nextjs';
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const data = await request.json();
    // Process data
    return NextResponse.json({ success: true });
  } catch (error) {
    Sentry.captureException(error, {
      extra: {
        endpoint: '/api/example',
        method: 'POST',
      },
    });
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### Wrap API Handler

```typescript
import { wrapApiHandlerWithSentry } from '@sentry/nextjs';

async function handler(req: NextRequest) {
  // Your API logic
}

export const POST = wrapApiHandlerWithSentry(handler, '/api/example');
```

## Performance Monitoring

### Custom Transactions

```typescript
import * as Sentry from '@sentry/nextjs';

async function processOrder(orderId: string) {
  return Sentry.startSpan(
    {
      name: 'Process Order',
      op: 'order.process',
    },
    async (span) => {
      span.setAttribute('order_id', orderId);

      // Nested span
      await Sentry.startSpan(
        {
          name: 'Validate Order',
          op: 'order.validate',
        },
        async () => {
          await validateOrder(orderId);
        }
      );

      // Another nested span
      await Sentry.startSpan(
        {
          name: 'Charge Payment',
          op: 'payment.charge',
        },
        async () => {
          await chargePayment(orderId);
        }
      );

      return { success: true };
    }
  );
}
```

### Measure Performance

```typescript
// Measure async operation
const result = await Sentry.startSpan(
  { name: 'Database Query', op: 'db.query' },
  async () => {
    return await db.query.users.findMany();
  }
);
```

## Server Actions

```typescript
// app/actions.ts
'use server';

import * as Sentry from '@sentry/nextjs';

export async function submitForm(formData: FormData) {
  return Sentry.withServerActionInstrumentation(
    'submitForm',
    {},
    async () => {
      try {
        // Process form
        const result = await processForm(formData);
        return { success: true, data: result };
      } catch (error) {
        Sentry.captureException(error);
        return { success: false, error: 'Form submission failed' };
      }
    }
  );
}
```

## Session Replay

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,

  integrations: [
    Sentry.replayIntegration({
      // Capture 10% of sessions
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],

  // Sample rates
  replaysSessionSampleRate: 0.1, // 10% of sessions
  replaysOnErrorSampleRate: 1.0, // 100% of sessions with errors
});
```

## Source Maps

### Upload During Build

```typescript
// next.config.js
module.exports = withSentryConfig(nextConfig, {
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,
  authToken: process.env.SENTRY_AUTH_TOKEN,

  // Hide source maps from client
  hideSourceMaps: true,

  // Automatically delete source maps after upload
  deleteFilesAfterUpload: ['**/*.map'],
});
```

### Manual Upload

```bash
npx @sentry/cli sourcemaps upload ./dist \
  --org your-org \
  --project your-project \
  --auth-token $SENTRY_AUTH_TOKEN
```

## Alerts and Notifications

Configure in Sentry dashboard:
- Error thresholds
- Performance degradation
- Crash-free rate drops
- Slack/email notifications

## Filtering Events

```typescript
Sentry.init({
  dsn: process.env.SENTRY_DSN,

  beforeSend(event, hint) {
    // Filter out known issues
    if (event.exception?.values?.[0]?.type === 'NetworkError') {
      return null; // Don't send
    }

    // Modify event
    if (event.user) {
      delete event.user.email; // Remove PII
    }

    return event;
  },

  beforeSendTransaction(transaction) {
    // Filter transactions
    if (transaction.transaction === '/health') {
      return null;
    }
    return transaction;
  },
});
```

## Release Tracking

```typescript
// Set release in config
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  release: process.env.VERCEL_GIT_COMMIT_SHA,
});

// Or dynamically
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  release: `${process.env.npm_package_name}@${process.env.npm_package_version}`,
});
```

## Best Practices

1. **Set sample rates appropriately** - 100% in dev, lower in prod
2. **Add user context** - Helps identify affected users
3. **Use tags for filtering** - Feature, environment, version
4. **Configure alerts** - Get notified of new issues
5. **Upload source maps** - Readable stack traces

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Exposing DSN client-side | DSN is safe to expose |
| 100% sample rate in prod | Use lower rates |
| Missing source maps | Configure upload in build |
| No user context | Set user on login |
| Capturing too much | Filter with beforeSend |

## Reference Files

- [references/configuration.md](references/configuration.md) - Full config options
- [references/performance.md](references/performance.md) - Performance monitoring
- [references/integrations.md](references/integrations.md) - Third-party integrations
