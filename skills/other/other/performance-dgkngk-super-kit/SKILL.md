---
name: performance
description: Performance profiling, optimization techniques, and caching strategies. Use when diagnosing slow applications, improving Core Web Vitals, or optimizing database queries and bundle size.
---

# Performance Optimization Skill

## Overview
Performance profiling, optimization techniques, and caching strategies.

## Core Web Vitals

### LCP (Largest Contentful Paint) < 2.5s
```typescript
// Optimize images
<Image
  src="/hero.jpg"
  alt="Hero"
  priority  // Preload
  sizes="100vw"
  placeholder="blur"
/>

// Preload critical resources
<link rel="preload" href="/fonts/inter.woff2" as="font" crossOrigin="" />
```

### CLS (Cumulative Layout Shift) < 0.1
```css
/* Reserve space for images */
img {
  aspect-ratio: 16 / 9;
  width: 100%;
  height: auto;
}

/* Skeleton loaders */
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  animation: shimmer 1.5s infinite;
}
```

### INP (Interaction to Next Paint) < 200ms
```typescript
// Defer non-critical work
import { startTransition } from 'react';

startTransition(() => {
  setExpensiveState(newValue);
});

// Use web workers for heavy computation
const worker = new Worker('/heavy-task.js');
worker.postMessage(data);
```

## JavaScript Optimization

### Code Splitting
```typescript
// Dynamic imports
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Route-based splitting (Next.js does this automatically)
import dynamic from 'next/dynamic';
const Chart = dynamic(() => import('./Chart'), { ssr: false });
```

### Bundle Analysis
```bash
# Next.js
npx @next/bundle-analyzer

# Webpack
npx webpack-bundle-analyzer stats.json
```

### Tree Shaking
```typescript
// ❌ Import entire library
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ Import specific function
import debounce from 'lodash/debounce';
debounce(fn, 300);
```

## Caching Strategies

### HTTP Caching
```typescript
// Static assets (1 year)
Cache-Control: public, max-age=31536000, immutable

// API responses (5 minutes with revalidation)
Cache-Control: public, max-age=300, stale-while-revalidate=60
```

### React Query / SWR
```typescript
const { data } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
  staleTime: 5 * 60 * 1000, // 5 minutes
  cacheTime: 30 * 60 * 1000, // 30 minutes
});
```

### Service Worker
```typescript
// Cache-first strategy for static assets
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => {
      return cached || fetch(event.request);
    })
  );
});
```

## Database Query Optimization
```sql
-- Add indexes
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at DESC);

-- Avoid N+1
SELECT posts.*, users.name 
FROM posts 
JOIN users ON posts.user_id = users.id;

-- Use EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = 123;
```
