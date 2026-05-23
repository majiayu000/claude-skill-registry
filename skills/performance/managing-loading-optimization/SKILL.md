---
name: managing-loading-optimization
description: Advanced code-splitting and lazy-loading techniques. Use to reduce initial bundle size and speed up the homepage.
---

# Code Splitting and Lazy Loading

## When to use this skill
- Importing heavy libraries (Charts, Leaflet Maps, Rich Text Editors).
- Loading non-critical UI (e.g., a "Support Chat" widget).

## Implementation
```tsx
import dynamic from 'next/dynamic';

const InteractiveMap = dynamic(() => import('@/components/Map'), {
    loading: () => <Skeleton className="h-[400px]" />,
    ssr: false, // Disable for browser-only libs like Leaflet
});
```

## Instructions
- **ssr: false**: Use this for components that use `window` or complex browser-only APIs.
- **Chunks**: Group related components into shared chunks if they are always used together.
- **Analysis**: Use `@next/bundle-analyzer` to identify large dependencies.
