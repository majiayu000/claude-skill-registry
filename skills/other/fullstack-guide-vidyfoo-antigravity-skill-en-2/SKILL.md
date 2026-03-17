---
name: fullstack-guide
description: 全栈开发规范百科全书 (React/TS/Node/Supabase). Modern patterns including Suspense, lazy loading, useSuspenseQuery, file organization with features directory, performance optimization, and TypeScript best practices. Use when creating components, pages, features, fetching data, styling, routing, or working with frontend/backend code.
---

# Frontend Development Guidelines

## Purpose

Comprehensive guide for modern React development, emphasizing Suspense-based data fetching, lazy loading, proper file organization, and performance optimization.

## When to Use This Skill

- Creating new components or pages
- Building new features
- Fetching data with TanStack Query
- Setting up routing with TanStack Router
- Styling components with MUI v7
- Performance optimization
- Organizing frontend code
- TypeScript best practices

---

## Quick Start

### New Component Checklist

Creating a component? Follow this checklist:

- [ ] Use `React.FC<Props>` pattern with TypeScript
- [ ] Lazy load if heavy component: `React.lazy(() => import())`
- [ ] Wrap in `<SuspenseLoader>` for loading states
- [ ] Use `useSuspenseQuery` for data fetching
- [ ] Import aliases (@/, ~types, ~components)
- [ ] Event handlers with `useCallback`
- [ ] No early returns for loading states

---

## Core Patterns

### Component Pattern

```typescript
import React, { useState, useCallback } from 'react';
import { Box, Paper } from '@mui/material';
import { useSuspenseQuery } from '@tanstack/react-query';
import { featureApi } from '../api/featureApi';
import type { FeatureData } from '~types/feature';

interface MyComponentProps {
    id: number;
    onAction?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ id, onAction }) => {
    const [state, setState] = useState<string>('');

    const { data } = useSuspenseQuery({
        queryKey: ['feature', id],
        queryFn: () => featureApi.getFeature(id),
    });

    const handleAction = useCallback(() => {
        setState('updated');
        onAction?.();
    }, [onAction]);

    return (
        <Box sx={{ p: 2 }}>
            <Paper sx={{ p: 3 }}>
                {/* Content */}
            </Paper>
        </Box>
    );
};

export default MyComponent;
```

### Data Fetching

```typescript
// Use useSuspenseQuery - No isLoading checks needed!
const { data } = useSuspenseQuery({
    queryKey: ['myEntity', id],
    queryFn: () => myFeatureApi.getEntity(id),
});

// data is ALWAYS defined (Suspense handles loading)
```

### Lazy Loading

```typescript
// Lazy load heavy components
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

// Wrap in SuspenseLoader
<SuspenseLoader>
    <HeavyComponent />
</SuspenseLoader>
```

---

## Anti-Patterns

### ❌ NEVER

- Early returns for loading states (causes layout shift)
- Use `any` type
- Use `makeStyles` or `styled()` (use `sx` prop)
- Use `react-toastify` (use `useMuiSnackbar`)
- Direct API calls for auth (use `useAuth` hook)

### ✅ ALWAYS

- `React.FC<Props>` with TypeScript
- `useSuspenseQuery` for data fetching
- Suspense boundaries for loading states
- MUI v7 `sx` prop for styling
- Import type for type imports

---

## File Organization

### features/ Directory

For domain-specific features with own logic and API:

```
features/
  my-feature/
    api/
      myFeatureApi.ts
    components/
      MyFeatureMain.tsx
    hooks/
      useMyFeature.ts
    types/
      index.ts
    index.ts
```

### components/ Directory

For truly reusable UI components:

```
components/
  SuspenseLoader/
  CustomAppBar/
  ErrorBoundary/
```

---

## Resource Files

| Topic | File |
|-------|------|
| Common patterns | [common-patterns.md](resources/common-patterns.md) |
| Component patterns | [component-patterns.md](resources/component-patterns.md) |
| Data fetching | [data-fetching.md](resources/data-fetching.md) |
| File organization | [file-organization.md](resources/file-organization.md) |
| Loading and errors | [loading-and-error-states.md](resources/loading-and-error-states.md) |
| Routing guide | [routing-guide.md](resources/routing-guide.md) |
| Styling guide | [styling-guide.md](resources/styling-guide.md) |
| TypeScript standards | [typescript-standards.md](resources/typescript-standards.md) |

---

## Related Skills

- **frontend-design**: Visual design and aesthetics
- **backend-dev-guidelines**: Backend API patterns that frontend consumes

---

**Skill Status**: COMPLETE ✅
**Line Count**: < 500 ✅
**Progressive Disclosure**: 8 resource files ✅
