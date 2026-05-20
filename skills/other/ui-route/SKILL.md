---
name: ui-route
description: Create SvelteKit routes and Svelte 5 components for the Traceway UI. Use when building new pages, components, or frontend features.
metadata:
  author: traceway
  version: "1.0.0"
---

# Create UI Route or Component

Use this skill when the user asks to add a new page, route, or component to the SvelteKit frontend.

## Creating a new route

Routes live in `ui/src/routes/`. SvelteKit uses file-based routing.

### Route file structure

```
ui/src/routes/<route-name>/
├── +page.svelte      # Page component
├── +page.ts          # Load function (optional, for SSR data)
└── +layout.svelte    # Layout wrapper (optional, inherits parent)
```

### Page template (Svelte 5 runes)

```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import { API_BASE, type MyType } from '$lib/api';

  // State — use $state(), never Svelte 4 stores
  let items: MyType[] = $state([]);
  let loading = $state(true);
  let error = $state('');

  // Derived values — use $derived()
  let itemCount = $derived(items.length);
  let hasItems = $derived(items.length > 0);

  // Complex derived — use $derived.by()
  let summary = $derived.by(() => {
    return items.reduce((acc, item) => acc + item.value, 0);
  });

  // Side effects — use $effect()
  $effect(() => {
    console.log(`Items changed: ${items.length}`);
  });

  onMount(async () => {
    try {
      const res = await fetch(`${API_BASE}/internal/my-endpoint?org_id=...&project_id=...`);
      items = await res.json();
    } catch (e: any) {
      error = e?.message || 'Failed to load';
    }
    loading = false;
  });
</script>

<div class="app-shell-wide">
  {#if loading}
    <p class="text-zinc-500 text-sm">Loading...</p>
  {:else if error}
    <div class="alert-danger">{error}</div>
  {:else}
    <div class="table-float">
      <!-- Content here -->
    </div>
  {/if}
</div>
```

## Creating a component

Components live in `ui/src/lib/components/`.

```svelte
<script lang="ts">
  // Props — use $props(), never export let
  let {
    items = [],
    selected = null,
    onSelect = undefined,
  }: {
    items: Item[];
    selected?: string | null;
    onSelect?: (id: string) => void;
  } = $props();

  // Internal state
  let expanded = $state(false);
</script>

<div class="surface-panel">
  {#each items as item (item.id)}
    <button
      class="btn-ghost"
      class:active={selected === item.id}
      onclick={() => onSelect?.(item.id)}
    >
      {item.name}
    </button>
  {/each}
</div>
```

## Adding API fetch helpers

Add new fetch functions to `ui/src/lib/api.ts`:

```typescript
export async function getMyEntities(): Promise<MyEntity[]> {
  const res = await fetch(`${API_BASE}/internal/my-entities?org_id=${getOrgId()}&project_id=${getProjectId()}`);
  if (!res.ok) throw new Error(`Failed to fetch: ${res.statusText}`);
  const data = await res.json();
  return data.items;
}
```

If the type comes from the OpenAPI spec, re-export it from `api-types.ts`:

```typescript
export type MyEntity = Schemas['MyEntity'];
```

## Design system primitives

Always check `DESIGN_SYSTEM.md` and reuse existing classes before adding new styles:

- **Surfaces**: `surface-panel`, `surface-command`, `surface-quiet`, `table-float`
- **Shells**: `app-shell-wide`, `app-toolbar-shell`, `app-page-shell`
- **Controls**: `control-input`, `control-select`, `control-textarea`
- **Buttons**: `btn-primary`, `btn-secondary`, `btn-ghost`
- **Chips**: `query-chip`, `query-chip-active`
- **Labels**: `label-micro`, `table-head-compact`
- **Alerts**: `alert-danger`, `alert-success`, `alert-warning`

## Key conventions

- **Svelte 5 only**: `$state`, `$derived`, `$effect`, `$props` — never use Svelte 4 `writable`/`derived` stores
- **Tailwind CSS v4**: Classes in markup, no CSS modules
- **Dark theme first**: Maintain dark/light parity on major surfaces
- **Dense controls**: 11px micro labels, 13px body, 14-16px headings
- **Floating panels**: Use right floating panel for detail/edit flows
- **a11y**: Use `for`/`id` on label/select pairs, proper button elements
- **Page params**: `page.params.id` can be `undefined` in Svelte 5 — always default with `?? ''`
- **Type casting**: Cast filters for query strings: `(filter ?? {}) as Record<string, string | undefined>`

## After creating the route

1. Run svelte-check: `cd ui && npm run check`
2. Verify in browser at `http://localhost:5173/<route-name>`
