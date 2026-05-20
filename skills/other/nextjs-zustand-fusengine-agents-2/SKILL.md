---
name: nextjs-zustand
description: Zustand v5 state management for Next.js 16 App Router. Use when implementing global state, stores, persist, hydration, or client-side state in Client Components.
versions:
  zustand: 5.0
  react: 19
  nextjs: 16
user-invocable: true
references: references/installation.md, references/store-patterns.md, references/hydration.md, references/middleware.md, references/nextjs-integration.md, references/typescript.md, references/slices.md, references/auto-selectors.md, references/reset-state.md, references/subscribe-api.md, references/testing.md, references/migration-v5.md
related-skills: nextjs-16, nextjs-tanstack-form, solid-nextjs
---

# Zustand for Next.js 16

Minimal, scalable state management with React 18+ useSyncExternalStore.

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing stores and state patterns
2. **fuse-ai-pilot:research-expert** - Verify latest Zustand v5 docs via Context7/Exa
3. **mcp__context7__query-docs** - Check middleware and TypeScript patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Managing client-side state in Next.js App Router applications
- Need global state across Client Components only
- Persisting state to localStorage/sessionStorage
- Building UI state (modals, sidebars, theme, cart)
- Replacing React Context for complex state

### Why Zustand v5

| Feature | Benefit |
|---------|---------|
| Minimal API | Simple create() function, no boilerplate |
| React 18 native | useSyncExternalStore, no shims needed |
| TypeScript first | Full inference with currying pattern |
| Middleware stack | devtools, persist, immer composable |
| Bundle size | ~2KB gzipped, smallest state library |
| No providers | Direct store access, no Context wrapper |

---

## Critical Rules

1. **Client Components ONLY** - Never use Zustand in Server Components
2. **Context pattern for App Router** - Avoid global stores (request isolation)
3. **useShallow for arrays/objects** - Prevent unnecessary re-renders
4. **skipHydration with persist** - Required for SSR compatibility
5. **Currying syntax v5** - `create<State>()((set) => ({...}))`
6. **SOLID paths** - Stores in `modules/[feature]/src/stores/`

---

## SOLID Architecture

### Module Structure

Stores organized by feature module:

- `modules/cores/stores/` - Shared stores (theme, ui)
- `modules/auth/src/stores/` - Auth state
- `modules/cart/src/stores/` - Cart state
- `modules/[feature]/src/interfaces/` - Store types

### File Organization

| File | Purpose | Max Lines |
|------|---------|-----------|
| `store.ts` | Store creation with create() | 50 |
| `store.interface.ts` | TypeScript interfaces | 30 |
| `store-provider.tsx` | Context provider (App Router) | 40 |
| `use-store.ts` | Custom hook with selector | 20 |

---

## Key Concepts

### Store Creation (v5 Syntax)

Double parentheses required for TypeScript inference. Currying pattern ensures full type safety.

### Context-Based Stores

For Next.js App Router, wrap stores in Context to prevent request-sharing. Use `createStore` from `zustand/vanilla` with `useRef` for initialization.

### Middleware Composition

Stack middlewares: devtools → persist → immer. Order matters for TypeScript types.

### Hydration Handling

Use `skipHydration: true` with persist middleware. Manually rehydrate in useEffect to avoid SSR mismatches.

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Initial setup | [installation.md](references/installation.md) |
| Store patterns | [store-patterns.md](references/store-patterns.md) |
| SSR/Hydration | [hydration.md](references/hydration.md) |
| Middleware | [middleware.md](references/middleware.md) |
| Next.js App Router | [nextjs-integration.md](references/nextjs-integration.md) |
| TypeScript | [typescript.md](references/typescript.md) |
| Slices pattern | [slices.md](references/slices.md) |
| Auto selectors | [auto-selectors.md](references/auto-selectors.md) |
| Reset state | [reset-state.md](references/reset-state.md) |
| Subscribe API | [subscribe-api.md](references/subscribe-api.md) |
| Testing | [testing.md](references/testing.md) |
| Migration v4→v5 | [migration-v5.md](references/migration-v5.md) |

---

## Best Practices

1. **Selector pattern** - Always use `useStore((s) => s.field)` for performance
2. **useShallow** - Wrap array/object selectors to prevent re-renders
3. **Separate stores** - One store per domain (auth, cart, ui, theme)
4. **Server data elsewhere** - Use TanStack Query for server state
5. **DevTools in dev only** - Wrap devtools in process.env check
6. **Partialize persist** - Only persist necessary fields, never tokens

---

## Forbidden Patterns

| Pattern | Reason | Alternative |
|---------|--------|-------------|
| Global stores in App Router | Request sharing between users | Context-based stores |
| Zustand in Server Components | No React hooks in RSC | Fetch data directly |
| Persisting auth tokens | Security vulnerability | httpOnly cookies |
| Without useShallow on objects | Excessive re-renders | `useShallow(selector)` |
| v4 syntax | TypeScript inference broken | v5 currying `create<T>()()` |
