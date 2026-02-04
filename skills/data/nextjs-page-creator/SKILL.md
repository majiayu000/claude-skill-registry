---
name: nextjs-page-creator
description: Creates Next.js 16 App Router pages with loading and error states. Use when asked to create new routes, pages, or views.
allowed-tools: Read, Write, Edit, Glob
context: fork
---

# Next.js 16 Page Creation Skill

## When to Use

Use this skill when the user asks to:

- Create a new page or route
- Add a new view to the application
- Set up page with loading/error states

## Critical: Next.js 16 Params Pattern

**In Next.js 15+, params are promises and MUST be awaited:**

```typescript
// ✅ CORRECT - Await params
export default async function Page(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;
  const { id } = params;
  // ... use id
}

// ❌ WRONG - Will cause runtime errors
export default async function Page({ params }: { params: { id: string } }) {
  const { id } = params; // ERROR: params is a Promise!
}
```

## Process

1. **Check existing patterns** in `app/` directory
2. **Create page.tsx** with async Server Component
3. **Create loading.tsx** with Skeleton components from shadcn/ui
4. **Create error.tsx** with proper error boundary

## Template: page.tsx

```typescript
import { Metadata } from 'next';
import { auth } from '@/lib/auth/config';
import { redirect } from 'next/navigation';

export const metadata: Metadata = {
  title: 'Page Title | Elon AI',
  description: 'Description',
};

interface PageProps {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ [key: string]: string | undefined }>;
}

export default async function PageName(props: PageProps) {
  const session = await auth();
  if (!session?.user) redirect('/auth/login');

  const params = await props.params;
  const { id } = params;

  // Fetch data with tenant scoping
  const data = await getData(id, session.user.tenantId);

  return (
    <div className="container py-8">
      {/* Page content */}
    </div>
  );
}
```

## Template: loading.tsx

```typescript
import { Skeleton } from '@/components/ui/skeleton';

export default function Loading() {
  return (
    <div className="container py-8 space-y-4">
      <Skeleton className="h-8 w-64" />
      <Skeleton className="h-64 w-full" />
    </div>
  );
}
```

## Template: error.tsx

```typescript
'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import Link from 'next/link';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="container py-8">
      <Card className="max-w-md mx-auto">
        <CardHeader>
          <CardTitle className="text-destructive">Something went wrong</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">
            We couldn't load this page. Please try again.
          </p>
          <div className="flex gap-2">
            <Button onClick={reset}>Try Again</Button>
            <Button variant="outline" asChild>
              <Link href="/dashboard">Go to Dashboard</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

## Checklist

- [ ] Page uses async Server Component
- [ ] Params awaited before use
- [ ] Session checked and tenant scoped
- [ ] loading.tsx created
- [ ] error.tsx created
- [ ] Uses shadcn/ui components
- [ ] WCAG AA accessible
- [ ] Mobile responsive
