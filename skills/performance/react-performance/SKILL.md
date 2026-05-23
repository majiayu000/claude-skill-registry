---
name: react-performance
description: Apply when diagnosing slow renders, optimizing list rendering, or preventing unnecessary re-renders in React applications.
version: 1.1.0
tokens: ~950
confidence: high
sources:
  - https://react.dev/learn/react-compiler
  - https://react.dev/reference/react/memo
  - https://react.dev/reference/react/useMemo
  - https://react.dev/learn/render-and-commit
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [react, performance, optimization, frontend]
---

## When to Use

Apply when diagnosing slow renders, optimizing list rendering, or preventing unnecessary re-renders in React applications.

## React Compiler (React 19+)

**React Compiler automatically handles memoization for you.** If your project uses React Compiler (React 19.2+ with compiler enabled):

- Manual `memo`, `useMemo`, and `useCallback` are often unnecessary
- The compiler automatically prevents unnecessary re-renders
- Profile first with React DevTools before adding manual optimizations
- See [React Compiler docs](https://react.dev/learn/react-compiler) for setup

**When to still use manual optimization with React Compiler:**
- Third-party libraries that require memoized props/callbacks
- Edge cases where compiler cannot optimize (check React DevTools)
- React 17-18 projects without compiler support

**Without React Compiler** (or React 17-18), use the patterns below.

## Patterns

### Pattern 1: React.memo for Pure Components
```typescript
// Source: https://react.dev/reference/react/memo
import { memo } from 'react';

interface ItemProps {
  id: string;
  title: string;
  onClick: (id: string) => void;
}

const ListItem = memo(function ListItem({ id, title, onClick }: ItemProps) {
  return <li onClick={() => onClick(id)}>{title}</li>;
});

// Only re-renders if props actually change
```

### Pattern 2: useMemo for Expensive Calculations
```typescript
// Source: https://react.dev/reference/react/useMemo
const filteredAndSorted = useMemo(() => {
  return items
    .filter(item => item.status === 'active')
    .sort((a, b) => b.priority - a.priority);
}, [items]); // Only recalculate when items change
```

### Pattern 3: useCallback for Stable Handlers
```typescript
// Source: https://react.dev/reference/react/useCallback
const handleDelete = useCallback((id: string) => {
  setItems(prev => prev.filter(item => item.id !== id));
}, []); // Stable reference, safe for memo'd children
```

### Pattern 4: Virtualization for Long Lists
```typescript
// Source: https://tanstack.com/virtual/latest
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: 400, overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize() }}>
        {virtualizer.getVirtualItems().map(row => (
          <div key={row.key} style={{ transform: `translateY(${row.start}px)` }}>
            {items[row.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Pattern 5: Lazy Loading Components
```typescript
// Source: https://react.dev/reference/react/lazy
import { lazy, Suspense } from 'react';

const HeavyChart = lazy(() => import('./HeavyChart'));

function Dashboard() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyChart data={data} />
    </Suspense>
  );
}
```

## Anti-Patterns

- **Premature optimization** - Measure first with React DevTools Profiler
- **memo everything** - Only memo components that receive same props often
- **useMemo for simple values** - Overhead > benefit for trivial calculations
- **Inline objects/arrays in JSX** - Creates new reference every render
- **Manual memo with React Compiler** - Redundant if compiler is enabled

## Verification Checklist

- [ ] Profiled with React DevTools before optimizing
- [ ] Checked if React Compiler is enabled in project
- [ ] memo'd components actually receive stable props
- [ ] Lists with 100+ items use virtualization
- [ ] Heavy components lazy loaded
- [ ] No inline object/array props to memo'd children
