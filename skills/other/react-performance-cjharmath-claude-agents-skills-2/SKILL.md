---
name: react-performance
description: Performance optimization for React web applications. Use when optimizing renders, implementing virtualization, memoizing components, or debugging performance issues.
---

# React Performance (Web)

## Problem Statement

React performance issues often stem from unnecessary re-renders, unoptimized lists, and expensive computations on the main thread. Understanding React's rendering behavior is key to building performant applications.

---

## Pattern: Memoization

### useMemo - Expensive Computations

```typescript
// ✅ CORRECT: Memoize expensive calculation
const sortedAndFilteredItems = useMemo(() => {
  return items
    .filter(item => item.active)
    .sort((a, b) => b.score - a.score)
    .slice(0, 100);
}, [items]);

// ❌ WRONG: Recalculates every render
const sortedAndFilteredItems = items
  .filter(item => item.active)
  .sort((a, b) => b.score - a.score);

// ❌ WRONG: Memoizing simple access (overhead > benefit)
const userName = useMemo(() => user.name, [user.name]);
```

**When to use useMemo:**
- Array transformations (filter, sort, map chains)
- Object creation passed to memoized children
- Computations with O(n) or higher complexity

### useCallback - Stable Function References

```typescript
// ✅ CORRECT: Stable callback for child props
const handleClick = useCallback((id: string) => {
  setSelectedId(id);
}, []);

// Pass to memoized child
<MemoizedItem onClick={handleClick} />

// ❌ WRONG: useCallback with unstable deps
const handleClick = useCallback((id: string) => {
  doSomething(unstableObject); // unstableObject changes every render
}, [unstableObject]); // Defeats the purpose
```

**When to use useCallback:**
- Callbacks passed to memoized children
- Callbacks in dependency arrays
- Event handlers that would cause child re-renders

---

## Pattern: React.memo

```typescript
// Wrap components that receive stable props
const ItemCard = memo(function ItemCard({
  item,
  onSelect
}: Props) {
  return (
    <div onClick={() => onSelect(item.id)}>
      <h3>{item.name}</h3>
      <p>{item.price}</p>
    </div>
  );
});

// Custom comparison for complex props
const ItemCard = memo(
  function ItemCard({ item, onSelect }: Props) {
    // ...
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (skip re-render)
    return (
      prevProps.item.id === nextProps.item.id &&
      prevProps.item.price === nextProps.item.price
    );
  }
);
```

**When to use React.memo:**
- List item components
- Components receiving stable primitive props
- Components that render frequently but rarely change

**When NOT to use:**
- Components that always receive new props
- Simple components (overhead > benefit)
- Root-level pages

---

## Pattern: List Virtualization

For long lists, render only visible items using react-window or react-virtualized.

```typescript
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }: { items: Item[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      <ItemCard item={items[index]} />
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      width="100%"
      itemCount={items.length}
      itemSize={80}
    >
      {Row}
    </FixedSizeList>
  );
}

// Variable height items
import { VariableSizeList } from 'react-window';

function VariableList({ items }: { items: Item[] }) {
  const getItemSize = (index: number) => {
    return items[index].expanded ? 200 : 80;
  };

  return (
    <VariableSizeList
      height={600}
      width="100%"
      itemCount={items.length}
      itemSize={getItemSize}
    >
      {Row}
    </VariableSizeList>
  );
}
```

**When to virtualize:**
- Lists with 100+ items
- Complex item components
- Scrollable containers with many children

---

## Pattern: Zustand Selector Optimization

**Problem:** Selecting entire store causes re-render on any state change.

```typescript
// ❌ WRONG: Re-renders on ANY store change
const store = useAppStore();
// or
const { items, loading, filters, ... } = useAppStore();

// ✅ CORRECT: Only re-renders when selected values change
const items = useAppStore((s) => s.items);
const loading = useAppStore((s) => s.loading);

// ✅ CORRECT: Multiple values with shallow comparison
import { useShallow } from 'zustand/react/shallow';

const { items, loading } = useAppStore(
  useShallow((s) => ({
    items: s.items,
    loading: s.loading
  }))
);
```

---

## Pattern: Avoiding Re-Renders

### Object/Array Stability

```typescript
// ❌ WRONG: New object every render
<ChildComponent style={{ padding: 10 }} />
<ChildComponent config={{ enabled: true }} />

// ✅ CORRECT: Stable reference
const style = useMemo(() => ({ padding: 10 }), []);
const config = useMemo(() => ({ enabled: true }), []);

<ChildComponent style={style} />
<ChildComponent config={config} />

// ✅ CORRECT: Or define outside component
const style = { padding: 10 };

function Parent() {
  return <ChildComponent style={style} />;
}
```

### Children Stability

```typescript
// ❌ WRONG: Inline function creates new element each render
<Parent>
  {() => <Child />}
</Parent>

// ✅ CORRECT: Stable element
const child = useMemo(() => <Child />, [deps]);
<Parent>{child}</Parent>
```

---

## Pattern: Code Splitting

```typescript
import { lazy, Suspense } from 'react';

// Lazy load components
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}

// Named exports
const Dashboard = lazy(() =>
  import('./pages/Dashboard').then(module => ({
    default: module.Dashboard
  }))
);
```

---

## Pattern: Debouncing and Throttling

```typescript
import { useMemo } from 'react';
import { debounce, throttle } from 'lodash-es';

// Debounce - wait until user stops typing
function SearchInput({ onSearch }: { onSearch: (query: string) => void }) {
  const debouncedSearch = useMemo(
    () => debounce(onSearch, 300),
    [onSearch]
  );

  return (
    <input
      type="text"
      onChange={(e) => debouncedSearch(e.target.value)}
    />
  );
}

// Throttle - limit how often function runs
function InfiniteScroll({ onLoadMore }: { onLoadMore: () => void }) {
  const throttledLoad = useMemo(
    () => throttle(onLoadMore, 1000),
    [onLoadMore]
  );

  useEffect(() => {
    const handleScroll = () => {
      if (nearBottom()) {
        throttledLoad();
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [throttledLoad]);

  return <div>...</div>;
}
```

---

## Pattern: Image Optimization

```typescript
// Lazy load images
<img
  src={imageUrl}
  loading="lazy"
  alt="Description"
/>

// With intersection observer for more control
function LazyImage({ src, alt }: { src: string; alt: string }) {
  const [isVisible, setIsVisible] = useState(false);
  const imgRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { rootMargin: '100px' }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <div ref={imgRef}>
      {isVisible ? (
        <img src={src} alt={alt} />
      ) : (
        <div className="placeholder" />
      )}
    </div>
  );
}

// Next.js Image component (if using Next.js)
import Image from 'next/image';

<Image
  src={imageUrl}
  alt="Description"
  width={400}
  height={300}
  placeholder="blur"
  blurDataURL={blurHash}
/>
```

---

## Pattern: Web Workers for Heavy Computation

```typescript
// worker.ts
self.onmessage = (e: MessageEvent<{ data: number[] }>) => {
  const result = heavyComputation(e.data.data);
  self.postMessage(result);
};

// Component
function DataProcessor({ data }: { data: number[] }) {
  const [result, setResult] = useState(null);

  useEffect(() => {
    const worker = new Worker(new URL('./worker.ts', import.meta.url));

    worker.onmessage = (e) => {
      setResult(e.data);
    };

    worker.postMessage({ data });

    return () => worker.terminate();
  }, [data]);

  return result ? <Results data={result} /> : <Loading />;
}
```

---

## Pattern: Detecting Re-Renders

### React DevTools Profiler

1. Open React DevTools
2. Go to Profiler tab
3. Click record, interact, stop
4. Review "Flamegraph" for render times
5. Look for components rendering unnecessarily

### why-did-you-render

```typescript
// Setup in development
import React from 'react';

if (process.env.NODE_ENV === 'development') {
  const whyDidYouRender = require('@welldone-software/why-did-you-render');
  whyDidYouRender(React, {
    trackAllPureComponents: true,
  });
}

// Mark specific component for tracking
ItemCard.whyDidYouRender = true;
```

### Console Logging

```typescript
// Quick check for re-renders
function ItemCard({ item }: Props) {
  console.log('ItemCard render:', item.id);
  // ...
}
```

---

## Performance Checklist

Before shipping:

- [ ] Large lists are virtualized
- [ ] List items are memoized with `React.memo`
- [ ] Callbacks passed to items use `useCallback`
- [ ] Zustand selectors are specific (not whole store)
- [ ] Images use lazy loading
- [ ] Heavy routes are code-split
- [ ] No inline object/function props to memoized children
- [ ] Profiler shows no unnecessary re-renders

---

## Common Issues

| Issue | Solution |
|-------|----------|
| List scroll lag | Virtualize list, memoize items |
| Component re-renders too often | Check selector specificity, memoize props |
| Slow initial render | Code split, reduce bundle size |
| Memory growing | Check for event listener cleanup, state accumulation |
| UI freezes on interaction | Move computation to web worker or defer |

---

## Relationship to Other Skills

- **react-zustand-patterns**: Selector optimization patterns
- **react-async-patterns**: Proper async handling prevents re-render loops
