---
name: performance-optimizer
description: |
  Optimize SvelteKit applications by leveraging SvelteKit's full-stack architecture for instant server-side rendering and progressive enhancement. Specialized in load functions, form actions, and SvelteKit's data loading patterns.

  Use when:
  - User reports slow initial page load with loading spinners
  - Page uses onMount + fetch for data fetching
  - Store patterns cause waterfall fetching
  - Need to improve SEO (content not in initial HTML)
  - Converting client-side data fetching to server-side load functions
  - Implementing progressive enhancement patterns

  Triggers: "slow loading", "optimize fetching", "SSR data", "SvelteKit optimization",
  "remove loading spinner", "server-side fetch", "convert to load function", "progressive enhancement",
  "data fetch lambat", "loading lama"
---

# SvelteKit Performance Optimizer

Optimize SvelteKit applications by leveraging the framework's full-stack capabilities for instant server-side rendering and progressive enhancement.

## Quick Diagnosis

Search for these anti-patterns in the codebase:

```bash
# Find client-side fetching patterns
rg -n "onMount.*fetch|\$state.*loading|writable\(\)" --type svelte
rg -n "fetch\(" src/routes/ --type svelte
rg -n "export let data" src/routes/ --type svelte
```

**Red flags:**
- `onMount` + `fetch()` = slow initial load
- `$state(true)` for `isLoading` = user sees spinner
- `writable()` or `derived` for initial page data = waterfall fetching
- Missing `export let data` in page components = not using load functions

## 3-Step Conversion Workflow

### Step 1: Identify Data Requirements

Determine what data the page needs on initial render:
- Static/rarely-changing data → **Universal Load Function** (SSR + CSR)
- User-interactive data (filters, search) → **Form Actions + Client-side Actions**
- Real-time data → **Server-Sent Events or WebSockets**

### Step 2: Extract Interactive Sections

Move sections with `on:viewportenter`, `$state`, `on:click` to separate components while preserving SvelteKit patterns:

```svelte
<!-- src/lib/components/DataSection.svelte -->
<script lang="ts">
  export let data: Item[];  // Receive data as props from load function

  import { onMount } from 'svelte';
  import { scrollReveal } from '$lib/actions/scrollReveal.js';
  import { fly, fade } from 'svelte/transition';

  let element: HTMLElement;
  let isVisible = false;

  // Client-side animation with Svelte patterns
  onMount(() => {
    scrollReveal(element);
  });
</script>

<div
  bind:this={element}
  transition:fly={{ y: 20 }}
  class:visible={isVisible}
>
  {#each data as item}
    <div transition:fade>
      {item.content}
    </div>
  {/each}
</div>
```

### Step 3: Implement SvelteKit Load Functions

```svelte
<!-- src/routes/+page.svelte -->
<script lang="ts">
  import DataSection from '$lib/components/DataSection.svelte';
  import type { PageData } from './$types';

  export let data: PageData;  // Data from universal load function
</script>

<DataSection {data} />

<!-- Optional: Progressive enhancement form -->
<form method="POST" action="?/submit">
  <input name="message" />
  <button type="submit">Submit</button>
</form>
```

```typescript
// src/routes/+page.server.ts
import { getData } from '$lib/server/data';
import type { PageServerLoad, Actions } from './$types';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ url }) => {
  const data = await getData();  // Fetch on server
  return { data };
};

export const actions: Actions = {
  default: async ({ request }) => {
    const formData = await request.formData();
    const message = formData.get('message');

    if (!message) {
      return fail(400, { message: 'Message is required' });
    }

    // Process data...
    return { success: true };
  }
};
```

## Type Adapter Pattern with SvelteKit

When DB types differ from frontend types:

```typescript
// src/lib/server/adapters.ts
import type { Item as DBItem } from "$lib/server/database.types";
import type { Item } from "$lib/types";

export function adaptDBToFrontend(db: DBItem): Item {
  return {
    id: db.id,
    name: db.name,
    description: db.description ?? "",
    createdAt: new Date(db.created_at),
  };
}

// src/routes/+page.server.ts
import { getItems } from '$lib/server/items';
import { adaptDBToFrontend } from '$lib/server/adapters';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, url, cookies }) => {
  const dbItems = await getItems();
  const items = dbItems.map(adaptDBToFrontend);

  return {
    items,
    // Additional SvelteKit-specific data
    search: url.searchParams.get('search') || '',
    user: cookies.get('user') ? JSON.parse(cookies.get('user')) : null
  };
};

// src/routes/+page.ts for universal load
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ parent, url }) => {
  const parentData = await parent();
  const clientData = await getClientOnlyData();

  return {
    ...parentData,
    clientData
  };
};
```

## When to Use Hybrid Patterns

Keep client-side fetching when:
- Real-time subscriptions (Supabase realtime, WebSockets)
- User-triggered fetching (search, filters, pagination) - use form actions
- Data depends on client state (auth token, localStorage) - use universal load functions
- Infinite scroll / load more patterns - use load functions with pagination

**Best practice:** Use SvelteKit's progressive enhancement - server-side load + client-side enhancement

## Advanced SvelteKit Patterns

See [references/patterns.md](references/patterns.md) for:
- Parallel data fetching with Promise.all in load functions
- Streaming with SvelteKit streaming responses and deferred loading
- Error handling with +error.svelte pages and form validation
- Caching strategies with cache headers and `depends()`
- Hybrid SSR + client patterns with form actions and progressive enhancement
- Route protection with `+layout.server.ts` hooks
- Database transactions with form actions
- Real-time updates with server-sent events

