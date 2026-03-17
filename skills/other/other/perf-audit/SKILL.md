---
skill: perf-audit
description: Profile and optimize React application performance
arguments: optional specific area to focus on
---

# Performance Audit

Profile the application and identify optimization opportunities.

## Process

### 1. Measure Baseline

**Build analysis:**
```bash
npm run build
# Check output size
ls -la .next/static/chunks/*.js | head -20
```

**Bundle analysis (if available):**
```bash
ANALYZE=true npm run build
```

### 2. Identify Issues

**Common performance problems:**

| Issue | Symptom | Detection |
|-------|---------|-----------|
| Large bundles | Slow initial load | Build output size |
| Unnecessary re-renders | Laggy UI | React DevTools Profiler |
| Memory leaks | Growing memory | Chrome DevTools Memory |
| Slow API calls | Loading spinners | Network tab |
| Layout thrashing | Janky scrolling | Performance tab |

### 3. Analyze Components

Look for:
- Components re-rendering when they shouldn't
- Missing memoization
- Inline function/object creation in render
- Large lists without virtualization

### 4. Apply Optimizations

**Memoization:**
```tsx
// Memoize expensive components
const MemoizedComponent = React.memo(Component);

// Memoize expensive calculations
const expensiveValue = useMemo(() => compute(data), [data]);

// Memoize callbacks
const handleClick = useCallback(() => { ... }, [deps]);
```

**Code splitting:**
```tsx
// Dynamic imports
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Spinner />,
});
```

**Image optimization:**
```tsx
import Image from 'next/image';
<Image src={src} alt={alt} width={w} height={h} />
```

**List virtualization:**
```tsx
import { FixedSizeList } from 'react-window';
```

### 5. Measure Improvement

Re-run baseline measurements and compare.

### 6. Report

Document:
- Issues found
- Optimizations applied
- Before/after metrics
- Remaining opportunities

## Quick Wins

1. **Add `loading="lazy"` to images below fold**
2. **Use `next/dynamic` for heavy components**
3. **Add `React.memo` to list item components**
4. **Move static data outside components**
5. **Use `useMemo` for filtered/sorted lists**

## Tools

- React DevTools Profiler
- Chrome DevTools Performance tab
- Lighthouse (in Chrome DevTools)
- `@next/bundle-analyzer`
- `why-did-you-render` library
