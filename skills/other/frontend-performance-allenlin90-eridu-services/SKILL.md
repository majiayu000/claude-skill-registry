---
name: frontend-performance
description: Provides performance optimization patterns for React applications. This skill should be used when optimizing bundle size, implementing code splitting, reducing re-renders, or improving web vitals.
---

# Frontend Performance

This skill provides patterns for optimizing React application performance.

## Canonical Examples

Study these real implementations:
- **Code Splitting**: [router.tsx](../../../apps/erify_studios/src/router.tsx)
- **Lazy Loading**: Route-level lazy loading with TanStack Router

---

## Core Optimization Strategies

### 1. Code Splitting & Lazy Loading

**Route-level code splitting** (automatic with TanStack Router):

```typescript
// Routes are automatically code-split
export const Route = createFileRoute('/studios/$studioId/tasks')({
  component: TasksPage,  // Automatically lazy-loaded
});
```

**Component-level lazy loading**:

```typescript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function Page() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### 2. Memoization

**useMemo for expensive computations**:

```typescript
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

**useCallback for stable function references**:

```typescript
const handleClick = useCallback(
  (id: string) => { updateItem(id); },
  [updateItem]
);
```

**React.memo for component memoization**:

```typescript
export const ItemCard = React.memo(({ item }: ItemCardProps) => {
  return <div>{item.name}</div>;
});
```

### 3. Virtual Scrolling

For long lists (>100 items), use `@tanstack/react-virtual`:

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 100,
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <ItemCard item={items[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 4. Image Optimization

```tsx
// Use native lazy loading
<img src={url} loading="lazy" alt={alt} />

// Use responsive images
<img
  srcSet={`${url}-small.jpg 400w, ${url}-medium.jpg 800w, ${url}-large.jpg 1200w`}
  sizes="(max-width: 640px) 400px, (max-width: 1024px) 800px, 1200px"
  src={url}
  alt={alt}
/>
```

### 5. Bundle Size Optimization

**Analyze bundle**:
```bash
npm run build -- --analyze
```

**Tree-shaking**: Import only what you need:
```typescript
// ✅ GOOD: Named imports
import { Button } from '@eridu/ui';

// ❌ BAD: Default imports from barrel files
import * as UI from '@eridu/ui';
```

---

## Performance Checklist

- [ ] Routes are code-split (automatic with TanStack Router)
- [ ] Heavy components use `lazy()` + `Suspense`
- [ ] Expensive computations use `useMemo`
- [ ] Callbacks use `useCallback` when passed to memoized children
- [ ] List items use `React.memo`
- [ ] Long lists (>100 items) use virtual scrolling
- [ ] Images use `loading="lazy"`
- [ ] Bundle analyzed and optimized
- [ ] Tree-shaking enabled (named imports)

---

## Related Skills

- [frontend-tech-stack](../frontend-tech-stack/SKILL.md) - Tech stack configuration
- [studio-list-pattern](../studio-list-pattern/SKILL.md) - Infinite scroll patterns
