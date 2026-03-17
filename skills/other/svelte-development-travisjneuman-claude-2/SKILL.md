---
name: svelte-development
description: Svelte 5 development with runes ($state, $derived, $effect), SvelteKit full-stack framework, and modern reactive patterns. Use when building Svelte applications, implementing fine-grained reactivity, or working with SvelteKit routing and server functions.
---

# Svelte 5 Development

Comprehensive guide for building modern Svelte applications with runes and SvelteKit.

## Stack Overview

| Tool       | Purpose              | Version |
| ---------- | -------------------- | ------- |
| Svelte 5   | Core framework       | 5.0+    |
| SvelteKit  | Full-stack framework | 2.0+    |
| TypeScript | Type safety          | 5.0+    |
| Vite       | Build tool           | 5.0+    |
| Vitest     | Testing              | 1.0+    |

---

## Svelte 5 Runes (Core Reactivity)

### The Rune System

Runes are compile-time macros prefixed with `$` that provide explicit, fine-grained reactivity.

| Rune        | Purpose               | Replaces                    |
| ----------- | --------------------- | --------------------------- |
| `$state`    | Reactive state        | `let` declarations          |
| `$derived`  | Computed values       | `$:` reactive statements    |
| `$effect`   | Side effects          | `$:` side effect statements |
| `$props`    | Component props       | `export let`                |
| `$bindable` | Two-way binding props | `export let` with bind:     |

### Basic Component Structure

```svelte
<script lang="ts">
  // Props with TypeScript
  interface Props {
    title: string
    count?: number
    onUpdate?: (value: number) => void
  }

  let { title, count = 0, onUpdate }: Props = $props()

  // Reactive state
  let localCount = $state(count)
  let items = $state<string[]>([])

  // Derived values (auto-update when dependencies change)
  let doubled = $derived(localCount * 2)
  let total = $derived(items.reduce((sum, i) => sum + i.length, 0))

  // Side effects
  $effect(() => {
    console.log(`Count changed to: ${localCount}`)
    onUpdate?.(localCount)
  })

  // Methods
  function increment() {
    localCount++
  }
</script>

<div class="component">
  <h1>{title}</h1>
  <p>Count: {localCount} (Doubled: {doubled})</p>
  <button onclick={increment}>Increment</button>
</div>

<style>
  .component {
    padding: 1rem;
  }
</style>
```

### State Patterns

```typescript
// Primitives
let count = $state(0);
let name = $state("");

// Objects (deeply reactive)
let user = $state({
  name: "John",
  email: "john@example.com",
  preferences: { theme: "dark" },
});

// Arrays
let items = $state<Item[]>([]);

// Direct mutation works!
user.name = "Jane"; // Reactive
user.preferences.theme = "light"; // Reactive (deep)
items.push({ id: 1, name: "New" }); // Reactive

// Frozen state (shallow reactivity)
let frozenList = $state.frozen([1, 2, 3]);
```

### Derived Values

```typescript
// Simple derived
let doubled = $derived(count * 2);

// Complex derived (use $derived.by for multi-line)
let stats = $derived.by(() => {
  const total = items.reduce((sum, i) => sum + i.value, 0);
  const average = items.length ? total / items.length : 0;
  return { total, average, count: items.length };
});

// Derived from multiple sources
let summary = $derived(`${user.name} has ${items.length} items`);
```

### Effects

```typescript
// Basic effect (runs when dependencies change)
$effect(() => {
  console.log(`Count is now: ${count}`);
});

// Effect with cleanup
$effect(() => {
  const interval = setInterval(() => {
    count++;
  }, 1000);

  // Cleanup function (returned)
  return () => clearInterval(interval);
});

// Pre-effect (runs before DOM updates)
$effect.pre(() => {
  console.log("About to update DOM");
});

// Root effect (doesn't track dependencies)
$effect.root(() => {
  // Manual dependency management
});
```

---

## Component Patterns

### Props with Defaults and Spreading

```svelte
<script lang="ts">
  interface Props {
    variant?: 'primary' | 'secondary'
    size?: 'sm' | 'md' | 'lg'
    disabled?: boolean
    children: import('svelte').Snippet
  }

  let {
    variant = 'primary',
    size = 'md',
    disabled = false,
    children,
    ...restProps
  }: Props = $props()
</script>

<button
  class="btn btn-{variant} btn-{size}"
  {disabled}
  {...restProps}
>
  {@render children()}
</button>
```

### Two-Way Binding with $bindable

```svelte
<!-- Input.svelte -->
<script lang="ts">
  interface Props {
    value: string
  }

  let { value = $bindable() }: Props = $props()
</script>

<input bind:value />

<!-- Parent.svelte -->
<script lang="ts">
  let name = $state('')
</script>

<Input bind:value={name} />
<p>Hello, {name}!</p>
```

### Snippets (Replacing Slots)

```svelte
<!-- Card.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte'

  interface Props {
    title: string
    children: Snippet
    footer?: Snippet
  }

  let { title, children, footer }: Props = $props()
</script>

<div class="card">
  <header>{title}</header>
  <main>{@render children()}</main>
  {#if footer}
    <footer>{@render footer()}</footer>
  {/if}
</div>

<!-- Usage -->
<Card title="My Card">
  <p>Card content goes here</p>

  {#snippet footer()}
    <button>Action</button>
  {/snippet}
</Card>
```

### Snippets with Parameters

```svelte
<!-- List.svelte -->
<script lang="ts" generics="T">
  import type { Snippet } from 'svelte'

  interface Props {
    items: T[]
    row: Snippet<[T, number]>
    empty?: Snippet
  }

  let { items, row, empty }: Props = $props()
</script>

{#if items.length === 0}
  {#if empty}
    {@render empty()}
  {:else}
    <p>No items</p>
  {/if}
{:else}
  <ul>
    {#each items as item, index}
      <li>{@render row(item, index)}</li>
    {/each}
  </ul>
{/if}

<!-- Usage -->
<List items={users}>
  {#snippet row(user, i)}
    <span>{i + 1}. {user.name}</span>
  {/snippet}

  {#snippet empty()}
    <p>No users found</p>
  {/snippet}
</List>
```

---

## Shared State with .svelte.ts Files

### Creating Shared State

```typescript
// lib/stores/counter.svelte.ts
export function createCounter(initial = 0) {
  let count = $state(initial);

  return {
    get count() {
      return count;
    },
    increment() {
      count++;
    },
    decrement() {
      count--;
    },
    reset() {
      count = initial;
    },
  };
}

// Singleton instance
export const counter = createCounter();
```

### Class-Based State

```typescript
// lib/stores/user.svelte.ts
export class UserStore {
  user = $state<User | null>(null);
  loading = $state(false);
  error = $state<string | null>(null);

  isLoggedIn = $derived(!!this.user);

  async login(email: string, password: string) {
    this.loading = true;
    this.error = null;

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) throw new Error("Login failed");

      this.user = await response.json();
    } catch (e) {
      this.error = e instanceof Error ? e.message : "Unknown error";
      throw e;
    } finally {
      this.loading = false;
    }
  }

  logout() {
    this.user = null;
  }
}

export const userStore = new UserStore();
```

### Using Shared State

```svelte
<script lang="ts">
  import { counter } from '$lib/stores/counter.svelte'
  import { userStore } from '$lib/stores/user.svelte'
</script>

<p>Count: {counter.count}</p>
<button onclick={counter.increment}>+</button>

{#if userStore.isLoggedIn}
  <p>Welcome, {userStore.user?.name}</p>
  <button onclick={() => userStore.logout()}>Logout</button>
{:else}
  <button onclick={() => userStore.login('test@test.com', 'pass')}>
    Login
  </button>
{/if}
```

---

## SvelteKit (Full-Stack)

### Project Structure

```
sveltekit-app/
├── src/
│   ├── routes/              # File-based routing
│   │   ├── +page.svelte     # /
│   │   ├── +page.server.ts  # Server load function
│   │   ├── +layout.svelte   # Root layout
│   │   ├── about/
│   │   │   └── +page.svelte # /about
│   │   ├── users/
│   │   │   ├── +page.svelte # /users
│   │   │   └── [id]/
│   │   │       ├── +page.svelte      # /users/:id
│   │   │       └── +page.server.ts
│   │   └── api/
│   │       └── users/
│   │           └── +server.ts  # /api/users
│   ├── lib/                 # $lib alias
│   │   ├── components/
│   │   └── stores/
│   └── app.html
├── static/
└── svelte.config.js
```

### Load Functions

```typescript
// routes/users/+page.server.ts
import type { PageServerLoad } from './$types'
import { error } from '@sveltejs/kit'

export const load: PageServerLoad = async ({ fetch, params }) => {
  const response = await fetch('/api/users')

  if (!response.ok) {
    throw error(response.status, 'Failed to load users')
  }

  const users = await response.json()

  return { users }
}

// routes/users/+page.svelte
<script lang="ts">
  import type { PageData } from './$types'

  let { data }: { data: PageData } = $props()
</script>

<h1>Users</h1>
{#each data.users as user}
  <p>{user.name}</p>
{/each}
```

### Form Actions

```typescript
// routes/login/+page.server.ts
import type { Actions } from "./$types";
import { fail, redirect } from "@sveltejs/kit";

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const formData = await request.formData();
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    // Validation
    if (!email || !password) {
      return fail(400, { email, missing: true });
    }

    // Authentication
    const user = await authenticate(email, password);

    if (!user) {
      return fail(401, { email, incorrect: true });
    }

    // Set session cookie
    cookies.set("session", user.token, { path: "/" });

    throw redirect(303, "/dashboard");
  },
};
```

```svelte
<!-- routes/login/+page.svelte -->
<script lang="ts">
  import type { ActionData } from './$types'
  import { enhance } from '$app/forms'

  let { form }: { form: ActionData } = $props()
</script>

<form method="POST" use:enhance>
  <input name="email" value={form?.email ?? ''} />

  {#if form?.missing}
    <p class="error">All fields are required</p>
  {/if}

  {#if form?.incorrect}
    <p class="error">Invalid credentials</p>
  {/if}

  <input name="password" type="password" />
  <button>Login</button>
</form>
```

### API Routes

```typescript
// routes/api/users/+server.ts
import type { RequestHandler } from "./$types";
import { json, error } from "@sveltejs/kit";

export const GET: RequestHandler = async ({ url }) => {
  const limit = Number(url.searchParams.get("limit")) || 10;

  const users = await prisma.user.findMany({ take: limit });

  return json(users);
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();

  if (!body.email || !body.name) {
    throw error(400, "Missing required fields");
  }

  const user = await prisma.user.create({ data: body });

  return json(user, { status: 201 });
};

// routes/api/users/[id]/+server.ts
export const GET: RequestHandler = async ({ params }) => {
  const user = await prisma.user.findUnique({
    where: { id: params.id },
  });

  if (!user) {
    throw error(404, "User not found");
  }

  return json(user);
};
```

### Middleware (Hooks)

```typescript
// src/hooks.server.ts
import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
  // Get session from cookie
  const session = event.cookies.get("session");

  if (session) {
    const user = await validateSession(session);
    event.locals.user = user;
  }

  // Protected routes
  if (event.url.pathname.startsWith("/dashboard") && !event.locals.user) {
    return new Response("Redirect", {
      status: 303,
      headers: { Location: "/login" },
    });
  }

  return resolve(event);
};
```

---

## Event Handling (Svelte 5)

### DOM Events (New Syntax)

```svelte
<!-- Old: on:click -->
<!-- New: onclick -->

<button onclick={() => count++}>Click me</button>

<input
  oninput={(e) => name = e.currentTarget.value}
  onkeydown={(e) => e.key === 'Enter' && submit()}
/>

<!-- Event modifiers: use JavaScript -->
<button onclick={(e) => {
  e.preventDefault()
  e.stopPropagation()
  handleClick()
}}>
  Submit
</button>

<!-- Once: use wrapper -->
<script>
  function once(fn) {
    return function(e) {
      if (!e.target.dataset.clicked) {
        e.target.dataset.clicked = 'true'
        fn(e)
      }
    }
  }
</script>

<button onclick={once(() => console.log('Once!'))}>
  Click once
</button>
```

### Component Events (Callback Props)

```svelte
<!-- Old: createEventDispatcher -->
<!-- New: callback props -->

<!-- Child.svelte -->
<script lang="ts">
  interface Props {
    onSelect?: (id: string) => void
    onClose?: () => void
  }

  let { onSelect, onClose }: Props = $props()
</script>

<button onclick={() => onSelect?.('123')}>Select</button>
<button onclick={onClose}>Close</button>

<!-- Parent.svelte -->
<Child
  onSelect={(id) => console.log('Selected:', id)}
  onClose={() => console.log('Closed')}
/>
```

---

## Testing with Vitest

### Setup

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import { svelte } from "@sveltejs/vite-plugin-svelte";

export default defineConfig({
  plugins: [svelte({ hot: !process.env.VITEST })],
  test: {
    globals: true,
    environment: "jsdom",
    include: ["src/**/*.{test,spec}.{js,ts}"],
  },
});
```

### Component Testing

```typescript
// tests/Counter.test.ts
import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/svelte";
import Counter from "$lib/components/Counter.svelte";

describe("Counter", () => {
  it("renders initial count", () => {
    render(Counter, { props: { initial: 5 } });

    expect(screen.getByText("Count: 5")).toBeInTheDocument();
  });

  it("increments on click", async () => {
    render(Counter);

    const button = screen.getByRole("button", { name: /increment/i });
    await fireEvent.click(button);

    expect(screen.getByText("Count: 1")).toBeInTheDocument();
  });
});
```

### Testing Stores

```typescript
// tests/stores/counter.test.ts
import { describe, it, expect } from "vitest";
import { counter } from "$lib/stores/counter.svelte";

describe("counter store", () => {
  it("increments count", () => {
    counter.reset();
    expect(counter.count).toBe(0);

    counter.increment();
    expect(counter.count).toBe(1);

    counter.increment();
    expect(counter.count).toBe(2);
  });

  it("decrements count", () => {
    counter.reset();
    counter.decrement();
    expect(counter.count).toBe(-1);
  });
});
```

---

## Migration from Svelte 4

| Svelte 4                   | Svelte 5                            |
| -------------------------- | ----------------------------------- |
| `let count = 0` (reactive) | `let count = $state(0)`             |
| `$: doubled = count * 2`   | `let doubled = $derived(count * 2)` |
| `$: console.log(count)`    | `$effect(() => console.log(count))` |
| `export let value`         | `let { value } = $props()`          |
| `on:click={handler}`       | `onclick={handler}`                 |
| `<slot />`                 | `{@render children()}`              |
| `createEventDispatcher()`  | Callback props                      |

### Migration Script

```bash
npx sv migrate svelte-5
```

---

## Anti-Patterns to Avoid

| Anti-Pattern                       | Problem                | Solution                    |
| ---------------------------------- | ---------------------- | --------------------------- |
| Using `$effect` for derived values | Unnecessary complexity | Use `$derived`              |
| Exporting `$state` directly        | Breaks reactivity      | Export getter/setter object |
| Not using TypeScript               | Missing type safety    | Enable `lang="ts"`          |
| Using old slot syntax              | Deprecated in Svelte 5 | Use snippets                |
| Using `on:event` syntax            | Deprecated in Svelte 5 | Use `onevent` props         |

---

## Performance Benefits

| Metric              | Improvement                   |
| ------------------- | ----------------------------- |
| Bundle size         | 40-60% smaller than React/Vue |
| Runtime performance | No virtual DOM overhead       |
| Time to interactive | Minimal JavaScript hydration  |
| Memory usage        | Lower due to compiled output  |

---

## Related Resources

- [Svelte 5 Documentation](https://svelte.dev/docs)
- [SvelteKit Documentation](https://svelte.dev/docs/kit)
- [Svelte 5 Migration Guide](https://svelte.dev/docs/svelte/v5-migration-guide)
- [Svelte Testing Docs](https://svelte.dev/docs/svelte/testing)
- [Joy of Code Tutorials](https://joyofcode.xyz/)

---

## When to Use This Skill

- Building new Svelte 5 applications with runes
- Migrating from Svelte 4 to Svelte 5
- Full-stack development with SvelteKit
- Creating reactive shared state
- Implementing form actions and API routes
- Testing Svelte components with Vitest
