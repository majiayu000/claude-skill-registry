---
name: performance-optimization
description: Skill for performance profiling and optimization of web applications. Use when conducting Lighthouse audits, analyzing bundles, implementing code splitting, optimizing images, configuring caching strategies, or improving Core Web Vitals. Provides patterns for frontend and backend performance improvements, including browser, CDN, and server caching.
---

# Performance Optimization

Skill for profiling and optimizing web application performance.

## Overview

This skill provides guidance for:
1. **Performance Profiling** - Lighthouse, bundle analysis, profiling tools
2. **Frontend Optimization** - Code splitting, lazy loading, image optimization
3. **Caching Strategies** - Browser, CDN, server-side caching
4. **Core Web Vitals** - LCP, FID/INP, CLS optimization

## Core Web Vitals

### Metrics Overview

| Metric | Target | Description |
|--------|--------|-------------|
| LCP (Largest Contentful Paint) | < 2.5s | Time to render largest content element |
| INP (Interaction to Next Paint) | < 200ms | Responsiveness to user interactions |
| CLS (Cumulative Layout Shift) | < 0.1 | Visual stability during page load |

### Measurement Tools

```bash
# Lighthouse CLI
npx lighthouse https://example.com --output=json --output-path=./lighthouse-report.json

# Web Vitals in code
npm install web-vitals
```

```typescript
// lib/web-vitals.ts
import { onLCP, onINP, onCLS } from 'web-vitals';

export function reportWebVitals() {
  onLCP((metric) => {
    console.log('LCP:', metric.value);
    // Send to analytics
  });

  onINP((metric) => {
    console.log('INP:', metric.value);
  });

  onCLS((metric) => {
    console.log('CLS:', metric.value);
  });
}
```

## Lighthouse Audits

### Running Audits

```bash
# Full audit
npx lighthouse https://example.com --view

# Specific categories
npx lighthouse https://example.com --only-categories=performance,accessibility

# Mobile simulation
npx lighthouse https://example.com --preset=mobile

# CI integration
npx lighthouse https://example.com --budget-path=./budget.json --output=json
```

### Performance Budget

```json
// budget.json
[
  {
    "resourceSizes": [
      { "resourceType": "script", "budget": 300 },
      { "resourceType": "image", "budget": 500 },
      { "resourceType": "stylesheet", "budget": 100 },
      { "resourceType": "total", "budget": 1000 }
    ],
    "resourceCounts": [
      { "resourceType": "script", "budget": 10 },
      { "resourceType": "third-party", "budget": 5 }
    ],
    "timings": [
      { "metric": "largest-contentful-paint", "budget": 2500 },
      { "metric": "first-contentful-paint", "budget": 1500 },
      { "metric": "interactive", "budget": 3500 }
    ]
  }
]
```

### Common Lighthouse Issues and Fixes

| Issue | Impact | Fix |
|-------|--------|-----|
| Render-blocking resources | LCP | Async/defer scripts, inline critical CSS |
| Large DOM size | All | Virtualization, pagination |
| Unused JavaScript | LCP | Code splitting, tree shaking |
| Unoptimized images | LCP | Next/Image, WebP, lazy loading |
| Layout shifts | CLS | Size attributes, font-display |
| Long tasks | INP | Code splitting, web workers |

## Bundle Analysis

### Webpack Bundle Analyzer

```bash
# Install
npm install --save-dev webpack-bundle-analyzer

# Next.js configuration
npm install @next/bundle-analyzer
```

```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // Next.js config
});
```

```bash
# Run analysis
ANALYZE=true npm run build
```

### Identifying Bundle Issues

| Issue | Indicator | Solution |
|-------|-----------|----------|
| Large dependencies | Single package > 100KB | Find smaller alternative |
| Duplicate packages | Same package multiple versions | Dedupe, peer dependencies |
| Unused exports | Large modules partially used | Tree shaking, selective imports |
| Dev dependencies in prod | moment locales, lodash full | Selective imports |

### Import Optimization

```typescript
// BAD: Imports entire library
import _ from 'lodash';
const result = _.debounce(fn, 300);

// GOOD: Import only what you need
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);

// BAD: Barrel imports
import { Button, Input, Modal } from '@/components';

// GOOD: Direct imports (when barrel causes issues)
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
```

## Code Splitting Strategies

### Route-Based Splitting (Next.js)

```typescript
// Automatic with App Router - each page is a separate chunk
// app/dashboard/page.tsx - separate chunk
// app/settings/page.tsx - separate chunk
```

### Component-Based Splitting

```typescript
// Dynamic import for heavy components
import dynamic from 'next/dynamic';

// Lazy load with loading state
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Disable SSR for client-only components
});

// Conditional loading
const AdminPanel = dynamic(() => import('@/components/AdminPanel'), {
  loading: () => <div>Loading admin panel...</div>,
});

export default function Dashboard({ isAdmin }) {
  return (
    <div>
      <HeavyChart data={data} />
      {isAdmin && <AdminPanel />}
    </div>
  );
}
```

### Library Splitting

```typescript
// Lazy load heavy libraries
const loadPdfLib = () => import('pdf-lib');

async function generatePdf() {
  const { PDFDocument } = await loadPdfLib();
  const doc = await PDFDocument.create();
  // ...
}
```

## Image Optimization

### Next.js Image Component

```typescript
import Image from 'next/image';

// Responsive image with automatic optimization
export function HeroImage() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero image"
      width={1200}
      height={600}
      priority // Preload for LCP
      placeholder="blur"
      blurDataURL={blurDataUrl}
    />
  );
}

// Fill container
export function BackgroundImage() {
  return (
    <div className="relative w-full h-64">
      <Image
        src="/background.jpg"
        alt="Background"
        fill
        style={{ objectFit: 'cover' }}
        sizes="100vw"
      />
    </div>
  );
}
```

### Image Format Selection

| Format | Use Case | Browser Support |
|--------|----------|-----------------|
| WebP | General purpose, photos | Modern browsers |
| AVIF | Best compression, photos | Chrome, Firefox |
| SVG | Icons, logos, illustrations | All |
| PNG | Transparency needed | All |
| JPEG | Photos (fallback) | All |

### Responsive Images

```typescript
// next.config.js
module.exports = {
  images: {
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    formats: ['image/avif', 'image/webp'],
  },
};
```

```typescript
// Specify sizes for responsive loading
<Image
  src="/product.jpg"
  alt="Product"
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
/>
```

## Caching Strategies

### Browser Caching

```typescript
// next.config.js - Static asset caching
module.exports = {
  async headers() {
    return [
      {
        source: '/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=0, must-revalidate',
          },
        ],
      },
    ];
  },
};
```

### CDN Caching

```typescript
// API route with CDN caching
export async function GET(request: Request) {
  const data = await fetchData();

  return Response.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=300',
    },
  });
}
```

### Cache Control Headers

| Directive | Use Case |
|-----------|----------|
| `public, max-age=31536000, immutable` | Versioned static assets (CSS, JS) |
| `public, max-age=3600` | Semi-static content |
| `public, s-maxage=60, stale-while-revalidate=300` | CDN caching with background refresh |
| `private, no-cache` | User-specific data |
| `no-store` | Sensitive data |

### Server-Side Caching (FastAPI)

```python
# Redis caching for API responses
from fastapi import FastAPI
from functools import wraps
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_response(ttl_seconds: int = 300):
    """Cache decorator for API endpoints."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute and cache
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, ttl_seconds, json.dumps(result))
            return result
        return wrapper
    return decorator

@app.get("/products")
@cache_response(ttl_seconds=300)
async def get_products():
    return await product_service.get_all()
```

### Database Query Caching

```python
# SQLAlchemy query caching
from sqlalchemy import event
from functools import lru_cache

class CachedRepository:
    def __init__(self, session):
        self.session = session
        self._cache = {}

    async def get_by_id(self, entity_id: int):
        cache_key = f"entity:{entity_id}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        result = await self.session.get(Entity, entity_id)
        self._cache[cache_key] = result
        return result

    def invalidate(self, entity_id: int):
        cache_key = f"entity:{entity_id}"
        self._cache.pop(cache_key, None)
```

## Frontend Performance Patterns

### Virtualization for Long Lists

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 5,
  });

  return (
    <div ref={parentRef} className="h-96 overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              transform: `translateY(${virtualItem.start}px)`,
              height: `${virtualItem.size}px`,
            }}
          >
            {items[virtualItem.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Debouncing User Input

```typescript
import { useDeferredValue, useState } from 'react';
import { useDebouncedCallback } from 'use-debounce';

function SearchInput() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);

  // Or with explicit debounce
  const debouncedSearch = useDebouncedCallback(
    (value: string) => {
      performSearch(value);
    },
    300
  );

  return (
    <input
      value={query}
      onChange={(e) => {
        setQuery(e.target.value);
        debouncedSearch(e.target.value);
      }}
    />
  );
}
```

### Optimistic Updates

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

function TodoItem({ todo }) {
  const queryClient = useQueryClient();

  const toggleMutation = useMutation({
    mutationFn: (completed: boolean) =>
      api.updateTodo(todo.id, { completed }),

    onMutate: async (completed) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['todos'] });

      // Snapshot previous value
      const previousTodos = queryClient.getQueryData(['todos']);

      // Optimistically update
      queryClient.setQueryData(['todos'], (old: Todo[]) =>
        old.map((t) =>
          t.id === todo.id ? { ...t, completed } : t
        )
      );

      return { previousTodos };
    },

    onError: (err, completed, context) => {
      // Rollback on error
      queryClient.setQueryData(['todos'], context?.previousTodos);
    },
  });

  return (
    <input
      type="checkbox"
      checked={todo.completed}
      onChange={(e) => toggleMutation.mutate(e.target.checked)}
    />
  );
}
```

## Backend Performance Patterns

### Database Query Optimization

```python
# Eager loading to avoid N+1 queries
from sqlalchemy.orm import joinedload, selectinload

# BAD: N+1 queries
users = session.query(User).all()
for user in users:
    print(user.orders)  # Separate query for each user!

# GOOD: Eager load relationships
users = session.query(User).options(
    selectinload(User.orders)
).all()

# For nested relationships
users = session.query(User).options(
    selectinload(User.orders).selectinload(Order.items)
).all()
```

### Connection Pooling

```python
# SQLAlchemy connection pool configuration
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,           # Number of persistent connections
    max_overflow=10,        # Additional connections when pool exhausted
    pool_timeout=30,        # Timeout waiting for connection
    pool_recycle=1800,      # Recycle connections after 30 mins
    pool_pre_ping=True,     # Verify connection before use
)
```

### Async Operations

```python
from fastapi import FastAPI
import asyncio

@app.get("/dashboard")
async def get_dashboard():
    # Run independent queries concurrently
    user_data, orders, notifications = await asyncio.gather(
        get_user_profile(),
        get_recent_orders(),
        get_notifications(),
    )

    return {
        "user": user_data,
        "orders": orders,
        "notifications": notifications,
    }
```

## Performance Monitoring

### Real User Monitoring (RUM)

```typescript
// Send performance data to analytics
export function trackPagePerformance() {
  if (typeof window === 'undefined') return;

  window.addEventListener('load', () => {
    setTimeout(() => {
      const timing = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;

      const metrics = {
        dns: timing.domainLookupEnd - timing.domainLookupStart,
        tcp: timing.connectEnd - timing.connectStart,
        ttfb: timing.responseStart - timing.requestStart,
        download: timing.responseEnd - timing.responseStart,
        domInteractive: timing.domInteractive - timing.fetchStart,
        domComplete: timing.domComplete - timing.fetchStart,
        loadComplete: timing.loadEventEnd - timing.fetchStart,
      };

      // Send to analytics
      analytics.track('page_performance', metrics);
    }, 0);
  });
}
```

## Performance Optimization Checklist

### Frontend

- [ ] Lighthouse score > 90 for Performance
- [ ] LCP < 2.5s
- [ ] INP < 200ms
- [ ] CLS < 0.1
- [ ] Bundle size within budget
- [ ] Images optimized (WebP/AVIF, lazy loading)
- [ ] Critical CSS inlined
- [ ] JavaScript async/deferred
- [ ] Code splitting implemented
- [ ] Fonts optimized (font-display: swap)

### Backend

- [ ] Database queries optimized (no N+1)
- [ ] Connection pooling configured
- [ ] Caching strategy implemented
- [ ] Async operations where beneficial
- [ ] Response compression enabled
- [ ] Indexes on frequently queried columns

### Caching

- [ ] Static assets cached with long TTL
- [ ] CDN configured for static content
- [ ] API responses cached appropriately
- [ ] Cache invalidation strategy defined

## References

For detailed guidance, see:
- `references/lighthouse-guide.md` - Comprehensive Lighthouse optimization
- `references/caching-patterns.md` - Advanced caching strategies
