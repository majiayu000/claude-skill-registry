---
name: react-server-components-framework
description: Use when building Next.js 16+ apps with React Server Components. Covers App Router, streaming SSR, Server Actions, and React 19 patterns for server-first architecture.
context: fork
agent: frontend-ui-developer
version: 1.3.0
author: AI Agent Hub
tags: [frontend, react, react-19.2, nextjs-16, server-components, streaming, 2026]
user-invocable: false
---

# React Server Components Framework

## Overview

React Server Components (RSC) enable server-first rendering with client-side interactivity. This skill covers Next.js 16 App Router patterns, Server Components, Server Actions, and streaming.

**When to use this skill:**
- Building Next.js 16+ applications with the App Router
- Designing component boundaries (Server vs Client Components)
- Implementing data fetching with caching and revalidation
- Creating mutations with Server Actions
- Optimizing performance with streaming and Suspense

---

## Quick Reference

### Server vs Client Components

| Feature | Server Component | Client Component |
|---------|-----------------|------------------|
| Directive | None (default) | `'use client'` |
| Async/await | Yes | No |
| Hooks | No | Yes |
| Browser APIs | No | Yes |
| Database access | Yes | No |
| Client JS bundle | Zero | Ships to client |

**Key Rule**: Server Components can render Client Components, but Client Components cannot directly import Server Components (use `children` prop instead).

### Data Fetching Quick Reference

```tsx
// Static (cached indefinitely)
await fetch(url, { cache: 'force-cache' })

// Revalidate every 60 seconds
await fetch(url, { next: { revalidate: 60 } })

// Always fresh
await fetch(url, { cache: 'no-store' })

// Tag-based revalidation
await fetch(url, { next: { tags: ['posts'] } })
```

### Server Actions Quick Reference

```tsx
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const post = await db.post.create({ data: { title } })
  revalidatePath('/posts')
  redirect("/posts/" + post.id)
}
```

---

## References

### Server Components
**See: `references/server-components.md`**

Key topics covered:
- Async server components and direct database access
- Data fetching patterns (parallel, sequential, cached)
- Route segment config (dynamic, revalidate, PPR)
- generateStaticParams for SSG
- Error handling and composition patterns

### Client Components
**See: `references/client-components.md`**

Key topics covered:
- The `'use client'` directive and boundary rules
- React 19 patterns (function declarations, ref as prop)
- Interactivity patterns (state, forms, events)
- Hydration and avoiding hydration mismatches
- Composition with Server Components via children

### Streaming Patterns
**See: `references/streaming-patterns.md`**

Key topics covered:
- Suspense boundaries and loading states
- loading.tsx automatic wrapping
- Parallel streaming and nested Suspense
- Partial Prerendering (PPR)
- Skeleton component best practices

### React 19 Patterns
**See: `references/react-19-patterns.md`**

Key topics covered:
- Function declarations over React.FC
- Ref as prop (forwardRef removal)
- useActionState, useFormStatus, useOptimistic
- Activity component for preloading UI
- useEffectEvent hook

### Server Actions
**See: `references/server-actions.md`**

Key topics covered:
- Progressive enhancement patterns
- Form handling with useActionState
- Validation with Zod
- Optimistic updates

### Routing Patterns
**See: `references/routing-patterns.md`**

Key topics covered:
- Parallel routes for simultaneous rendering
- Intercepting routes for modals
- Route groups for organization
- Dynamic and catch-all routes

### Migration Guide
**See: `references/migration-guide.md`**

Key topics covered:
- Pages Router to App Router migration
- getServerSideProps/getStaticProps replacement
- Layout and metadata migration

### TanStack Router
**See: `references/tanstack-router-patterns.md`**

Key topics covered:
- React 19 features without Next.js
- Route-based data fetching
- Client-rendered app patterns

---

## Searching References

```bash
# Find component patterns
grep -r "Server Component" references/

# Search for data fetching strategies
grep -A 10 "Caching Strategies" references/data-fetching.md

# Find Server Actions examples
grep -B 5 "Progressive Enhancement" references/server-actions.md

# Locate routing patterns
grep -n "Parallel Routes" references/routing-patterns.md
```

---

## Best Practices Summary

### Component Boundaries
- Keep Client Components at the edges (leaves) of the component tree
- Use Server Components by default
- Extract minimal interactive parts to Client Components
- Pass Server Components as `children` to Client Components

### Data Fetching
- Fetch data in Server Components close to where it's used
- Use parallel fetching (`Promise.all`) for independent data
- Set appropriate cache and revalidate options
- Use `generateStaticParams` for static routes

### Performance
- Use Suspense boundaries for streaming
- Implement loading.tsx for instant loading states
- Enable PPR for static/dynamic mix
- Use route segment config to control rendering mode

---

## Templates

- **`templates/ServerComponent.tsx`** - Basic async Server Component with data fetching
- **`templates/ClientComponent.tsx`** - Interactive Client Component with hooks
- **`templates/ServerAction.tsx`** - Server Action with validation and revalidation

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| "You're importing a component that needs useState" | Add `'use client'` directive |
| "async/await is not valid in non-async Server Components" | Add `async` to function declaration |
| "Cannot use Server Component inside Client Component" | Pass Server Component as `children` prop |
| "Hydration mismatch" | Use `'use client'` for Date.now(), Math.random(), browser APIs |

---

## Resources

- [Next.js 16 Documentation](https://nextjs.org/docs)
- [React 19.2 Blog Post](https://react.dev/blog/2025/10/01/react-19-2)
- [React Server Components RFC](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md)
- [App Router Migration Guide](https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration)

---

## Related Skills

After mastering React Server Components:
1. **Streaming API Patterns** - Real-time data patterns
2. **Type Safety & Validation** - tRPC integration
3. **Edge Computing Patterns** - Global deployment
4. **Performance Optimization** - Core Web Vitals

---

## Capability Details

### react-19-patterns
**Keywords:** react 19, React.FC, forwardRef, useActionState, useFormStatus, useOptimistic, function declaration
**Solves:**
- How do I replace React.FC in React 19?
- forwardRef replacement pattern
- useActionState vs useFormState
- React 19 component declaration best practices

### use-hook-suspense
**Keywords:** use(), use hook, suspense, promise, data fetching, promise cache, cachePromise
**Solves:**
- How do I use the use() hook in React 19?
- Suspense-native data fetching pattern
- Promise caching to prevent infinite loops

### optimistic-updates-async
**Keywords:** useOptimistic, useTransition, optimistic update, instant ui, auto rollback
**Solves:**
- How to show instant UI updates before API responds?
- useOptimistic with useTransition pattern
- Auto-rollback on API failure

### rsc-patterns
**Keywords:** rsc, server component, client component, use client, use server
**Solves:**
- When to use server vs client components?
- RSC boundaries and patterns

### server-actions
**Keywords:** server action, form action, use server, mutation
**Solves:**
- How do I create a server action?
- Form handling with server actions

### data-fetching
**Keywords:** fetch, data fetching, async component, loading, suspense
**Solves:**
- How do I fetch data in RSC?
- Async server components

### streaming-ssr
**Keywords:** streaming, ssr, suspense boundary, loading ui
**Solves:**
- How do I stream server content?
- Progressive loading patterns

### caching
**Keywords:** cache, revalidate, static, dynamic, isr
**Solves:**
- How do I cache in Next.js 15?
- Revalidation strategies

### tanstack-router-patterns
**Keywords:** tanstack router, react router, vite, spa, client rendering, prefetch
**Solves:**
- How do I use React 19 features without Next.js?
- TanStack Router prefetching setup
- Route-based data fetching with TanStack Query