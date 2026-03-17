---
name: plausible
description: Implements privacy-friendly web analytics with Plausible as a Google Analytics alternative. Use when adding lightweight, cookie-free analytics that are GDPR compliant without consent banners.
---

# Plausible Analytics

Lightweight, open source, privacy-friendly Google Analytics alternative. Cookie-free, GDPR compliant, and under 1KB script size.

## Quick Start - Script Tag

```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

## NPM Package

```bash
npm install @plausible-analytics/tracker
```

### Basic Setup

```typescript
import Plausible from '@plausible-analytics/tracker';

const plausible = Plausible({
  domain: 'yourdomain.com',
});

// Enable automatic pageview tracking
plausible.enableAutoPageviews();
```

## Next.js Integration

### App Router

```tsx
// app/layout.tsx
import Script from 'next/script';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <Script
          defer
          data-domain="yourdomain.com"
          src="https://plausible.io/js/script.js"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### With next-plausible Package

```bash
npm install next-plausible
```

```tsx
// app/layout.tsx
import PlausibleProvider from 'next-plausible';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <PlausibleProvider domain="yourdomain.com" />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

## Custom Events

### Script Tag Method

```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>

<script>
window.plausible = window.plausible || function() {
  (window.plausible.q = window.plausible.q || []).push(arguments);
};
</script>

<button onclick="plausible('Signup')">Sign Up</button>
```

### NPM Package

```typescript
import Plausible from '@plausible-analytics/tracker';

const plausible = Plausible({
  domain: 'yourdomain.com',
});

// Track custom event
plausible.trackEvent('signup', {
  props: {
    plan: 'pro',
    source: 'homepage',
  },
});

// Track with callback
plausible.trackEvent('purchase', {
  props: { product: 'Widget' },
  callback: () => {
    console.log('Event tracked successfully');
  },
});
```

### With next-plausible

```tsx
'use client';

import { usePlausible } from 'next-plausible';

function SignupButton() {
  const plausible = usePlausible();

  const handleSignup = () => {
    plausible('signup', {
      props: { plan: 'pro' },
    });
    // Continue with signup...
  };

  return <button onClick={handleSignup}>Sign Up</button>;
}
```

## Revenue Tracking

Track ecommerce revenue with custom events.

```typescript
plausible.trackEvent('purchase', {
  revenue: {
    amount: 49.99,
    currency: 'USD',
  },
  props: {
    product_id: 'prod_123',
    product_name: 'Premium Widget',
  },
});
```

### With HTML

```html
<button onclick="plausible('purchase', {
  revenue: { amount: 49.99, currency: 'USD' },
  props: { product: 'Widget' }
})">
  Buy Now
</button>
```

## Configuration Options

```typescript
const plausible = Plausible({
  domain: 'yourdomain.com',
  trackLocalhost: false,      // Track localhost (for dev)
  apiHost: 'https://plausible.io',  // Your Plausible host
  hashMode: false,            // Track hash changes
});

// Enable features
plausible.enableAutoPageviews();
plausible.enableAutoOutboundTracking();  // Track outbound links
```

## Script Variants

Plausible offers different script variants for additional features.

### Outbound Link Tracking

```html
<script defer data-domain="yourdomain.com"
  src="https://plausible.io/js/script.outbound-links.js"></script>
```

### File Downloads

```html
<script defer data-domain="yourdomain.com"
  src="https://plausible.io/js/script.file-downloads.js"></script>
```

### Hash-based Routing

```html
<script defer data-domain="yourdomain.com"
  src="https://plausible.io/js/script.hash.js"></script>
```

### All Extensions

```html
<script defer data-domain="yourdomain.com"
  src="https://plausible.io/js/script.outbound-links.file-downloads.hash.js"></script>
```

## Custom Properties (Pageview)

Track custom properties with every pageview.

### NPM Package

```typescript
const plausible = Plausible({
  domain: 'yourdomain.com',
});

// Set custom properties for all pageviews
plausible.enableAutoPageviews({
  customProperties: () => ({
    author: 'John Doe',
    logged_in: 'true',
  }),
});
```

### Script Tag

```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.pageview-props.js"></script>

<script>
window.plausible = window.plausible || function() {
  (window.plausible.q = window.plausible.q || []).push(arguments);
};

// Track pageview with custom props
plausible('pageview', { props: { author: 'John Doe' } });
</script>
```

## SPA Support

Plausible works automatically with pushState-based routers. For manual control:

```typescript
const plausible = Plausible({
  domain: 'yourdomain.com',
});

// Manual pageview tracking
plausible.trackPageview({
  url: window.location.href,
  referrer: document.referrer,
});

// With custom properties
plausible.trackPageview({
  url: '/blog/article-1',
  props: {
    category: 'technology',
  },
});
```

## Proxy Setup (Avoid Blockers)

Proxy Plausible through your own domain to avoid ad blockers.

### Next.js Rewrites

```javascript
// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/js/script.js',
        destination: 'https://plausible.io/js/script.js',
      },
      {
        source: '/api/event',
        destination: 'https://plausible.io/api/event',
      },
    ];
  },
};
```

```html
<script defer data-domain="yourdomain.com"
  data-api="/api/event"
  src="/js/script.js"></script>
```

### Vercel Edge Config

```javascript
// vercel.json
{
  "rewrites": [
    {
      "source": "/js/script.js",
      "destination": "https://plausible.io/js/script.js"
    },
    {
      "source": "/api/event",
      "destination": "https://plausible.io/api/event"
    }
  ]
}
```

## Server-Side Events API

Send events from your server without JavaScript.

```typescript
// app/api/track/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const { name, url, props } = await request.json();

  await fetch('https://plausible.io/api/event', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': request.headers.get('user-agent') || '',
      'X-Forwarded-For': request.headers.get('x-forwarded-for') || '',
    },
    body: JSON.stringify({
      domain: 'yourdomain.com',
      name,
      url,
      props,
    }),
  });

  return NextResponse.json({ success: true });
}
```

## React Component

```tsx
'use client';

import { useEffect } from 'react';
import Plausible from '@plausible-analytics/tracker';

const plausible = Plausible({
  domain: 'yourdomain.com',
});

export function PlausibleProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    plausible.enableAutoPageviews();
  }, []);

  return <>{children}</>;
}

// Hook for tracking events
export function usePlausible() {
  return {
    trackEvent: (name: string, props?: Record<string, string>) => {
      plausible.trackEvent(name, { props });
    },
  };
}
```

## TypeScript

```typescript
import Plausible from '@plausible-analytics/tracker';

type PlausibleEvents = {
  signup: { plan: string; source: string };
  purchase: { product_id: string; amount: number };
  download: { file: string };
};

const plausible = Plausible({
  domain: 'yourdomain.com',
});

function trackEvent<K extends keyof PlausibleEvents>(
  name: K,
  props: PlausibleEvents[K]
) {
  plausible.trackEvent(name, { props });
}

// Type-safe event tracking
trackEvent('signup', { plan: 'pro', source: 'homepage' });
trackEvent('purchase', { product_id: 'prod_123', amount: 49.99 });
```

## Self-Hosting

Plausible can be self-hosted using Docker.

```typescript
const plausible = Plausible({
  domain: 'yourdomain.com',
  apiHost: 'https://analytics.yourdomain.com',
});
```

```html
<script defer data-domain="yourdomain.com"
  src="https://analytics.yourdomain.com/js/script.js"></script>
```

## Best Practices

1. **Use script tag for simplicity** - Smallest payload
2. **Proxy through your domain** - Avoids ad blockers
3. **Track meaningful events** - Focus on conversions
4. **Use revenue tracking** - For ecommerce
5. **No consent banner needed** - Cookie-free by design
6. **Consider self-hosting** - For full data ownership
