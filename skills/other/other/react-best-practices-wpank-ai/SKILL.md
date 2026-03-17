---
name: react-best-practices
model: standard
version: 1.0.0
description: >
  React and Next.js performance optimization guidelines from Vercel Engineering.
  57 rules across 8 categories for writing, reviewing, and refactoring React code.
tags: [react, nextjs, performance, optimization, ssr, bundle, rendering]
license: MIT
author: vercel
---

# React Best Practices

Comprehensive performance optimization guide for React and Next.js applications from Vercel Engineering. Contains 57 rules across 8 categories, prioritized by impact.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install react-best-practices
```


## WHAT This Skill Does

Provides actionable rules for:
- Eliminating request waterfalls
- Optimizing bundle size
- Improving server-side performance
- Efficient client-side data fetching
- Minimizing re-renders
- Rendering performance optimizations
- JavaScript micro-optimizations
- Advanced patterns for edge cases

## WHEN To Use

- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring React/Next.js applications
- Optimizing bundle size or load times
- Debugging slow renders or waterfalls

## KEYWORDS

react performance, nextjs optimization, bundle size, waterfalls, suspense, server components, rsc, rerender, usememo, dynamic import, parallel fetching, cache, swr

## Rule Categories by Priority

| Priority | Category | Impact | Rule Prefix |
|----------|----------|--------|-------------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

| Rule | Description |
|------|-------------|
| `async-defer-await` | Move await into branches where actually used |
| `async-parallel` | Use `Promise.all()` for independent operations |
| `async-dependencies` | Use better-all for partial dependencies |
| `async-api-routes` | Start promises early, await late in API routes |
| `async-suspense-boundaries` | Use Suspense to stream content |

### 2. Bundle Size Optimization (CRITICAL)

| Rule | Description |
|------|-------------|
| `bundle-barrel-imports` | Import directly, avoid barrel files |
| `bundle-dynamic-imports` | Use `next/dynamic` for heavy components |
| `bundle-defer-third-party` | Load analytics/logging after hydration |
| `bundle-conditional` | Load modules only when feature is activated |
| `bundle-preload` | Preload on hover/focus for perceived speed |

### 3. Server-Side Performance (HIGH)

| Rule | Description |
|------|-------------|
| `server-auth-actions` | Authenticate server actions like API routes |
| `server-cache-react` | Use `React.cache()` for per-request dedup |
| `server-cache-lru` | Use LRU cache for cross-request caching |
| `server-dedup-props` | Avoid duplicate serialization in RSC props |
| `server-serialization` | Minimize data passed to client components |
| `server-parallel-fetching` | Restructure components to parallelize fetches |
| `server-after-nonblocking` | Use `after()` for non-blocking operations |

### 4. Client-Side Data Fetching (MEDIUM-HIGH)

| Rule | Description |
|------|-------------|
| `client-swr-dedup` | Use SWR for automatic request deduplication |
| `client-event-listeners` | Deduplicate global event listeners |
| `client-passive-event-listeners` | Use passive listeners for scroll |
| `client-localstorage-schema` | Version and minimize localStorage data |

### 5. Re-render Optimization (MEDIUM)

| Rule | Description |
|------|-------------|
| `rerender-defer-reads` | Don't subscribe to state only used in callbacks |
| `rerender-memo` | Extract expensive work into memoized components |
| `rerender-memo-with-default-value` | Hoist default non-primitive props |
| `rerender-dependencies` | Use primitive dependencies in effects |
| `rerender-derived-state` | Subscribe to derived booleans, not raw values |
| `rerender-derived-state-no-effect` | Derive state during render, not effects |
| `rerender-functional-setstate` | Use functional setState for stable callbacks |
| `rerender-lazy-state-init` | Pass function to useState for expensive values |
| `rerender-simple-expression-in-memo` | Avoid memo for simple primitives |
| `rerender-move-effect-to-event` | Put interaction logic in event handlers |
| `rerender-transitions` | Use startTransition for non-urgent updates |
| `rerender-use-ref-transient-values` | Use refs for transient frequent values |

### 6. Rendering Performance (MEDIUM)

| Rule | Description |
|------|-------------|
| `rendering-animate-svg-wrapper` | Animate div wrapper, not SVG element |
| `rendering-content-visibility` | Use content-visibility for long lists |
| `rendering-hoist-jsx` | Extract static JSX outside components |
| `rendering-svg-precision` | Reduce SVG coordinate precision |
| `rendering-hydration-no-flicker` | Use inline script for client-only data |
| `rendering-hydration-suppress-warning` | Suppress expected mismatches |
| `rendering-activity` | Use Activity component for show/hide |
| `rendering-conditional-render` | Use ternary, not && for conditionals |
| `rendering-usetransition-loading` | Prefer useTransition for loading state |

### 7. JavaScript Performance (LOW-MEDIUM)

| Rule | Description |
|------|-------------|
| `js-batch-dom-css` | Group CSS changes via classes or cssText |
| `js-index-maps` | Build Map for repeated lookups |
| `js-cache-property-access` | Cache object properties in loops |
| `js-cache-function-results` | Cache function results in module-level Map |
| `js-cache-storage` | Cache localStorage/sessionStorage reads |
| `js-combine-iterations` | Combine multiple filter/map into one loop |
| `js-length-check-first` | Check array length before expensive ops |
| `js-early-exit` | Return early from functions |
| `js-hoist-regexp` | Hoist RegExp creation outside loops |
| `js-min-max-loop` | Use loop for min/max instead of sort |
| `js-set-map-lookups` | Use Set/Map for O(1) lookups |
| `js-tosorted-immutable` | Use toSorted() for immutability |

### 8. Advanced Patterns (LOW)

| Rule | Description |
|------|-------------|
| `advanced-event-handler-refs` | Store event handlers in refs |
| `advanced-init-once` | Initialize app once per app load |
| `advanced-use-latest` | useLatest for stable callback refs |

## How to Use

### Reading Individual Rules

Each rule file in `rules/` contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/rerender-memo.md
```

### Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

This 2900+ line document contains every rule with full code examples and detailed explanations, suitable for comprehensive reference.

## Key Patterns

### Parallel Data Fetching

```typescript
// Bad: sequential
const user = await fetchUser()
const posts = await fetchPosts()

// Good: parallel
const [user, posts] = await Promise.all([
  fetchUser(),
  fetchPosts()
])
```

### Dynamic Imports

```tsx
// Bad: bundles Monaco with main chunk
import { MonacoEditor } from './monaco-editor'

// Good: loads on demand
const MonacoEditor = dynamic(
  () => import('./monaco-editor').then(m => m.MonacoEditor),
  { ssr: false }
)
```

### Functional setState

```tsx
// Bad: stale closure risk
const addItem = useCallback((item) => {
  setItems([...items, item])
}, [items]) // recreates on every items change

// Good: always uses latest state
const addItem = useCallback((item) => {
  setItems(curr => [...curr, item])
}, []) // stable reference
```

## NEVER Do

1. **NEVER await** operations sequentially when they can run in parallel
2. **NEVER import** from barrel files (`import { X } from 'lib'`) — import directly
3. **NEVER skip** authentication in Server Actions — treat them like API routes
4. **NEVER pass** entire objects to client components when only one field is needed
5. **NEVER use** `&&` for conditional rendering with numbers — use ternary
6. **NEVER subscribe** to state only used in event handlers — read on demand
7. **NEVER mutate** arrays with `.sort()` — use `.toSorted()`
8. **NEVER put** initialization in `useEffect([])` — use module-level guard
