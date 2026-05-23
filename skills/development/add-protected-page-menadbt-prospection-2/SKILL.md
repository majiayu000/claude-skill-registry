---
name: add-protected-page
description: Creates a protected page with Suspense loading pattern. Use when adding new pages that require authentication, creating dashboard pages, or setting up new routes.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Add Protected Page

Creates a protected page following the Suspense loading pattern with Clerk authentication.

## Structure

For a new route `/my-feature`:

```
front/
├── app/my-feature/
│   ├── page.tsx        # Auth only - wraps content in Suspense
│   └── loading.tsx     # Automatic Suspense fallback
└── components/my-feature/
    └── MyFeatureContent.tsx  # Data fetching + UI
```

## Workflow

### 1. Create Page Component

```typescript
// app/my-feature/page.tsx
'use client';

import { Suspense } from 'react';
import { useUser } from '@clerk/nextjs';
import { MyFeatureContent } from '@/components/my-feature/MyFeatureContent';

export default function MyFeaturePage() {
  const { user } = useUser();
  if (!user) return null; // REQUIRED for SSG

  return (
    <Suspense>
      <MyFeatureContent userId={user.id} />
    </Suspense>
  );
}
```

**Key Points**:
- `'use client'` directive required
- `if (!user) return null` is **MANDATORY** - prevents build errors
- Page only handles auth, wraps content in Suspense
- No data fetching here

### 2. Create Loading Fallback

```typescript
// app/my-feature/loading.tsx
import { LoadingSpinner } from '@/components/_shared/loading-spinner';

export default function Loading() {
  return <LoadingSpinner message="Loading..." />;
}
```

### 3. Create Content Component

```typescript
// components/my-feature/MyFeatureContent.tsx
'use client';

import { useMyFeatureSuspense } from '@/lib/hooks/use-my-feature';

interface MyFeatureContentProps {
  userId: string;
}

export function MyFeatureContent({ userId }: MyFeatureContentProps) {
  const { data } = useMyFeatureSuspense(userId);

  return (
    <div className="container mx-auto p-4">
      {/* Render data - no isLoading check needed! */}
      {data.map((item) => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  );
}
```

**Key Points**:
- Uses `useSuspenseQuery` - no loading states needed
- Receives `userId` as prop from page
- Pure UI rendering

### 4. Update Middleware (if new route pattern)

```typescript
// middleware.ts
const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/items(.*)',
  '/paid-feature(.*)',
  '/my-feature(.*)', // Add new route
]);
```

## Important Rules

**DO**:
- Add `if (!user) return null` in page components
- Use Suspense to wrap content
- Put data fetching in content component
- Use `useSuspenseQuery` for automatic loading states

**DO NOT**:
- Fetch data in page component
- Add manual loading states (`isLoading`)
- Forget the null check (causes build errors)
- Use `dynamic = 'force-dynamic'` (middleware handles auth)

## Creating the Feature Hook

See the `add-feature-hook` skill for creating the hook used in the content component.
