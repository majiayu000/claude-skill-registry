---
name: posthog
description: Implements product analytics with PostHog including event tracking, feature flags, and session replay. Use when adding analytics, A/B testing, or user behavior tracking to React and Next.js applications.
---

# PostHog

Product analytics platform with autocapture, feature flags, session replay, and A/B testing. Open source with self-hosting option.

## Quick Start

```bash
npm install posthog-js @posthog/react
```

### React Setup

```tsx
// src/main.tsx or src/index.tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import posthog from 'posthog-js';
import { PostHogProvider } from '@posthog/react';
import App from './App';

posthog.init(import.meta.env.VITE_PUBLIC_POSTHOG_KEY, {
  api_host: import.meta.env.VITE_PUBLIC_POSTHOG_HOST || 'https://us.i.posthog.com',
  defaults: '2025-11-30',  // Use 2025 defaults
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <PostHogProvider client={posthog}>
      <App />
    </PostHogProvider>
  </StrictMode>
);
```

### Next.js App Router Setup

```tsx
// app/providers.tsx
'use client';

import posthog from 'posthog-js';
import { PostHogProvider as PHProvider } from '@posthog/react';
import { useEffect } from 'react';

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://us.i.posthog.com',
      defaults: '2025-11-30',
      capture_pageview: 'history_change',  // Auto-capture for App Router
    });
  }, []);

  return <PHProvider client={posthog}>{children}</PHProvider>;
}
```

```tsx
// app/layout.tsx
import { PostHogProvider } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <PostHogProvider>
          {children}
        </PostHogProvider>
      </body>
    </html>
  );
}
```

## Event Tracking

### Using the usePostHog Hook

```tsx
import { usePostHog } from '@posthog/react';

function ProductCard({ product }) {
  const posthog = usePostHog();

  const handleAddToCart = () => {
    posthog.capture('add_to_cart', {
      product_id: product.id,
      product_name: product.name,
      price: product.price,
      category: product.category,
    });
  };

  const handleView = () => {
    posthog.capture('product_viewed', {
      product_id: product.id,
      product_name: product.name,
    });
  };

  return (
    <div onClick={handleView}>
      <h3>{product.name}</h3>
      <button onClick={handleAddToCart}>Add to Cart</button>
    </div>
  );
}
```

### Common Events

```tsx
const posthog = usePostHog();

// Page views (automatic with defaults: '2025-11-30')
// posthog.capture('$pageview');  // Usually not needed

// User actions
posthog.capture('button_clicked', { button_name: 'signup' });
posthog.capture('form_submitted', { form_name: 'contact' });
posthog.capture('file_downloaded', { file_name: 'report.pdf' });

// Ecommerce
posthog.capture('purchase_completed', {
  order_id: 'order_123',
  total: 99.99,
  currency: 'USD',
  items: ['product_1', 'product_2'],
});

// Feature usage
posthog.capture('feature_used', {
  feature_name: 'export',
  feature_variant: 'csv',
});
```

## User Identification

```tsx
const posthog = usePostHog();

// Identify user after login
function onLogin(user) {
  posthog.identify(user.id, {
    email: user.email,
    name: user.name,
    plan: user.subscription?.plan,
    created_at: user.createdAt,
  });
}

// Reset on logout
function onLogout() {
  posthog.reset();
}

// Update user properties
posthog.people.set({
  plan: 'pro',
  last_active: new Date().toISOString(),
});

// Set properties once (won't overwrite)
posthog.people.set_once({
  initial_referrer: document.referrer,
  signup_date: new Date().toISOString(),
});
```

## Feature Flags

### Check Flag Status

```tsx
import { useFeatureFlagEnabled, useFeatureFlagVariantKey } from '@posthog/react';

function FeatureComponent() {
  // Boolean flag
  const showNewFeature = useFeatureFlagEnabled('new-feature');

  // Multivariate flag
  const variant = useFeatureFlagVariantKey('checkout-experiment');

  if (!showNewFeature) {
    return null;
  }

  return (
    <div>
      {variant === 'control' && <OldCheckout />}
      {variant === 'test' && <NewCheckout />}
    </div>
  );
}
```

### PostHogFeature Component

```tsx
import { PostHogFeature } from '@posthog/react';

function App() {
  return (
    <div>
      <PostHogFeature flag="new-dashboard" match={true}>
        <NewDashboard />
      </PostHogFeature>

      <PostHogFeature flag="new-dashboard" match={false}>
        <OldDashboard />
      </PostHogFeature>
    </div>
  );
}
```

### Feature Flag with Payload

```tsx
import { useFeatureFlagPayload, useFeatureFlagEnabled } from '@posthog/react';

function PricingPage() {
  // Use both hooks to track experiment exposure
  const isEnabled = useFeatureFlagEnabled('pricing-experiment');
  const payload = useFeatureFlagPayload('pricing-experiment');

  if (!isEnabled || !payload) {
    return <DefaultPricing />;
  }

  return (
    <div>
      <h1>{payload.headline}</h1>
      <p>Starting at ${payload.startingPrice}/month</p>
    </div>
  );
}
```

### Server-Side Feature Flags

```typescript
// app/api/feature/route.ts
import { PostHog } from 'posthog-node';

const posthog = new PostHog(process.env.POSTHOG_API_KEY!, {
  host: process.env.POSTHOG_HOST,
});

export async function GET(request: Request) {
  const userId = getUserId(request);

  const flagEnabled = await posthog.isFeatureEnabled('new-feature', userId);
  const variant = await posthog.getFeatureFlag('experiment', userId);

  return Response.json({ flagEnabled, variant });
}
```

## Groups (B2B Analytics)

```tsx
const posthog = usePostHog();

// Associate user with a company
posthog.group('company', 'company_123', {
  name: 'Acme Inc',
  plan: 'enterprise',
  employee_count: 50,
});

// Events now include company context
posthog.capture('feature_used', { feature: 'api' });
```

## Session Replay

Enable in PostHog dashboard and configure:

```tsx
posthog.init(POSTHOG_KEY, {
  api_host: POSTHOG_HOST,
  defaults: '2025-11-30',

  // Session replay options
  session_recording: {
    maskAllInputs: true,
    maskTextSelector: '.sensitive-data',
  },
});
```

### Manual Controls

```tsx
const posthog = usePostHog();

// Start/stop recording
posthog.startSessionRecording();
posthog.stopSessionRecording();

// Check if recording
const isRecording = posthog.sessionRecordingStarted();
```

## A/B Testing (Experiments)

```tsx
import { useFeatureFlagVariantKey, usePostHog } from '@posthog/react';

function CheckoutButton() {
  const posthog = usePostHog();
  const variant = useFeatureFlagVariantKey('checkout-button-experiment');

  const handleClick = () => {
    posthog.capture('checkout_clicked');
    // Process checkout...
  };

  if (variant === 'control') {
    return <button onClick={handleClick}>Checkout</button>;
  }

  if (variant === 'test') {
    return <button onClick={handleClick} className="cta-primary">Buy Now</button>;
  }

  return <button onClick={handleClick}>Checkout</button>;
}
```

## Server-Side (Node.js)

```bash
npm install posthog-node
```

```typescript
import { PostHog } from 'posthog-node';

const posthog = new PostHog(process.env.POSTHOG_API_KEY!, {
  host: process.env.POSTHOG_HOST,
});

// Capture event
posthog.capture({
  distinctId: 'user_123',
  event: 'api_called',
  properties: {
    endpoint: '/api/users',
    method: 'POST',
  },
});

// Identify user
posthog.identify({
  distinctId: 'user_123',
  properties: {
    email: 'user@example.com',
    plan: 'pro',
  },
});

// Shutdown (important for serverless)
await posthog.shutdown();
```

## Configuration Options

```tsx
posthog.init(POSTHOG_KEY, {
  api_host: 'https://us.i.posthog.com',
  defaults: '2025-11-30',

  // Autocapture
  autocapture: true,
  capture_pageview: 'history_change',
  capture_pageleave: true,

  // Privacy
  disable_session_recording: false,
  mask_all_text: false,
  mask_all_element_attributes: false,

  // Performance
  loaded: (posthog) => {
    // Called when PostHog is ready
  },

  // Debugging
  debug: process.env.NODE_ENV === 'development',
});
```

## Environment Variables

```bash
# Client-side
NEXT_PUBLIC_POSTHOG_KEY=phc_xxxxxxxxxxxxxx
NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com

# Or for Vite
VITE_PUBLIC_POSTHOG_KEY=phc_xxxxxxxxxxxxxx
VITE_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com

# Server-side
POSTHOG_API_KEY=phx_xxxxxxxxxxxxxx
POSTHOG_HOST=https://us.i.posthog.com
```

## Best Practices

1. **Use defaults: '2025-11-30'** - Enables modern best practices
2. **Identify early** - Call identify as soon as user logs in
3. **Use groups for B2B** - Track company-level analytics
4. **Reset on logout** - Call reset() to clear user data
5. **Use feature flag hooks** - Tracks experiment exposure automatically
6. **Avoid direct import** - Always use usePostHog hook in components
7. **Consider reverse proxy** - Reduces ad blocker interference
