---
name: react-19
description: Guide for React 19 development with Actions, Server Components, and new hooks. Use for building React 19 apps, form handling, optimistic updates, and migrations.
---

# React 19

React 19 (stable since Dec 2024) simplifies async operations, improves SSR, and enhances DX with Actions, Server Components, and new hooks.

## When to Use

- Building React 19 applications
- Async form handling with automatic pending/error states
- Server Components for SSR
- Optimistic UI updates
- Migrating from React 18
- Server Actions for full-stack forms

## Installation

```bash
npm install react@19.2.1 react-dom@19.2.1
npm install --save-dev @types/react@19.0.0 @types/react-dom@19.0.0
```

**Required:** Enable modern JSX transform in `tsconfig.json`:
```json
{ "compilerOptions": { "jsx": "react-jsx" } }
```

## Core Concepts

### Execution Boundaries

| Type | Runs | State | Access |
|------|------|-------|--------|
| Server Component | Server | No | DB, FS, Secrets |
| Client Component | Browser | Yes | DOM, Browser APIs |
| Server Action | Server | No | DB, APIs |

### Conventions

- `"use server"` = Server Action
- `"use client"` = Client Component
- No directive = Server Component (in RSC environment)
- `async` component = Auto-suspends

## Essential Patterns

### 1. Forms with useActionState

```javascript
'use client';
import { useActionState } from 'react';

function SignupForm() {
  const [state, formAction, isPending] = useActionState(
    async (prev, formData) => {
      const error = await createUser(formData.get('email'));
      return error ? { error } : null;
    },
    { error: null }
  );

  return (
    <form action={formAction}>
      <input type="email" name="email" required />
      <button disabled={isPending}>
        {isPending ? 'Signing up...' : 'Sign Up'}
      </button>
      {state.error && <p>{state.error}</p>}
    </form>
  );
}
```

### 2. Optimistic Updates

```javascript
'use client';
import { useOptimistic } from 'react';

function Comments({ comments, addComment }) {
  const [optimistic, addOptimistic] = useOptimistic(
    comments,
    (curr, newComment) => [...curr, { ...newComment, pending: true }]
  );

  return (
    <div>
      {optimistic.map(c => <div key={c.id}>{c.text}</div>)}
      <form action={async (formData) => {
        addOptimistic({ id: Date.now(), text: formData.get('text') });
        await addComment(formData);
      }}>
        <input name="text" />
        <button>Post</button>
      </form>
    </div>
  );
}
```

### 3. Server Actions

```javascript
'use server';
export async function createPost(formData) {
  const title = formData.get('title');
  if (!title || title.length < 3) {
    return { error: 'Title too short' };
  }
  await db.posts.create({ title });
  revalidatePath('/posts');
}
```

### 4. Streaming with Suspense

```javascript
export default function Dashboard() {
  return (
    <div>
      <Suspense fallback={<Skeleton />}>
        <RevenueCard />
      </Suspense>
      <Suspense fallback={<Skeleton />}>
        <UsersCard />
      </Suspense>
    </div>
  );
}

async function RevenueCard() {
  const data = await db.analytics.getRevenue();
  return <div>{data}</div>;
}
```

## Security Essentials

```javascript
// 1. Always authenticate
'use server';
export async function deleteUser(id) {
  const user = await getCurrentUser();
  if (!user) throw new Error('Unauthorized');
  await db.users.delete(id);
}

// 2. Keep secrets server-side
'use server';
export async function fetchData() {
  const secret = process.env.API_SECRET; // Inside function!
  return fetch(url, { headers: { Authorization: `Bearer ${secret}` }});
}

// 3. Validate inputs
import { z } from 'zod';
const schema = z.object({ email: z.string().email() });
const result = schema.safeParse(formData);
```

See `references/security-guide.md` for complete security guidance.

## Migration from React 18

1. Update to React 18.3 first (fix warnings)
2. Update to React 19: `npm install react@19 react-dom@19`
3. Run codemods: `npx codemod@latest react/19/migration-recipe`
4. Fix TypeScript: `npx types-react-codemod@latest preset-19 ./src`
5. Test thoroughly

**Key breaking changes:**
- `ReactDOM.render` → `createRoot`
- `PropTypes` removed → Use TypeScript
- `forwardRef` deprecated → Use `ref` as prop
- `useRef()` requires argument → `useRef(null)`

See `references/upgrade-checklist.md` and `references/migration-patterns.md`.

## Quick Reference

### New Hooks

| Hook | Purpose |
|------|---------|
| `useActionState` | Form state with async actions |
| `useOptimistic` | Instant UI feedback |
| `use()` | Read promises/context (can be conditional) |
| `useTransition` | Non-urgent updates |

See `references/hooks-api.md` for detailed API docs.

### When to Use What

| Task | Solution |
|------|----------|
| Forms | `useActionState` + Server Actions |
| Instant UI | `useOptimistic` |
| Data fetching | Server Components with `async/await` |
| Refs | `ref` as regular prop |
| Progressive rendering | Suspense boundaries |

## Reference Files

- **references/hooks-api.md** - Complete hook documentation
- **references/migration-patterns.md** - Detailed migration guide
- **references/advanced-examples.md** - Production examples
- **references/security-guide.md** - Security best practices
- **references/upgrade-checklist.md** - Step-by-step upgrade
- **references/core-workflows.md** - 5 essential patterns with full examples

## Resources

- React 19 Docs: https://react.dev
- Next.js 15 Docs: https://nextjs.org/docs

**Version:** 2.1 | **Updated:** 2025-12-27
