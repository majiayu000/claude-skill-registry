---
name: web-frontend
description: Next.js App Router, Server/Client components, shadcn/ui patterns, Tailwind CSS conventions
---

# Web Frontend Skill

## Core Principles

1. **Server Components by Default** - Use Client Components only when needed (hooks, events, browser APIs)
2. **Type-Safe API Calls** - Always use tRPC for data fetching
3. **Semantic Colors** - Use design tokens from globals.css
4. **Form Validation** - React Hook Form + Zod for complex forms
5. **Protected Routes** - Wrap authenticated pages with AuthGuard
6. **Error Boundaries** - Use error.tsx for automatic error handling

## Patterns to Follow

### Pattern 1: Server vs Client Component Decision

**Decision Tree**:

```
Does it use hooks? (useState, useEffect, etc.) → Client Component
Does it handle events? (onClick, onChange, etc.) → Client Component
Does it use browser APIs? (window, localStorage, etc.) → Client Component
Does it use third-party client libraries? → Client Component
Otherwise → Server Component (default)
```

**Examples**:

```tsx
// ✅ Server Component - Data fetching
export default async function ActivityPage({
  params,
}: {
  params: { id: string };
}) {
  const supabase = createClient();
  const { data: activity } = await supabase
    .from("activities")
    .select("*")
    .eq("id", params.id)
    .single();

  return <ActivityDetail activity={activity} />;
}

// ✅ Client Component - Interactive
("use client");

export function ActivityChart({ data }: Props) {
  const [metric, setMetric] = useState("heartRate");

  return (
    <div>
      <select onChange={(e) => setMetric(e.target.value)}>
        <option value="heartRate">Heart Rate</option>
      </select>
      <Chart data={data} metric={metric} />
    </div>
  );
}
```

### Pattern 2: tRPC Query Integration

**When to use**: Client-side data fetching
**Why**: Type-safe, automatic cache management

```tsx
"use client";

import { trpc } from "@/lib/trpc";

export function ActivitiesList() {
  const { data, isLoading, error, refetch } = trpc.activities.list.useQuery(
    { limit: 20, offset: 0 },
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  );

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorAlert message={error.message} />;

  return (
    <div>
      {data?.map((activity) => (
        <ActivityCard key={activity.id} activity={activity} />
      ))}
    </div>
  );
}
```

### Pattern 3: tRPC Mutation with Optimistic Updates

**When to use**: Create/update/delete operations
**Why**: Instant UI feedback, automatic rollback on error

```tsx
const utils = trpc.useUtils();

const mutation = trpc.activities.update.useMutation({
  onMutate: async (updatedActivity) => {
    await utils.activities.list.cancel();
    const previousActivities = utils.activities.list.getData();

    utils.activities.list.setData(undefined, (old) =>
      old?.map((act) =>
        act.id === updatedActivity.id ? { ...act, ...updatedActivity } : act,
      ),
    );

    return { previousActivities };
  },
  onError: (err, vars, context) => {
    utils.activities.list.setData(undefined, context?.previousActivities);
  },
  onSettled: () => {
    utils.activities.list.invalidate();
  },
});
```

### Pattern 4: Complex Forms with React Hook Form

**When to use**: Forms with validation, field arrays, dynamic fields
**Why**: Type-safe, automatic error handling, Zod integration

```tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { activitySchema } from "@repo/core/schemas";

export function ActivityForm() {
  const form = useForm({
    resolver: zodResolver(activitySchema),
    defaultValues: { name: "", type: "run", distance: 0 },
  });

  const mutation = trpc.activities.create.useMutation({
    onSuccess: () => toast.success("Activity created"),
    onError: (error) => {
      if (error.data?.zodError) {
        const fieldErrors = error.data.zodError.fieldErrors;
        Object.entries(fieldErrors).forEach(([field, messages]) => {
          form.setError(field as any, { message: messages?.[0] });
        });
      }
    },
  });

  return (
    <form onSubmit={form.handleSubmit((data) => mutation.mutate(data))}>
      <input {...form.register("name")} />
      {form.formState.errors.name && (
        <span className="text-destructive">
          {form.formState.errors.name.message}
        </span>
      )}
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Creating..." : "Create"}
      </button>
    </form>
  );
}
```

### Pattern 5: Protected Routes with AuthGuard

**When to use**: Dashboard pages, user-specific content
**Why**: Automatic redirect to login, loading states

```tsx
// Layout for protected routes
export default function DashboardLayout({ children }: Props) {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-background">
        <Sidebar />
        <main className="ml-64">{children}</main>
      </div>
    </AuthGuard>
  );
}

// AuthGuard component
("use client");

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { data: session, isLoading } = useSession();

  if (isLoading) return <LoadingScreen />;
  if (!session) redirect("/login");

  return <>{children}</>;
}
```

### Pattern 6: shadcn/ui Component Usage

**When to use**: UI components needing consistent styling
**Why**: Pre-styled, accessible, customizable

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

<Card>
  <CardHeader>
    <CardTitle>Activity Details</CardTitle>
  </CardHeader>
  <CardContent>
    <Button variant="default">Save</Button>
    <Button variant="outline">Cancel</Button>
  </CardContent>
</Card>;
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Using Hooks in Server Components

```tsx
// ❌ BAD
export default function Page() {
  const [state, setState] = useState(0); // Error!
  return <div>{state}</div>;
}

// ✅ CORRECT
("use client");

export default function Page() {
  const [state, setState] = useState(0);
  return <div>{state}</div>;
}
```

### Anti-Pattern 2: Fetching Data in Client Components

```tsx
// ❌ BAD
"use client";

export default function Page() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/api/data")
      .then((r) => r.json())
      .then(setData);
  }, []);
}

// ✅ CORRECT - Use tRPC
("use client");

export default function Page() {
  const { data } = trpc.getData.useQuery();
}

// ✅ OR use Server Component
export default async function Page() {
  const data = await fetchData();
  return <ClientComponent data={data} />;
}
```

### Anti-Pattern 3: Ignoring Cache Invalidation

```tsx
// ❌ BAD
const mutation = trpc.activities.create.useMutation({
  onSuccess: () => {
    toast.success("Created");
    // Forgot to invalidate cache!
  },
});

// ✅ CORRECT
const utils = trpc.useUtils();

const mutation = trpc.activities.create.useMutation({
  onSuccess: () => {
    utils.activities.list.invalidate();
    toast.success("Created");
  },
});
```

## File Organization

```
apps/web/
├── app/
│   ├── (marketing)/       # Public pages
│   │   ├── page.tsx       # Landing page
│   │   └── _layout.tsx
│   ├── (dashboard)/       # Protected dashboard
│   │   ├── activities/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   └── _layout.tsx
│   ├── api/               # API routes
│   └── globals.css
├── components/
│   ├── ui/                # shadcn/ui components
│   └── shared/            # Shared components
└── lib/
    ├── trpc.ts            # tRPC client
    └── utils.ts
```

## Naming Conventions

- **Components**: `PascalCase` → `ActivityCard.tsx`
- **Utilities**: `camelCase` → `formatDate.ts`
- **Hooks**: `camelCase` with `use` → `useAuth.ts`
- **Route Segments**: `kebab-case` → `activity-detail/`
- **API Routes**: `kebab-case` → `webhook-handler/`

## Common Scenarios

### Scenario 1: Create Protected Dashboard Page

```tsx
// app/(dashboard)/activities/page.tsx
import { AuthGuard } from "@/components/AuthGuard";
import { ActivitiesList } from "@/components/ActivitiesList";

export default function ActivitiesPage() {
  return (
    <AuthGuard>
      <div className="container py-8">
        <h1 className="text-3xl font-bold mb-6">Activities</h1>
        <ActivitiesList />
      </div>
    </AuthGuard>
  );
}
```

### Scenario 2: OAuth Callback Handler

```tsx
// app/api/auth/callback/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const code = request.nextUrl.searchParams.get("code");

  if (!code) {
    return NextResponse.redirect("/login?error=no_code");
  }

  // Exchange code for tokens
  const tokens = await exchangeCodeForTokens(code);

  // Store tokens
  await storeTokens(userId, tokens);

  return NextResponse.redirect("/dashboard");
}
```

## Dependencies

**Required**:

- `next` v15+
- `react` v19+
- `@tanstack/react-query` v5
- `@trpc/client`, `@trpc/server`, `@trpc/react-query`
- `tailwindcss` v4
- `zod`

**Optional**:

- `react-hook-form` + `@hookform/resolvers`
- `sonner` (toast notifications)

## Testing Requirements

- Test Server Components with async data
- Test Client Components with React Testing Library
- Mock tRPC with msw-trpc
- Test forms with user event simulation
- Test error boundaries

## Checklist

- [ ] "use client" directive on interactive components
- [ ] tRPC queries for data fetching
- [ ] Cache invalidation on mutations
- [ ] Protected routes wrapped with AuthGuard
- [ ] Forms use React Hook Form + Zod
- [ ] Error boundaries implemented
- [ ] Loading states handled
- [ ] Semantic colors from design tokens

## Related Skills

- [Backend Skill](./backend-skill.md) - tRPC router patterns
- [Core Package Skill](./core-package-skill.md) - Zod schemas
- [Testing Skill](./testing-skill.md) - Web testing patterns

## Version History

- **1.0.0** (2026-01-21): Initial version

---

**Next Review**: 2026-02-21
