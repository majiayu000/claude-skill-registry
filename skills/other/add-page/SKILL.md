---
name: add-page
description: Create a Next.js 15 App Router page with Server/Client split
---

# Add Page Skill

Create a new Next.js 15 App Router page in the x4-mono web app.

## Arguments

The user describes the page. If unclear, ask for:

- Page name/path (e.g., `/settings`, `/projects/[id]`)
- Route group: `(auth)` (public) or `(dashboard)` (requires login)
- Server or Client component (default: Client if it uses tRPC hooks)
- Data requirements (which tRPC procedures to call)

## File Location

Pages go in `apps/web/src/app/{route-group}/{path}/page.tsx`.

Examples:

- `/settings` → `apps/web/src/app/(dashboard)/settings/page.tsx`
- `/projects/[id]` → `apps/web/src/app/(dashboard)/projects/[id]/page.tsx`
- `/login` → `apps/web/src/app/(auth)/login/page.tsx`

## Client Page Template (most common)

Reference: `apps/web/src/app/(dashboard)/projects/page.tsx`

```tsx
'use client';

import { trpc } from '@x4/shared/api-client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function MyPage() {
  const { data, isLoading, error } = trpc.routerName.list.useQuery({
    limit: 20,
    offset: 0,
  });

  if (isLoading) {
    return <div className="flex items-center justify-center p-8">Loading...</div>;
  }

  if (error) {
    return <div className="text-destructive p-8">Error: {error.message}</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">Page Title</h1>
        <Button>Action</Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {data?.items.map((item) => (
          <Card key={item.id}>
            <CardHeader>
              <CardTitle>{item.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">{item.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
```

## Server Page Template (no client state needed)

```tsx
// No 'use client' directive

export default async function MyPage() {
  // Server-side data fetching if needed
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold">Page Title</h1>
      {/* Static or server-rendered content */}
    </div>
  );
}
```

## Dynamic Route Page

```tsx
'use client';

import { useParams } from 'next/navigation';
import { trpc } from '@x4/shared/api-client';

export default function DetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data, isLoading } = trpc.routerName.get.useQuery({ id });
  // ...
}
```

## Layout (optional, for shared UI in a section)

```tsx
export default function SectionLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="max-w-4xl mx-auto">
      <nav>{/* Section navigation */}</nav>
      {children}
    </div>
  );
}
```

## Conventions

- **Imports**: `@x4/shared/*` for cross-package, `@/*` for intra-workspace
- **Styling**: Tailwind v4 classes only — no CSS modules
- **Components**: shadcn/ui from `@/components/ui/`
- **Data**: tRPC hooks from `@x4/shared/api-client`
- **File naming**: kebab-case directories, `page.tsx` is the convention

## Workflow

1. Determine route group (`(auth)` or `(dashboard)`)
2. Create directory structure: `apps/web/src/app/{group}/{path}/`
3. Create `page.tsx` with appropriate template
4. Optionally create `layout.tsx` if the section needs shared UI
5. Verify the page renders: `bun turbo dev` and visit the URL
6. Run `bun turbo type-check` to verify
