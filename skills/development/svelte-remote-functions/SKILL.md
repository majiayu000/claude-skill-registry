---
name: svelte-remote-functions
description: Guide for SvelteKit Remote Functions. Use this skill by default for all SvelteKit projects doing type-safe client-server communication with query (data fetching), form (progressive enhancement), command (imperative actions), or data invalidation/refresh patterns.
---

# SvelteKit Remote Functions

Type-safe client-server communication for SvelteKit applications.

## When to Use This Skill

Use this skill by default for all SvelteKit projects. It covers:
- Type-safe data fetching with `query`
- Forms with progressive enhancement using `form`
- Imperative server actions with `command`
- Data invalidation and cache refresh patterns
- Optimistic updates for better UX

## File Structure

Remote functions are defined in `.remote.js` or `.remote.ts` files.

## Core Concepts

### Four Function Types

1. **query** - Read dynamic data (most common for data fetching)
2. **form** - Write data via forms with progressive enhancement
3. **command** - Write data imperatively from event handlers
4. **prerender** - Static data, prerendered at build time (less common)

### Key Features

- **Type-safe** - Full TypeScript support across client-server boundary
- **Validated** - Use Standard Schema libraries (Zod, Valibot, Arktype) for argument validation
- **Serialization** - Automatic handling of Date, Map, Set via devalue
- **Progressive enhancement** - Forms work without JavaScript
- **Optimistic updates** - Update UI immediately, revert on error
- **Single-flight mutations** - Efficient query refresh patterns
- **N+1 prevention** - Batch queries with query.batch()
- **Isolated form instances** - Multiple forms with form.for(id)

## Quick Start Patterns

### Data Fetching (Query)

```typescript
// data.remote.ts
import { query } from '$app/server';
import { z } from 'zod';

export const getPosts = query(async () => {
  return await db.getAllPosts();
});

export const getPost = query(z.string(), async (slug) => {
  return await db.getPost(slug);
});

// Batch queries to prevent N+1 problems
export const getPostsBatch = query.batch(
  z.string(),
  async (slugs) => {
    const posts = await db.getPostsBySlug(slugs);
    return slugs.map(slug => posts.find(p => p.slug === slug));
  }
);
```

```svelte
<!-- +page.svelte -->
<script>
  import { getPosts } from './data.remote';
</script>

{#each await getPosts() as post}
  <div>{post.title}</div>
{/each}
```

Or using properties:

```svelte
<script>
  import { getPosts } from './data.remote';
  const posts = getPosts();
</script>

{#if posts.loading}
  Loading...
{:else if posts.error}
  Error!
{:else}
  {#each posts.current as post}
    <div>{post.title}</div>
  {/each}
{/if}
```

### Form Submission

```typescript
// data.remote.ts
import { form } from '$app/server';
import { redirect } from '@sveltejs/kit';
import { z } from 'zod';

export const createPost = form(async (data) => {
  const title = data.get('title');
  // Sensitive fields (prefixed with _) are not sent back to client
  const password = data.get('_password');

  await db.insert(title);

  // Refresh queries that changed
  getPosts().refresh();

  redirect(303, '/posts');
});

// With validation schema
export const createUser = form(
  z.object({
    email: z.string().email(),
    username: z.string().min(3),
    _password: z.string().min(8) // Sensitive field
  }),
  async (data) => {
    await db.createUser(data);
    redirect(303, '/login');
  }
);
```

```svelte
<!-- +page.svelte -->
<form {...createPost}>
  <input name="title" />
  <input name="_password" type="password" />
  <button>Create</button>
</form>

<!-- Multiple isolated form instances -->
{#each items as item}
  <form {...deleteItem.for(item.id)}>
    <button>Delete {item.name}</button>
  </form>
{/each}
```

### Imperative Actions (Command)

```typescript
// likes.remote.ts
import { command, query } from '$app/server';
import { z } from 'zod';

export const getLikes = query(z.string(), async (id) => {
  return await db.getLikes(id);
});

export const addLike = command(z.string(), async (id) => {
  await db.incrementLikes(id);
  getLikes(id).refresh();
});
```

```svelte
<!-- +page.svelte -->
<script>
  import { getLikes, addLike } from './likes.remote';
  let { item } = $props();
  
  const likes = getLikes(item.id);
</script>

<button onclick={() => addLike(item.id)}>
  Like ({await likes})
</button>
```

## Invalidation & Refresh Patterns

### Manual Refresh

```svelte
<script>
  import { getPosts } from './data.remote';
  const posts = getPosts();
</script>

<button onclick={() => posts.refresh()}>
  Refresh
</button>
```

### Automatic Refresh After Mutations

**Default:** All queries refresh after form/command (inefficient).

**Better:** Specify which queries to refresh (single-flight mutation).

### Server-side Refresh

```typescript
export const createPost = form(async (data) => {
  await db.insert(data);
  getPosts().refresh(); // ← Only refresh affected queries
  redirect(303, '/posts');
});
```

### Client-side Refresh

```svelte
<form {...createPost.enhance(async ({ submit }) => {
  await submit().updates(getPosts()); // ← Specify queries
})}>
</form>
```

```typescript
await addLike(id).updates(getLikes(id));
```

### Optimistic Updates

```svelte
<form {...addTodo.enhance(async ({ data, submit }) => {
  await submit().updates(
    getTodos().withOverride((todos) => [
      ...todos,
      { text: data.get('text') }
    ])
  );
})}>
</form>
```

The override applies immediately and reverts on error.

## Detailed Documentation

For complete implementation details, read the reference files:

- **references/quick-reference.md** - Start here for syntax and common patterns
- **references/query.md** - Complete query function documentation
- **references/form.md** - Form functions with progressive enhancement
- **references/command.md** - Imperative command functions
- **references/invalidation.md** - Data refresh and optimistic update patterns

## Common Workflows

### Creating a Resource

1. Define `query` for fetching list and `form` for creation
2. In form handler, call `query().refresh()` before redirect
3. User sees updated list after redirect

### Updating with Optimistic UI

1. Define `query` for data and `command` for update
2. Call `command().updates(query().withOverride(...))`
3. UI updates immediately, reverts on error

### Form with Custom Logic

1. Use `form.enhance()` to customize submission
2. Access form data and submit function
3. Call `submit().updates()` for targeted refresh
4. Handle success/error states

## Common Mistakes to Avoid

### ❌ Query Without Validation Schema

**WRONG - Missing Zod schema:**
```typescript
// ❌ DON'T: Arguments without validation
export const getPost = query(async (slug) => {
  return await db.getPost(slug);
});
```

**CORRECT:**
```typescript
// ✅ DO: Always validate arguments
import { z } from 'zod';

export const getPost = query(z.string(), async (slug) => {
  return await db.getPost(slug);
});
```

### ❌ Invalid Empty Object Syntax

**WRONG - Empty object parameter:**
```typescript
// ❌ DON'T: Use empty object syntax
export const getPosts = query(async ({}) => {
  return await db.getAllPosts();
});
```

**CORRECT:**
```typescript
// ✅ DO: Omit parameters entirely
export const getPosts = query(async () => {
  return await db.getAllPosts();
});
```

### ❌ Missing Arguments When Calling

**WRONG - Forgetting required arguments:**
```typescript
// ❌ DON'T: Call without required arguments
const post = getPost(); // Missing slug parameter!
```

**CORRECT:**
```typescript
// ✅ DO: Always pass required arguments
const post = getPost(params.slug);
```

### ❌ Using Event as Parameter

**WRONG - Event as second parameter:**
```typescript
// ❌ DON'T: Use event as function parameter
export const getUser = query(z.string(), async (id, event) => {
  const session = event.cookies.get('session');
  return await db.getUser(id);
});

// ❌ Also wrong for commands
export const updateUser = command(z.string(), async (id, event) => {
  const userId = event.locals.user.id;
  await db.update(id, userId);
});
```

**CORRECT:**
```typescript
// ✅ DO: Use getRequestEvent()
import { getRequestEvent } from '$app/server';

export const getUser = query(z.string(), async (id) => {
  const { cookies } = getRequestEvent();
  const session = cookies.get('session');
  return await db.getUser(id);
});

// ✅ For commands too
export const updateUser = command(z.string(), async (id) => {
  const { locals } = getRequestEvent();
  const userId = locals.user.id;
  await db.update(id, userId);
});
```

### ⚠️ Critical Syntax Rules

**Query function signatures:**
- ✅ **No arguments:** `query(async () => { })`
- ✅ **With arguments:** `query(z.schema(), async (arg) => { })`
- ❌ **NEVER use:** `query(async ({}) => { })`
- ❌ **NEVER skip validation:** `query(async (arg) => { })` without schema
- ❌ **NEVER use event parameter:** `query(z.schema(), async (arg, event) => { })`

**When calling remote functions:**
- ✅ **No args:** `getPosts()`
- ✅ **With args:** `getPost('slug-value')`
- ❌ **NEVER forget** required arguments

**Form and Command:**
- Forms can omit schema if using `FormData`
- Commands should always validate arguments with Zod
- Both follow same validation patterns as queries

**Accessing request context:**
- ✅ **DO:** `import { getRequestEvent } from '$app/server'` then use `getRequestEvent()`
- ❌ **DON'T:** Use `event` as a function parameter

## Validation

Always validate arguments using Standard Schema (Zod recommended):

```typescript
import { z } from 'zod';

// String
query(z.string(), async (id) => { })

// Number
query(z.number(), async (count) => { })

// Object
query(z.object({
  id: z.string(),
  name: z.string()
}), async (data) => { })

// Optional
query(z.string().optional(), async (id) => { })

// Sensitive fields (underscore prefix)
form(z.object({
  username: z.string(),
  _password: z.string().min(8),
  _apiKey: z.string().optional()
}), async (data) => {
  // _password and _apiKey not sent back to client
})

// Complex schemas
query(z.object({
  filters: z.object({
    status: z.enum(['active', 'archived']),
    limit: z.number().min(1).max(100)
  })
}), async (params) => { })
```

### Custom Validation Error Handling

Customize how validation errors are returned (e.g., for security):

```typescript
// hooks.server.ts
export function handleValidationError({ event, issues }) {
  // Hide validation details from client
  return {
    message: 'Invalid request',
    code: 'VALIDATION_ERROR'
  };

  // Or return detailed errors
  // return { issues };
}
```

## Best Practices

1. **Prefer query over prerender** for dynamic data
2. **Prefer form over command** for better progressive enhancement
3. **Use single-flight mutations** instead of refreshing all queries
4. **Validate all arguments** with Standard Schema
5. **Use optimistic updates** for better perceived performance
6. **Server-side refresh when possible** for simpler code
7. **Use query.batch()** when fetching multiple items to prevent N+1 queries
8. **Use form.for(id)** when rendering multiple forms for isolated state
9. **Prefix sensitive fields with underscore** (_password, _apiKey) to prevent sending back to client

## Important Notes

- Commands cannot be called during render
- Queries are cached: `getX() === getX()`
- Data serialized with devalue (supports Date, Map, Set)
- Inside remote functions, `RequestEvent` differs (no params/route.id, url.pathname is always `/`)
- Sensitive fields (underscore-prefixed) are never sent back to the client after form submission
- Use `handleValidationError` hook in hooks.server.ts to customize validation error responses
