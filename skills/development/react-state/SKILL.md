---
name: react-state
description: Zustand v5 state management for React. Use when implementing global state, stores, persist, or client-side state.
versions:
  zustand: 5.0
  react: 19
user-invocable: true
references: references/installation.md, references/store-patterns.md, references/middleware.md, references/typescript.md, references/slices.md, references/auto-selectors.md, references/reset-state.md, references/subscribe-api.md, references/testing.md, references/migration-v5.md
related-skills: react-19, react-forms, solid-react
---

# Zustand for React

Minimal, scalable state management with React 18+ useSyncExternalStore.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing stores and state patterns
2. **fuse-ai-pilot:research-expert** - Verify latest Zustand v5 docs via Context7/Exa
3. **mcp__context7__query-docs** - Check middleware and TypeScript patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Managing global state in React applications
- Need state shared across components
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

1. **useShallow for arrays/objects** - Prevent unnecessary re-renders
2. **Currying syntax v5** - `create<State>()((set) => ({...}))`
3. **SOLID paths** - Stores in `modules/[feature]/src/stores/`
4. **Separate stores** - One store per domain (auth, cart, ui, theme)
5. **Server state elsewhere** - Use TanStack Query for server state

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
| `use-store.ts` | Custom hook with selector | 20 |

---

## Key Concepts

### Store Creation (v5 Syntax)

Double parentheses required for TypeScript inference. Currying pattern ensures full type safety.

### Middleware Composition

Stack middlewares: devtools -> persist -> immer. Order matters for TypeScript types.

### Selector Pattern

Always use `useStore((s) => s.field)` for performance. Use `useShallow` for array/object selectors.

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Initial setup | [installation.md](references/installation.md) |
| Store patterns | [store-patterns.md](references/store-patterns.md) |
| Middleware | [middleware.md](references/middleware.md) |
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
| Persisting auth tokens | Security vulnerability | httpOnly cookies |
| Without useShallow on objects | Excessive re-renders | `useShallow(selector)` |
| v4 syntax | TypeScript inference broken | v5 currying `create<T>()()` |
| Giant monolithic store | Hard to maintain | Slices or separate stores |
