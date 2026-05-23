---
name: rsc-data-optimizer
description: |
  Optimize Next.js App Router data fetching by converting slow client-side 
  fetching to fast server-side fetching using React Server Components (RSC).
  
  Use when:
  - User reports slow initial page load with loading spinners
  - Page uses useEffect + useState for data fetching
  - StoreContext/useStore pattern causes waterfall fetching
  - Need to improve SEO (content not in initial HTML)
  - Converting "use client" pages to Server Components
  
  Triggers: "slow loading", "optimize fetching", "SSR data", "RSC optimization",
  "remove loading spinner", "server-side fetch", "convert to server component",
  "data fetch lambat", "loading lama"
---

# RSC Data Fetching Optimizer

Optimize slow client-side data fetching to instant server-side rendering.

## Quick Diagnosis

Search for these anti-patterns in the codebase:

```bash
# Find client-side fetching patterns
rg -n "useEffect.*fetch|useState.*loading|useStore\(\)" --type tsx
rg -n '"use client"' app/ --type tsx
```

**Red flags:**
- `"use client"` + `useEffect` + `fetch()` = slow initial load
- `useState(true)` for `isLoading` = user sees spinner
- `useStore()` or `useContext` for initial page data = waterfall fetching

## 3-Step Conversion Workflow

### Step 1: Identify Data Requirements

Determine what data the page needs on initial render:
- Static/rarely-changing data → **Server Component** (SSR)
- User-interactive data (filters, search) → **Client Component**

### Step 2: Extract Interactive Sections

Move sections with `useInView`, `useState`, `onClick` to separate Client Components:

```tsx
// components/data-section.tsx
"use client";

interface DataSectionProps {
  data: Item[];  // Receive data as props
}

export function DataSection({ data }: DataSectionProps) {
  const [ref, inView] = useInView();  // Client-side animation OK
  return <div ref={ref}>...</div>;
}
```

### Step 3: Convert Page to Server Component

```tsx
// app/page.tsx - NO "use client"
import { getData } from "@/lib/actions/data";
import { DataSection } from "@/components/data-section";

export default async function Page() {
  const data = await getData();  // Fetch on server
  return <DataSection data={data} />;
}
```

## Type Adapter Pattern

When DB types differ from frontend types:

```tsx
import type { Item as DBItem } from "@/lib/database.types";
import type { Item } from "@/lib/types";

function adaptDBToFrontend(db: DBItem): Item {
  return {
    id: db.id,
    name: db.name,
    description: db.description ?? "",
    createdAt: new Date(db.created_at),
  };
}

export default async function Page() {
  const dbItems = await getItems();
  const items = dbItems.map(adaptDBToFrontend);
  return <ItemList items={items} />;
}
```

## When to Keep Client-Side

Keep `"use client"` when:
- Real-time subscriptions (Supabase realtime)
- User-triggered fetching (search, filters, pagination)
- Data depends on client state (auth token, localStorage)
- Infinite scroll / load more patterns

## Advanced Patterns

See [references/patterns.md](references/patterns.md) for:
- Parallel data fetching
- Streaming with Suspense
- Error boundaries
- Caching strategies
- Hybrid SSR + client patterns
