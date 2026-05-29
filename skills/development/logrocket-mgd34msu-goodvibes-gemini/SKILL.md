---
name: logrocket
description: Implements session replay and error tracking with LogRocket for debugging user issues. Use when adding session recording, error monitoring, and performance tracking to React applications.
---

# LogRocket

Session replay platform with error tracking, performance monitoring, and product analytics. Captures every user interaction for debugging.

## Quick Start

```bash
npm install logrocket logrocket-react
```

### Basic Setup

```typescript
// logrocketSetup.ts
import LogRocket from 'logrocket';

LogRocket.init('your-app-id/your-project');
```

```typescript
// main.tsx - Import setup FIRST
import './logrocketSetup';
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

## User Identification

```typescript
import LogRocket from 'logrocket';

// Identify user after login
function onLogin(user) {
  LogRocket.identify(user.id, {
    name: user.name,
    email: user.email,

    // Custom attributes
    subscriptionType: user.plan,
    createdAt: user.createdAt,
  });
}

// Anonymous session (before login)
LogRocket.identify('anonymous-user-123');
```

## Custom Events

```typescript
import LogRocket from 'logrocket';

// Basic event
LogRocket.track('Button Clicked');

// Event with properties
LogRocket.track('PurchaseComplete', {
  revenue: 42.99,
  productCategory: 'Clothing',
  productSku: 4887369299,
  couponApplied: true,
  customerSegments: ['aef34b', '97cb20'],
});

// Form submission
LogRocket.track('FormSubmitted', {
  formName: 'contact',
  success: true,
});

// Feature usage
LogRocket.track('FeatureUsed', {
  featureName: 'export',
  format: 'csv',
});
```

## React Error Boundary

```tsx
import LogRocket from 'logrocket';
import setupLogRocketReact from 'logrocket-react';

// After LogRocket.init()
setupLogRocketReact(LogRocket);
```

This automatically captures:
- React component errors
- Error boundary crashes
- Component stack traces

### Manual Error Logging

```typescript
import LogRocket from 'logrocket';

try {
  // risky operation
} catch (error) {
  LogRocket.captureException(error);
}

// With extra context
LogRocket.captureException(error, {
  tags: {
    component: 'PaymentForm',
    userId: 'user_123',
  },
  extra: {
    orderId: 'order_456',
    attemptNumber: 3,
  },
});
```

## Console Logging

LogRocket captures console logs automatically. Add custom context:

```typescript
import LogRocket from 'logrocket';

// Log with structured data
LogRocket.log('Processing order', { orderId: 'order_123', items: 3 });
LogRocket.info('User action', { action: 'checkout_started' });
LogRocket.warn('Rate limit approaching', { remaining: 10 });
LogRocket.error('Payment failed', { reason: 'insufficient_funds' });
```

## Redux Integration

```typescript
import LogRocket from 'logrocket';
import { createStore, applyMiddleware } from 'redux';

const store = createStore(
  rootReducer,
  applyMiddleware(LogRocket.reduxMiddleware())
);
```

### With Redux Toolkit

```typescript
import { configureStore } from '@reduxjs/toolkit';
import LogRocket from 'logrocket';

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(LogRocket.reduxMiddleware()),
});
```

## Network Request Logging

LogRocket captures network requests automatically. Sanitize sensitive data:

```typescript
LogRocket.init('app-id/project', {
  network: {
    requestSanitizer: (request) => {
      // Remove authorization header
      if (request.headers['Authorization']) {
        request.headers['Authorization'] = '[REDACTED]';
      }

      // Sanitize request body
      if (request.body) {
        const body = JSON.parse(request.body);
        if (body.password) {
          body.password = '[REDACTED]';
        }
        request.body = JSON.stringify(body);
      }

      return request;
    },
    responseSanitizer: (response) => {
      // Sanitize response body
      if (response.body) {
        const body = JSON.parse(response.body);
        if (body.token) {
          body.token = '[REDACTED]';
        }
        response.body = JSON.stringify(body);
      }
      return response;
    },
  },
});
```

## Privacy & Sanitization

### Mask Sensitive Data

```typescript
LogRocket.init('app-id/project', {
  dom: {
    // Mask all inputs
    inputSanitizer: true,

    // Mask specific elements
    textSanitizer: true,

    // Mask by CSS selector
    privateAttributeBlocklist: ['data-private'],
  },
});
```

### HTML Masking

```html
<!-- Mask specific elements -->
<input type="password" data-private />
<div data-private>Sensitive content</div>

<!-- Or use CSS class -->
<div class="lr-hide">Hidden from replay</div>
```

### Block Recording

```html
<!-- Completely hide from DOM -->
<div data-logrocket-hidden>
  This content won't appear in recordings
</div>
```

## Conditional Recording

Only record certain users or conditions:

```typescript
import LogRocket from 'logrocket';

// Check condition before initializing
if (shouldRecordUser(user)) {
  LogRocket.init('app-id/project');
  LogRocket.identify(user.id, { name: user.name });
}

// Or start/stop recording
LogRocket.startRecording();
LogRocket.stopRecording();
```

### Sample Rate

```typescript
LogRocket.init('app-id/project', {
  shouldSendData: () => {
    // Record 10% of sessions
    return Math.random() < 0.1;
  },
});
```

## Session URL

Get the session URL for support tickets:

```typescript
import LogRocket from 'logrocket';

LogRocket.getSessionURL((sessionURL) => {
  // Send to support system
  console.log('Session URL:', sessionURL);

  // Or add to error reports
  Sentry.setExtra('sessionURL', sessionURL);
});
```

## Integration with Error Tracking

### Sentry

```typescript
import * as Sentry from '@sentry/react';
import LogRocket from 'logrocket';

LogRocket.getSessionURL((sessionURL) => {
  Sentry.configureScope((scope) => {
    scope.setExtra('sessionURL', sessionURL);
  });
});
```

### Custom Integration

```typescript
import LogRocket from 'logrocket';

LogRocket.getSessionURL((sessionURL) => {
  // Add to your error tracking
  errorTracker.setContext('logrocket_session', sessionURL);

  // Or send to your backend
  fetch('/api/session', {
    method: 'POST',
    body: JSON.stringify({ sessionURL, userId: currentUser.id }),
  });
});
```

## Next.js Integration

```tsx
// app/providers.tsx
'use client';

import { useEffect } from 'react';
import LogRocket from 'logrocket';
import setupLogRocketReact from 'logrocket-react';

export function LogRocketProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    if (typeof window !== 'undefined') {
      LogRocket.init('app-id/project');
      setupLogRocketReact(LogRocket);
    }
  }, []);

  return <>{children}</>;
}
```

```tsx
// app/layout.tsx
import { LogRocketProvider } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <LogRocketProvider>
          {children}
        </LogRocketProvider>
      </body>
    </html>
  );
}
```

## Configuration Options

```typescript
LogRocket.init('app-id/project', {
  // Console options
  console: {
    isEnabled: true,
    shouldAggregateConsoleErrors: true,
  },

  // Network options
  network: {
    isEnabled: true,
    requestSanitizer: (request) => request,
    responseSanitizer: (response) => response,
  },

  // DOM options
  dom: {
    isEnabled: true,
    inputSanitizer: true,
    textSanitizer: false,
    baseHref: 'https://yourdomain.com',
  },

  // Release tracking
  release: process.env.NEXT_PUBLIC_VERSION,

  // Parent domain (for cross-subdomain tracking)
  parentDomain: 'yourdomain.com',

  // Merge IDs (connect anonymous with identified)
  mergeImmediately: true,
});
```

## TypeScript

```typescript
import LogRocket from 'logrocket';

interface UserTraits {
  name: string;
  email: string;
  plan: 'free' | 'pro' | 'enterprise';
  createdAt: string;
}

function identifyUser(userId: string, traits: UserTraits) {
  LogRocket.identify(userId, traits);
}

interface PurchaseEvent {
  productId: string;
  amount: number;
  currency: string;
}

function trackPurchase(event: PurchaseEvent) {
  LogRocket.track('Purchase', event);
}
```

## Performance Monitoring

LogRocket automatically captures:
- Page load times
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Time to Interactive (TTI)
- Network request timing

Access in the LogRocket dashboard under Performance.

## Best Practices

1. **Initialize early** - Import setup file before other modules
2. **Identify users** - Connect sessions to user accounts
3. **Sanitize data** - Never record passwords or tokens
4. **Use conditional recording** - Sample in production
5. **Track key events** - Conversions, errors, feature usage
6. **Integrate with error tracking** - Link sessions to Sentry/etc
7. **Use private attributes** - Mark sensitive DOM elements
