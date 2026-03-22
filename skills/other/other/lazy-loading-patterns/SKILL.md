---
name: lazy-loading-patterns
description: >
  Implement lazy loading and code splitting to reduce initial bundle size and improve
  load times. Activate whenever the user works on bundle optimization, asks about code
  splitting, implements dynamic imports, uses React.lazy or Suspense, sets up route-based
  splitting, or optimizes image loading with intersection observer.
---

# Lazy Loading Patterns

Load code and assets only when needed. Reduce initial bundle size to improve Time to
Interactive and First Contentful Paint. Split by route, by component, and by visibility.

## When to Use
- Initial page load is slow due to large JavaScript bundle
- Components are below the fold or behind user interaction
- Routes have heavy dependencies not needed on every page
- Images or media dominate page weight
- Third-party libraries are used on specific pages only

## Core Patterns

### Route-Based Code Splitting (React)

Split your bundle by route so users only download code for the page they visit.

```typescript
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Each lazy() call creates a separate chunk
const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));
const AdminPanel = lazy(() => import('./pages/AdminPanel'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageSkeleton />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

// Skeleton loader instead of spinner for better perceived performance
function PageSkeleton() {
  return (
    <div className="animate-pulse space-y-4 p-6">
      <div className="h-8 bg-gray-200 rounded w-1/3" />
      <div className="h-4 bg-gray-200 rounded w-2/3" />
      <div className="h-4 bg-gray-200 rounded w-1/2" />
    </div>
  );
}
```

### Component-Level Lazy Loading

Defer loading of heavy components until they are needed.

```typescript
import { lazy, Suspense, useState } from 'react';

// Heavy components loaded on demand
const MarkdownEditor = lazy(() => import('./components/MarkdownEditor'));
const ChartDashboard = lazy(() => import('./components/ChartDashboard'));
function DocumentPage({ doc }: { doc: Document }) {
  const [isEditing, setIsEditing] = useState(false);
  return (
    <div>
      <h1>{doc.title}</h1>
      {isEditing ? (
        <Suspense fallback={<div>Loading editor...</div>}>
          <MarkdownEditor content={doc.content} />
        </Suspense>
      ) : (
        <button onClick={() => setIsEditing(true)}>Edit</button>
      )}
    </div>
  );
}
```

### Dynamic Imports (Framework-Agnostic)

Use dynamic `import()` to load modules on demand in any JavaScript environment.

```typescript
// Load a heavy library only when needed
async function generatePDF(data: ReportData): Promise<Blob> {
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF();
  doc.text(data.title, 10, 10);
  // ... build PDF
  return doc.output('blob');
}

// Webpack magic comments for prefetching/preloading
const Settings = lazy(() =>
  import(/* webpackPrefetch: true */ './pages/Settings') // Download during idle
);
const Dashboard = lazy(() =>
  import(/* webpackPreload: true */ './pages/Dashboard') // Download immediately
);
```

### Intersection Observer for Visibility-Based Loading

Load content when it scrolls into the viewport.

```typescript
import { useEffect, useRef, useState } from 'react';

function useIntersectionObserver(
  options: IntersectionObserverInit = {}
): [React.RefObject<HTMLDivElement>, boolean] {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.unobserve(element); // Only trigger once
        }
      },
      { rootMargin: '200px', ...options } // Start loading 200px before visible
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  return [ref, isVisible];
}

// Usage: lazy-load a heavy section
function AnalyticsSection({ userId }: { userId: string }) {
  const [ref, isVisible] = useIntersectionObserver();

  return (
    <div ref={ref}>
      {isVisible ? (
        <Suspense fallback={<SectionSkeleton />}>
          <ChartDashboard userId={userId} />
        </Suspense>
      ) : (
        <SectionSkeleton />
      )}
    </div>
  );
}
```

### Image Lazy Loading

Defer image loading until they approach the viewport.

```typescript
// Native lazy loading (simplest approach)
function ImageGallery({ images }: { images: ImageData[] }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {images.map(img => (
        <img
          key={img.id}
          src={img.url}
          alt={img.alt}
          loading="lazy"           // Native browser lazy loading
          decoding="async"         // Non-blocking decode
          width={img.width}        // Prevent layout shift
          height={img.height}
        />
      ))}
    </div>
  );
}

// Next.js: use priority={true} for above-the-fold LCP images,
// default lazy loading for everything else.
```

### Bundle Analysis

Identify what to split by analyzing your bundle composition.

```bash
# Webpack bundle analyzer
npx webpack-bundle-analyzer dist/stats.json

# Next.js bundle analysis
ANALYZE=true npm run build

# Vite bundle visualization
npx vite-bundle-visualizer

# Check individual import costs
npx import-cost  # VS Code extension shows inline import sizes
```

```typescript
// Identify heavy imports to split
// BEFORE: Everything in main bundle
import { Chart } from 'chart.js';          // ~200KB
import { marked } from 'marked';           // ~50KB
import { highlight } from 'highlight.js';  // ~300KB

// AFTER: Loaded on demand
const loadChart = () => import('chart.js').then(m => m.Chart);
const loadMarked = () => import('marked').then(m => m.marked);
```

## Anti-Patterns
- Lazy loading components that are always visible above the fold
- Creating too many tiny chunks (excessive HTTP requests)
- Not providing width/height on images (causes layout shift)
- Using `loading="lazy"` on the hero/LCP image (delays critical content)
- Wrapping every component in Suspense instead of grouping related components
- Lazy loading tiny modules (< 5KB) where the overhead exceeds the savings
- Not preloading chunks that are very likely needed next (e.g., next step in a wizard)

## Quick Reference

| Technique | When to Use | Savings |
|-----------|-------------|---------|
| Route splitting | Always, for multi-page apps | 30-70% initial bundle |
| Component splitting | Heavy components behind interaction | Per-component basis |
| Dynamic import | Conditional features, large libraries | Library size |
| Image lazy loading | Below-the-fold images | Bandwidth, LCP |
| Intersection Observer | Content sections below viewport | Per-section basis |
| Prefetch | Links user is likely to click | Perceived latency |

| Tool | Purpose |
|------|---------|
| `React.lazy` + `Suspense` | React component code splitting |
| `import()` | Dynamic module loading (any JS) |
| `loading="lazy"` | Native browser image lazy loading |
| `IntersectionObserver` | Visibility-based triggering |
