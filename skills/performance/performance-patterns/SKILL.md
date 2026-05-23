---
name: performance-patterns
description: Web performance patterns - Core Web Vitals, code splitting, caching, and bundle optimization. Use when improving web application performance.
---

# Web Performance Patterns

## Core Web Vitals Targets

| Metric | Target | What It Measures |
|--------|--------|-----------------|
| LCP (Largest Contentful Paint) | < 2.5s | Loading performance |
| INP (Interaction to Next Paint) | < 200ms | Responsiveness |
| CLS (Cumulative Layout Shift) | < 0.1 | Visual stability |

---

## Lighter Alternatives

| Heavy | Light Alternative |
|-------|-------------------|
| moment.js (300KB) | date-fns (~5KB/fn), dayjs (2KB) |
| lodash (70KB) | Individual imports, native methods |
| axios (13KB) | fetch API (native) |

```tsx
// ❌ Imports entire library
import _ from 'lodash';

// ✅ Import only what you need
import debounce from 'lodash/debounce';
```

---

## Code Splitting

```tsx
// Route-based splitting
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));

function App() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Suspense>
  );
}

// Next.js dynamic imports
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});
```

---

## Dynamic Library Import

```tsx
// Load heavy libraries only when needed
async function generatePDF(data) {
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF();
  return doc;
}
```

---

## Layout Stability (CLS)

```tsx
// Reserve space for images
<div style={{ aspectRatio: '16/9' }}>
  <Image src={src} alt={alt} fill />
</div>

// Reserve space for dynamic content
<div style={{ minHeight: '250px' }}>
  <Suspense fallback={<Skeleton height={250} />}>
    <DynamicContent />
  </Suspense>
</div>
```

```css
/* Font loading without CLS */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;
}
```

---

## Caching with TanStack Query

```tsx
function useProducts() {
  return useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
    staleTime: 5 * 60 * 1000,   // Fresh for 5 minutes
    gcTime: 30 * 60 * 1000,     // Keep in cache 30 minutes
  });
}

// Prefetch on hover
const queryClient = useQueryClient();

const handleMouseEnter = () => {
  queryClient.prefetchQuery({
    queryKey: ['product', productId],
    queryFn: () => fetchProduct(productId),
  });
};
```

---

## Debounce Hook

```tsx
import { useMemo } from 'react';
import debounce from 'lodash/debounce';

function SearchInput() {
  const debouncedSearch = useMemo(
    () => debounce((term: string) => {
      performSearch(term);
    }, 300),
    []
  );

  return (
    <input
      onChange={(e) => debouncedSearch(e.target.value)}
      placeholder="Search..."
    />
  );
}
```

---

## Virtualization (Long Lists)

```tsx
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={400}
  itemCount={items.length}
  itemSize={35}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>{items[index].name}</div>
  )}
</FixedSizeList>
```

---

## Checklist

- [ ] Code split by route
- [ ] Lazy load below-fold content
- [ ] Use modern image formats (WebP/AVIF)
- [ ] Set image dimensions (prevent CLS)
- [ ] Replace heavy libraries with lighter alternatives
- [ ] Enable caching (TanStack Query staleTime)
- [ ] Debounce expensive operations
- [ ] Virtualize long lists
- [ ] Measure Core Web Vitals
