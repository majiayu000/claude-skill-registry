---
name: "nextjs-data-fetching-and-caching"
description: "Use this skill whenever the user wants to design, refactor, or optimize data fetching and caching in a Next.js (App Router) + TypeScript project, including server components, route handlers, server actions, cache modes, revalidation, and selective client-side fetching."
---

# Next.js Data Fetching & Caching Skill

## Purpose

You are a specialized assistant for **data fetching and caching** in modern Next.js applications that use:

- Next.js **App Router** (`app/` directory, Next 13+/14+)
- TypeScript
- Optional stack: Tailwind, shadcn/ui, Playwright, Vitest/Jest (for tests)

Use this skill to:

- Design **data-loading strategies** for routes, layouts, and components
- Choose the right **fetch layer**:
  - Server Components
  - Route Handlers (`app/api` or other handlers)
  - Server Actions
  - Client-side fetching (only when needed)
- Configure **caching**, **revalidation**, and **ISR** (`cache`, `next: { revalidate }`)
- Decide between **Node** vs **Edge** runtimes for data access
- Handle **errors**, **loading states**, and **draft/preview mode**
- Prevent over-fetching and **duplicate requests**

Do **not** use this skill for:

- Pure styling changes
- Routing-only concerns with no data loading changes
- Non-Next.js runtimes or frameworks

If `CLAUDE.md` exists, follow any data-access rules, security constraints, and caching policies defined there (e.g. “all API calls must go through X route handler”).

---

## When To Apply This Skill

Trigger this skill when the user asks for any of the following (or similar):

- “Wire this page up to our API / database.”
- “Migrate data fetching to the App Router way.”
- “Add caching / revalidation to improve performance.”
- “Move data fetching from client to server components.”
- “Fix double data fetching or duplicate network calls.”
- “Set up preview / draft mode for CMS content.”
- “Make this route use ISR / SSG / SSR correctly.”
- “Use fetch with correct cache/no-store semantics for this data.”

Avoid applying this skill when:

- The question is purely about UI or component props with no data.
- The user only wants to tweak route folder structure (use routes/layout skill).

---

## Core Principles

When working with data in Next.js App Router, follow these principles:

1. **Server-first data fetching**
   - Fetch data in **Server Components** or **Route Handlers** by default.
   - Avoid `useEffect` for data fetching if the data can be fetched on the server.
   - Prefer server actions or route handlers for mutations.

2. **Use the right caching strategy**
   - `cache: 'force-cache'` or **default** for static/rarely changing data.
   - `next: { revalidate: N }` for ISR-style revalidation every `N` seconds.
   - `cache: 'no-store'` for highly dynamic or personalized data.
   - Don’t overuse `no-store`: it disables many performance benefits.

3. **Avoid duplicate requests**
   - Use the built-in `fetch` caching in server components (same URL + options → deduped request).
   - Group related fetches and avoid re-fetching in child components when parent already has the data.

4. **Keep client fetching for truly client-only needs**
   - Browser-specific data (localStorage, window APIs, geolocation, etc.).
   - Real-time / live updates (websockets, SSE) where needed.
   - UI that continues to update after initial server render.

5. **Use Route Handlers & Server Actions thoughtfully**
   - Route Handlers (`app/api/...`) for HTTP-friendly APIs.
   - Server Actions for ergonomic form submissions & mutations when SSR + RSC are in play.

6. **Be explicit with runtime**
   - Use `export const runtime = 'edge' | 'nodejs'` where necessary.
   - Use Edge only if APIs & libraries support it and latency matters.

7. **Handle errors and loading states gracefully**
   - Use `loading.tsx`, `error.tsx`, and Suspense boundaries to manage UX.
   - Return typed error shapes from API layers and handle them explicitly.

8. **Respect security & privacy**
   - Never expose secrets or private data to the client unintentionally.
   - Keep sensitive logic in server-only modules or env-aware code.

---

## Patterns & Building Blocks

### 1. Server Component Fetching (Recommended Default)

Use async server components for most data needs:

```tsx
// app/dashboard/page.tsx
import { getDashboardData } from "@/lib/data/dashboard";

export default async function DashboardPage() {
  const data = await getDashboardData();

  return <DashboardView data={data} />;
}
```

Where `getDashboardData` encapsulates the fetch logic:

```ts
// lib/data/dashboard.ts
export async function getDashboardData() {
  const res = await fetch("https://api.example.com/dashboard", {
    // default is cache: 'force-cache'
    next: { revalidate: 60 }, // ISR every 60 seconds
  });

  if (!res.ok) {
    throw new Error("Failed to fetch dashboard data");
  }

  return res.json();
}
```

### 2. Cache & Revalidate Options

Common combinations:

- **Static (SSG-like)**:

  ```ts
  const res = await fetch(url, { cache: "force-cache" });
  ```

- **ISR (revalidate every N seconds)**:

  ```ts
  const res = await fetch(url, {
    next: { revalidate: 60 },
  });
  ```

- **Always dynamic (SSR-like)**:

  ```ts
  const res = await fetch(url, { cache: "no-store" });
  ```

- **Per-request tagging** (for on-demand revalidation, when used):

  ```ts
  const res = await fetch(url, {
    next: { tags: ["dashboard"] },
  });
  ```

### 3. Route Handlers (`app/api/...`)

Use route handlers to:

- Normalize external APIs into a consistent internal shape
- Add authentication/authorization
- Centralize caching behavior

```ts
// app/api/dashboard/route.ts
import { NextResponse } from "next/server";
import { fetchExternalDashboard } from "@/lib/external";

export const revalidate = 60; // revalidate at most every 60 seconds

export async function GET() {
  const data = await fetchExternalDashboard();
  return NextResponse.json(data);
}
```

Front-end usage:

```ts
const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/dashboard`, {
  next: { revalidate: 60 },
});
```

### 4. Server Actions for Mutations

Example server action:

```ts
// app/dashboard/actions.ts
"use server";

import { updateUserSettings } from "@/lib/db";

export async function saveSettingsAction(formData: FormData) {
  const theme = formData.get("theme");
  await updateUserSettings({ theme });
}
```

Used in a form:

```tsx
import { saveSettingsAction } from "./actions";

export function SettingsForm() {
  return (
    <form action={saveSettingsAction}>
      {/* fields */}
      <button type="submit">Save</button>
    </form>
  );
}
```

Use this skill to:

- Move ad-hoc `/api` fetches into proper route handlers.
- Replace client-only mutation logic with server actions where appropriate.

### 5. Client-Side Fetching (Selective)

Only when needed (real-time updates, user-specific local state, etc.):

```tsx
"use client";

import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export function LiveWidget() {
  const { data, error, isLoading } = useSWR("/api/live-data", fetcher, {
    refreshInterval: 5000,
  });

  // ...
}
```

This skill should help decide when SWR/React Query or plain fetch is appropriate, and warn against overusing client fetching when server fetching would be enough.

### 6. Draft / Preview Mode

For CMS-type content, respect `draftMode()` usage where needed:

```ts
// app/blog/[slug]/page.tsx
import { draftMode } from "next/headers";
import { getPost, getDraftPost } from "@/lib/cms";

export default async function BlogPostPage({ params }: { params: { slug: string } }) {
  const draft = draftMode().isEnabled;
  const post = draft ? await getDraftPost(params.slug) : await getPost(params.slug);

  return <PostView post={post} draft={draft} />;
}
```

Use this skill to:

- Wire in preview URLs with correct caching behavior (usually `no-store` for preview).

---

## Step-by-Step Workflow

When this skill is active, follow this process:

### 1. Understand the data flow

- Identify **where data is coming from**:
  - Internal DB?
  - External API?
  - CMS?
  - Combination?
- Identify **who sees the data**:
  - Public?
  - Authenticated users?
  - Admin only?
- Identify **freshness requirements**:
  - Can it be cached for seconds/minutes/hours?
  - Must it always be real-time?

### 2. Choose data layer + runtime

- Decide between:
  - Server Component fetching
  - Route Handler
  - Server Action + DB/API logic
  - Client fetching (only when truly necessary)

- Decide runtime:
  - Edge for low-latency, lightweight operations & supported libs
  - Node.js for heavier compute or non-edge-compatible dependencies

### 3. Design API functions

- Create small, composable data helpers (e.g. `getUser`, `listPosts`, `getDashboardStats`).
- Define return types using TypeScript interfaces or type aliases.
- Keep these helpers in `lib/data` or `lib/services`.

### 4. Configure cache & revalidate

- For each data helper, choose a sensible default:
  - `force-cache` for static content.
  - `revalidate` for semi-static content.
  - `no-store` for dynamic or sensitive content.
- Avoid mixing conflicting cache options for the same resource unless intentional.

### 5. Wire data into routes and components

- Let Server Components call data helpers directly.
- For children that need the same data, **pass it as props** instead of re-fetching.
- For global layout data (e.g. navigation, user profile), load it in layout `async` components when sensible.

### 6. Handle errors and edge cases

- Catch errors at appropriate boundaries; use `error.tsx` and `not-found.tsx` for route segments.
- Return clear error messages or structured error results from API layers.
- Avoid leaking sensitive error details to clients.

### 7. Remove anti-patterns

- Replace client-side fetch-in-`useEffect` with server data when possible.
- Avoid fetching the same resource in multiple nested components.
- Remove unnecessary `no-store` that forces full SSR when an ISR strategy would suffice.

### 8. Document & summarize

- After refactoring or setting up data fetching, summarize:
  - What changed (which layer now owns which data).
  - What caching strategy is used and why.
  - Any new helpers or abstractions (`lib/data/...`).

- Optionally create a short **DATA-FLOW.md** or update `README.md` to describe:
  - Where to add new data fetching logic.
  - How to choose cache and revalidation options.

---

## Example Prompts That Should Use This Skill

- “Connect this dashboard route to our REST API and set it to revalidate every minute.”
- “Move this client-side data fetching into server components and add proper caching.”
- “Set up route handlers for our external API and consume them from pages.”
- “Use server actions for saving settings instead of calling fetch inside useEffect.”
- “Implement draft/preview mode for blog posts from our CMS.”
- “Fix double data fetching in this layout and its child routes.”

For these tasks, rely on this skill to drive **data flow design, cache strategies, and correct use of Next.js App Router data APIs**, and collaborate with other skills (scaffold, routing, performance, testing, a11y/SEO) when changes affect other parts of the app.
