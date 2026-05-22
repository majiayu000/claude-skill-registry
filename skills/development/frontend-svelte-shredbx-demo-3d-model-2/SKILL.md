---
name: frontend-svelte
description: Technical knowledge for SvelteKit 5 development. Build reactive applications with Svelte's compile-time magic. Expert in SvelteKit, stores, and reactive patterns. Activate for Svelte development, performance optimization, or modern web apps. This skill provides MCP usage patterns and Svelte 5 conventions. Use when implementing Svelte components or SvelteKit routes.
---

# Frontend-Svelte

Technical reference for SvelteKit 5 development.

## MCP Usage Priority

1. **svelte** - Official Svelte 5 and SvelteKit documentation (ALWAYS CHECK FIRST)
2. **context7** - Third-party libraries:
   - shadcn-svelte: `/huntabyte/shadcn-svelte`
   - Other Svelte ecosystem packages
3. **web_search** - For cases not covered by MCPs

## Svelte 5 Conventions

- **Runes**: `$state`, `$derived`, `$effect`, `$props`
- **Components**: Single-file `.svelte` components
- **Events**: Use `onclick={handler}` syntax

## SvelteKit Conventions

- **Routes**: `+page.svelte`, `+page.server.ts`, `+layout.svelte`
- **Data Loading**: Use `load` functions in `+page.server.ts`
- **Form Actions**: `+page.server.ts` actions

# Svelte 5 Standards

## Runes (Svelte 5)

- Use $state() for reactive state
- Use $derived() for computed values
- Use $effect() for side effects (sparingly)
- Use $props() for component props

```svelte
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);

  let { user, onUpdate } = $props<{
    user: User;
    onUpdate: (user: User) => void;
  }>();

  $effect(() => {
    console.log('Count changed:', count);
  });
</script>
```

## Component Structure

- Script (setup code) → Markup → Styles
- TypeScript by default
- Export props explicitly with $props()
- Keep components small (<200 lines)

## State Management

- Local state: $state()
- Derived values: $derived()
- Cross-component: Svelte stores or context
- Avoid global stores when local state works

## Stores (when needed)

```typescript
// stores.ts
import { writable, derived } from "svelte/store";

export const user = writable<User | null>(null);
export const isLoggedIn = derived(user, ($user) => $user !== null);
```

## Reactivity Best Practices

- Keep $effect() minimal and focused
- Avoid side effects in $derived()
- Use event handlers over watchers when possible
- Don't mutate props

## Forms & Validation

- Use bind:value for two-way binding
- Validate on blur, not on every keystroke
- Use form actions for submissions (SvelteKit)
- Show errors after user interaction

## SvelteKit Specific

- Use load functions for data fetching
- +page.svelte for routes
- +page.server.ts for server-side logic
- +layout.svelte for shared layouts
- Form actions in +page.server.ts

```typescript
// +page.server.ts
export const load = async ({ params, locals }) => {
  const property = await db.property.findUnique({
    where: { id: params.id },
  });
  return { property };
};

export const actions = {
  default: async ({ request, locals }) => {
    const data = await request.formData();
    // handle form submission
  },
};
```

## Component Props Pattern

```svelte
<script lang="ts">
  interface Props {
    title: string;
    subtitle?: string;
    onSave?: (data: FormData) => void;
  }

  let { title, subtitle = '', onSave }: Props = $props();
</script>
```

## Styling

- Scoped styles by default
- Use CSS variables for theming
- Tailwind for utility classes (if using)
- Keep critical CSS inline
- Avoid deep selectors (:global() sparingly)

## Performance

- Use {#key} to force recreation when needed
- Lazy load heavy components
- Virtual lists for long lists
- Debounce expensive operations

## Anti-Patterns to Avoid

- Don't use $effect() for derived state (use $derived())
- Don't create stores for everything (local state first)
- Don't mutate props directly
- Avoid nested reactive statements
- Don't use bind: for one-way data flow

## Component Documentation Standard (Bestays)

Every component should have a header comment block:

```svelte
<!--
ComponentName - Brief description

ARCHITECTURE:
  Layer: Component/Page
  Pattern: [Pattern Name]

PATTERNS USED:
  - Pattern 1
  - Pattern 2

DEPENDENCIES:
  External: [npm packages]
  Internal: [local imports]

INTEGRATION:
  - Used by: [files]
  - Spec: [spec file if exists]
-->
```
