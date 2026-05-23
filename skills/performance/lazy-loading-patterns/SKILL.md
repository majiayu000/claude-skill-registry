---
name: lazy-loading-patterns
description: Code splitting and lazy loading with React.lazy, Suspense, route-based splitting, intersection observer, and preload strategies for optimal bundle performance
tags: [lazy-loading, code-splitting, suspense, dynamic-import, intersection-observer, preload, react-19, performance]
context: fork
agent: frontend-ui-developer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Lazy Loading Patterns

Code splitting and lazy loading patterns for React 19 applications using `React.lazy`, `Suspense`, route-based splitting, and intersection observer strategies.

## When to Use

- Reducing initial bundle size for faster page loads
- Route-based code splitting in SPAs
- Lazy loading heavy components (charts, editors, modals)
- Below-the-fold content loading
- Conditional feature loading based on user permissions
- Progressive image and media loading

## Core Patterns

### 1. React.lazy + Suspense (Standard Pattern)

```tsx
import { lazy, Suspense } from 'react';

// Lazy load component - code split at this boundary
const HeavyEditor = lazy(() => import('./HeavyEditor'));

function EditorPage() {
  return (
    <Suspense fallback={<EditorSkeleton />}>
      <HeavyEditor />
    </Suspense>
  );
}

// With named exports (requires intermediate module)
const Chart = lazy(() =>
  import('./charts').then(module => ({ default: module.LineChart }))
);
```

### 2. React 19 `use()` Hook (Modern Pattern)

```tsx
import { use, Suspense } from 'react';

// Create promise outside component
const dataPromise = fetchData();

function DataDisplay() {
  // Suspense-aware promise unwrapping
  const data = use(dataPromise);
  return <div>{data.title}</div>;
}

// Usage with Suspense
<Suspense fallback={<Skeleton />}>
  <DataDisplay />
</Suspense>
```

### 3. Route-Based Code Splitting (React Router 7.x)

```tsx
import { lazy } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router';

// Lazy load route components
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));
const Analytics = lazy(() => import('./pages/Analytics'));

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { path: 'dashboard', element: <Dashboard /> },
      { path: 'settings', element: <Settings /> },
      { path: 'analytics', element: <Analytics /> },
    ],
  },
]);

// Root with Suspense boundary
function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <RouterProvider router={router} />
    </Suspense>
  );
}
```

### 4. Intersection Observer Lazy Loading

```tsx
import { useRef, useState, useEffect, lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function LazyOnScroll({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { rootMargin: '100px' } // Load 100px before visible
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div ref={ref}>
      {isVisible ? children : <Placeholder />}
    </div>
  );
}

// Usage
<LazyOnScroll>
  <Suspense fallback={<ChartSkeleton />}>
    <HeavyComponent />
  </Suspense>
</LazyOnScroll>
```

### 5. Prefetching on Hover/Focus

```tsx
import { useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router';

function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  const queryClient = useQueryClient();

  const prefetchRoute = () => {
    // Prefetch data for the route
    queryClient.prefetchQuery({
      queryKey: ['page', to],
      queryFn: () => fetchPageData(to),
    });

    // Prefetch the component chunk
    import(`./pages/${to}`);
  };

  return (
    <Link
      to={to}
      onMouseEnter={prefetchRoute}
      onFocus={prefetchRoute}
      preload="intent" // React Router preloading
    >
      {children}
    </Link>
  );
}
```

### 6. Module Preload Hints

```html
<!-- In index.html or via helmet -->
<link rel="modulepreload" href="/assets/dashboard-chunk.js" />
<link rel="modulepreload" href="/assets/vendor-react.js" />

<!-- Prefetch for likely next navigation -->
<link rel="prefetch" href="/assets/settings-chunk.js" />
```

```tsx
// Programmatic preloading
function preloadComponent(importFn: () => Promise<any>) {
  const link = document.createElement('link');
  link.rel = 'modulepreload';
  link.href = importFn.toString().match(/import\("(.+?)"\)/)?.[1] || '';
  document.head.appendChild(link);
}
```

### 7. Conditional Loading with Feature Flags

```tsx
import { lazy, Suspense } from 'react';
import { useFeatureFlag } from '@/hooks/useFeatureFlag';

const NewDashboard = lazy(() => import('./NewDashboard'));
const LegacyDashboard = lazy(() => import('./LegacyDashboard'));

function Dashboard() {
  const useNewDashboard = useFeatureFlag('new-dashboard');

  return (
    <Suspense fallback={<DashboardSkeleton />}>
      {useNewDashboard ? <NewDashboard /> : <LegacyDashboard />}
    </Suspense>
  );
}
```

## Suspense Boundaries Strategy

```tsx
// ✅ CORRECT: Granular Suspense boundaries
function Dashboard() {
  return (
    <div className="grid grid-cols-3 gap-4">
      <Suspense fallback={<ChartSkeleton />}>
        <RevenueChart />
      </Suspense>
      <Suspense fallback={<ChartSkeleton />}>
        <UsersChart />
      </Suspense>
      <Suspense fallback={<TableSkeleton />}>
        <RecentOrders />
      </Suspense>
    </div>
  );
}

// ❌ WRONG: Single boundary blocks entire UI
function Dashboard() {
  return (
    <Suspense fallback={<FullPageSkeleton />}>
      <RevenueChart />
      <UsersChart />
      <RecentOrders />
    </Suspense>
  );
}
```

## Error Boundaries with Lazy Components

```tsx
import { Component, ErrorInfo, ReactNode } from 'react';

class LazyErrorBoundary extends Component<
  { children: ReactNode; fallback: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Lazy load failed:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

// Usage
<LazyErrorBoundary fallback={<ErrorFallback />}>
  <Suspense fallback={<Skeleton />}>
    <LazyComponent />
  </Suspense>
</LazyErrorBoundary>
```

## Bundle Analysis Integration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor splitting
          'vendor-react': ['react', 'react-dom'],
          'vendor-router': ['react-router'],
          'vendor-query': ['@tanstack/react-query'],
          // Feature splitting
          'feature-charts': ['recharts', 'd3'],
          'feature-editor': ['@tiptap/react', '@tiptap/starter-kit'],
        },
      },
    },
  },
  plugins: [
    visualizer({
      filename: 'dist/bundle-analysis.html',
      open: true,
      gzipSize: true,
    }),
  ],
});
```

## Performance Budgets

```json
// package.json
{
  "bundlesize": [
    { "path": "dist/assets/index-*.js", "maxSize": "80kb" },
    { "path": "dist/assets/vendor-react-*.js", "maxSize": "50kb" },
    { "path": "dist/assets/feature-*-*.js", "maxSize": "100kb" }
  ]
}
```

## Anti-Patterns (FORBIDDEN)

```tsx
// ❌ NEVER: Lazy load small components (< 5KB)
const Button = lazy(() => import('./Button')); // Overhead > savings

// ❌ NEVER: Missing Suspense boundary
function App() {
  const Chart = lazy(() => import('./Chart'));
  return <Chart />; // Will throw!
}

// ❌ NEVER: Lazy inside render (creates new component each render)
function App() {
  const Component = lazy(() => import('./Component')); // ❌
  return <Component />;
}

// ❌ NEVER: Lazy loading critical above-fold content
const Hero = lazy(() => import('./Hero')); // Delays LCP!

// ❌ NEVER: Over-splitting (too many small chunks)
// Each chunk = 1 HTTP request = latency overhead

// ❌ NEVER: Missing error boundary for network failures
<Suspense fallback={<Skeleton />}>
  <LazyComponent /> {/* What if import fails? */}
</Suspense>
```

## Key Decisions

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Splitting granularity | Per-component | Per-route | **Per-route** for most apps, per-component for heavy widgets |
| Prefetch strategy | On hover | On viewport | **On hover** for nav links, **viewport** for content |
| Suspense placement | Single root | Granular | **Granular** for independent loading |
| Skeleton vs spinner | Skeleton | Spinner | **Skeleton** for content, spinner for actions |
| Chunk naming | Auto-generated | Manual | **Manual** for debugging, auto for production |

## Related Skills

- `core-web-vitals` - LCP optimization through lazy loading
- `vite-advanced` - Vite code splitting configuration
- `render-optimization` - React render performance
- `react-server-components-framework` - Server-side code splitting

## Capability Details

### component-lazy-loading
**Keywords**: React.lazy, dynamic import, Suspense, code splitting
**Solves**: How to lazy load React components, reduce bundle size

### route-splitting
**Keywords**: route, code splitting, React Router, lazy routes
**Solves**: Route-based code splitting, per-page bundles

### intersection-observer
**Keywords**: scroll, viewport, lazy, IntersectionObserver, below-fold
**Solves**: Load components when scrolled into view

### suspense-patterns
**Keywords**: Suspense, fallback, boundary, skeleton, loading
**Solves**: Proper Suspense boundary placement, skeleton loading

### preloading
**Keywords**: prefetch, preload, modulepreload, hover, intent
**Solves**: Preload on hover, prefetch likely navigation

### bundle-optimization
**Keywords**: bundle, chunks, splitting, manualChunks, vendor
**Solves**: Optimize bundle splitting strategy, vendor chunks

## References

- `references/route-splitting.md` - Route-based code splitting patterns
- `references/intersection-observer.md` - Scroll-triggered lazy loading
- `templates/lazy-component.tsx` - Lazy component template
