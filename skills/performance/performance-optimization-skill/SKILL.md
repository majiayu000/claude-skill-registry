---
name: "Performance Optimization"
description: "Optimize Next.js bundle size with code splitting, tree shaking, lazy loading, and build configuration. Apply when improving performance, reducing bundle size, analyzing dependencies, or optimizing load times."
allowed-tools: Read, Write, Edit, Bash
version: 1.0.0
---

# Performance Optimization

Systematic performance optimization for faster load times and reduced resource consumption.

## Overview

This Skill enforces:
- Code splitting and lazy loading
- Tree shaking unused code
- Bundle size analysis
- Dynamic imports
- Image optimization
- Build configuration tuning
- Compression strategies
- Caching headers

Apply when optimizing performance, reducing bundle size, or improving load times.

## Code Splitting

### Route-Based Splitting

```tsx
// Next.js automatically splits by route
app/
├── dashboard/page.tsx    // bundle-1.js
├── settings/page.tsx     // bundle-2.js
└── analytics/page.tsx    // bundle-3.js

// Only loaded when user visits that route
```

### Component-Level Splitting

```tsx
// ✅ GOOD: Lazy load heavy components
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/Chart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false  // Don't render on server
});

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <HeavyChart />  {/* Loaded only when page loads */}
    </div>
  );
}

// ❌ BAD: Import everything upfront
import { HeavyChart } from '@/components/Chart';
// Included in main bundle even if user doesn't need it
```

### Dynamic Imports

```ts
// Load module only when needed
app.get('/api/reports', async (req, res) => {
  const { generateReport } = await import('@/lib/report-generator');
  const result = await generateReport();
  res.json(result);
});

// ✅ GOOD: Module loaded only for /api/reports
// ❌ BAD: Module loaded at startup
const { generateReport } = require('@/lib/report-generator');
```

## Tree Shaking

### Configure package.json

```json
{
  "name": "myapp",
  "sideEffects": false,  // No side effects, safe to remove
  "exports": {
    ".": "./dist/index.js",
    "./utils": "./dist/utils.js"
  }
}
```

### Use Named Exports

```ts
// ✅ GOOD: Tree shakeable (named exports)
export function usedFunction() { }
export function unusedFunction() { }

// Only used functions included in bundle
import { usedFunction } from './module';

// ❌ BAD: Not tree shakeable (default export)
export default {
  usedFunction,
  unusedFunction
};

// Everything included in bundle
import module from './module';
module.usedFunction();
```

### Import Only What You Need

```ts
// ✅ GOOD: Import specific function
import { debounce } from 'lodash-es';

// ❌ BAD: Import entire library
import * as _ from 'lodash';
const debounce = _.debounce;
// Entire library included
```

## Bundle Analysis

### Analyze Bundle Size

```bash
# Install analyzer
npm install -D @next/bundle-analyzer

# Configure next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // Next.js config
});

# Analyze
ANALYZE=true npm run build
```

### Tools for Analysis

```bash
# webpack-bundle-analyzer
npm install -D webpack-bundle-analyzer

# esbuild
npm install -D esbuild

# Source map explorer
npm install -D source-map-explorer
npm run source-map-explorer 'dist/**/*.js.map'
```

## Image Optimization

### Next.js Image Component

```tsx
// ✅ GOOD: Optimized images
import Image from 'next/image';

export function UserAvatar({ src, alt }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={200}
      height={200}
      priority  // Preload critical images
      quality={80}  // 80% quality (good trade-off)
      placeholder="blur"  // Blur while loading
    />
  );
}

// ❌ BAD: Unoptimized
<img src={imageUrl} alt={alt} />
// No lazy loading, no optimization
```

### Image Formats

```tsx
// ✅ GOOD: Modern formats with fallback
<picture>
  <source srcSet={image.webp} type="image/webp" />
  <img src={image.jpg} alt="" />
</picture>

// ✅ GOOD: WebP with Next.js
<Image
  src={image}
  alt={alt}
  quality={80}
  format="webp"
/>
```

## Build Configuration

### next.config.js Optimization

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable SWC minification (faster)
  swcMinify: true,

  // Optimize packages
  optimizePackageImports: [
    '@mui/material',
    '@mui/icons-material',
    'lodash-es'
  ],

  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com'
      }
    ],
    formats: ['image/avif', 'image/webp'],
    imageSizes: [16, 32, 48, 64, 96, 128, 256],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920]
  },

  // Compression
  compress: true,

  // Generate source maps only in dev
  productionBrowserSourceMaps: false
};

module.exports = nextConfig;
```

## Lazy Loading Components

### React Suspense

```tsx
import { Suspense } from 'react';

async function SlowComponent() {
  // Simulate slow operation
  await new Promise(r => setTimeout(r, 3000));
  return <div>Loaded after 3 seconds</div>;
}

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      
      {/* Show immediately */}
      <p>Quick stats</p>
      
      {/* Lazy load with fallback */}
      <Suspense fallback={<div>Loading...</div>}>
        <SlowComponent />
      </Suspense>
    </div>
  );
}
```

### Dynamic Suspense

```tsx
import dynamic from 'next/dynamic';
import { Suspense } from 'react';

const LazyChart = dynamic(
  () => import('@/components/Chart'),
  { 
    loading: () => <div>Loading chart...</div>,
    ssr: false
  }
);

export default function Dashboard() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyChart />
    </Suspense>
  );
}
```

## Performance Metrics

### Web Vitals

```ts
// lib/web-vitals.ts
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  console.log(metric);
  // Send to analytics service
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

## Caching Strategies

### HTTP Caching Headers

```ts
// ✅ GOOD: Cache static assets long-term
response.headers.set('Cache-Control', 'public, max-age=31536000, immutable');

// ✅ GOOD: Cache HTML (revalidate frequently)
response.headers.set('Cache-Control', 'public, max-age=3600, s-maxage=3600');

// ✅ GOOD: No cache for API responses
response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate');
```

### Service Worker Caching

```ts
// lib/service-worker.ts
const CACHE_NAME = 'v1';
const urlsToCache = [
  '/',
  '/offline.html',
  '/styles/main.css',
  '/scripts/main.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

## Compression

```ts
// ✅ GOOD: Enable compression
import compression from 'compression';

app.use(compression());

// Middleware in Next.js
export async function middleware(request: NextRequest) {
  const response = NextResponse.next();
  response.headers.set('Content-Encoding', 'gzip');
  return response;
}
```

## Anti-Patterns

```ts
// ❌ BAD: Import entire library
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ GOOD: Import specific function
import { debounce } from 'lodash-es';
debounce(fn, 300);

// ❌ BAD: Large unoptimized image
<img src={largeImage} alt="" />

// ✅ GOOD: Optimized with Next.js Image
<Image src={optimizedImage} alt="" quality={80} />

// ❌ BAD: No code splitting
import * from './all-components';

// ✅ GOOD: Lazy load
const Component = dynamic(() => import('./heavy-component'));

// ❌ BAD: No caching
response.headers.set('Cache-Control', 'no-cache');

// ✅ GOOD: Cache appropriately
response.headers.set('Cache-Control', 'public, max-age=31536000');
```

## Verification Before Production

- [ ] Bundle size analyzed
- [ ] Code splitting enabled for routes
- [ ] Heavy components lazy loaded
- [ ] Tree shaking configured
- [ ] Images optimized (Next.js Image)
- [ ] Unused packages removed
- [ ] Build optimized (SWC, minification)
- [ ] Caching headers set
- [ ] Service Worker (if offline support needed)
- [ ] Web Vitals monitored

## Integration with Project Standards

Enforces performance optimization:
- Fast page loads (better UX)
- Reduced bandwidth usage
- Improved SEO (Core Web Vitals)
- Better mobile experience

## Resources

- Next.js Performance: https://nextjs.org/learn/foundation/how-nextjs-works/rendering
- Bundle Analysis: https://nextjs.org/docs/advanced-features/analyzing-bundles
- Web Vitals: https://web.dev/vitals
