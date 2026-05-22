---
name: react
description: React 19 performance optimization guidelines for concurrent rendering, Server Components, actions, hooks, and memoization (formerly react-19). This skill should be used when writing React 19 components, using concurrent features, or optimizing re-renders. This skill does NOT cover Next.js-specific features like App Router, next.config.js, or Next.js caching (use nextjs-16-app-router skill). For client-side form validation with React Hook Form, use react-hook-form skill.
---

# React 19 Best Practices

Comprehensive performance optimization guide for React 19 applications. Contains 40 rules across 8 categories, prioritized by impact from critical (concurrent rendering, server components) to incremental (component patterns).

## Table of Contents

1. [Concurrent Rendering](references/_sections.md#1-concurrent-rendering) — **CRITICAL**
   - 1.1 [Avoid Suspense Fallback Thrashing](references/conc-suspense-fallback.md) — HIGH (prevents flickering, smoother UX)
   - 1.2 [Leverage Automatic Batching for Fewer Renders](references/conc-automatic-batching.md) — HIGH (32% fewer renders in heavy updates)
   - 1.3 [Use useDeferredValue for Derived Expensive Values](references/conc-use-deferred-value.md) — CRITICAL (prevents jank in derived computations)
   - 1.4 [Use useTransition for Non-Blocking Updates](references/conc-use-transition.md) — CRITICAL (keeps UI responsive during heavy updates)
   - 1.5 [Write Concurrent-Safe Components](references/conc-concurrent-safe.md) — MEDIUM-HIGH (prevents bugs in concurrent rendering)
2. [Server Components](references/_sections.md#2-server-components) — **CRITICAL**
   - 2.1 [Avoid Client-Only Libraries in Server Components](references/rsc-avoid-client-only-libs.md) — MEDIUM-HIGH (prevents build errors, correct component placement)
   - 2.2 [Enable Streaming with Nested Suspense](references/rsc-streaming.md) — MEDIUM-HIGH (progressive loading, faster TTFB)
   - 2.3 [Fetch Data in Server Components](references/rsc-data-fetching-server.md) — CRITICAL (38% less client JS, no client waterfalls)
   - 2.4 [Minimize Server/Client Boundary Crossings](references/rsc-server-client-boundary.md) — CRITICAL (reduces serialization overhead, smaller bundles)
   - 2.5 [Pass Only Serializable Props to Client Components](references/rsc-serializable-props.md) — HIGH (prevents runtime errors, ensures correct hydration)
   - 2.6 [Use Composition to Mix Server and Client Components](references/rsc-composition-pattern.md) — HIGH (maintains server rendering for static content)
3. [Actions & Forms](references/_sections.md#3-actions-&-forms) — **HIGH**
   - 3.1 [Use Form Actions Instead of onSubmit](references/form-actions.md) — HIGH (progressive enhancement, simpler code)
   - 3.2 [Use useActionState for Form State Management](references/form-use-action-state.md) — HIGH (declarative form handling, automatic pending states)
   - 3.3 [Use useFormStatus for Submit Button State](references/form-use-form-status.md) — MEDIUM-HIGH (proper loading indicators, prevents double submission)
   - 3.4 [Use useOptimistic for Instant UI Feedback](references/form-use-optimistic.md) — HIGH (instant perceived response, auto-rollback on failure)
   - 3.5 [Validate Forms on Server with Actions](references/form-validation.md) — MEDIUM (secure validation, consistent error handling)
4. [Data Fetching](references/_sections.md#4-data-fetching) — **HIGH**
   - 4.1 [Fetch Data in Parallel with Promise.all](references/data-parallel-fetching.md) — MEDIUM-HIGH (eliminates waterfalls, 2-5× faster)
   - 4.2 [Use cache() for Request Deduplication](references/data-cache-deduplication.md) — HIGH (eliminates duplicate fetches per render)
   - 4.3 [Use Error Boundaries with Suspense](references/data-error-boundaries.md) — MEDIUM (graceful error recovery, isolated failures)
   - 4.4 [Use Suspense for Declarative Loading States](references/data-suspense-data-fetching.md) — HIGH (cleaner code, coordinated loading UI)
   - 4.5 [Use the use() Hook for Promises in Render](references/data-use-hook.md) — HIGH (cleaner async component code, Suspense integration)
5. [State Management](references/_sections.md#5-state-management) — **MEDIUM-HIGH**
   - 5.1 [Calculate Derived Values During Render](references/rstate-derived-values.md) — MEDIUM (eliminates sync bugs, simpler code)
   - 5.2 [Split Context to Prevent Unnecessary Re-renders](references/rstate-context-optimization.md) — MEDIUM (reduces re-renders from context changes)
   - 5.3 [Use Functional State Updates for Derived Values](references/rstate-functional-updates.md) — MEDIUM-HIGH (prevents stale closures, stable callbacks)
   - 5.4 [Use Lazy Initialization for Expensive Initial State](references/rstate-lazy-initialization.md) — MEDIUM-HIGH (prevents expensive computation on every render)
   - 5.5 [Use useReducer for Complex State Logic](references/rstate-use-reducer.md) — MEDIUM (clearer state transitions, easier testing)
6. [Memoization & Performance](references/_sections.md#6-memoization-&-performance) — **MEDIUM**
   - 6.1 [Avoid Premature Memoization](references/memo-avoid-premature.md) — MEDIUM (memoization has overhead, measure first)
   - 6.2 [Leverage React Compiler for Automatic Memoization](references/memo-compiler.md) — MEDIUM (automatic optimization, less manual code)
   - 6.3 [Use React.memo for Expensive Pure Components](references/memo-react-memo.md) — MEDIUM (skips re-render when props unchanged)
   - 6.4 [Use useCallback for Stable Function References](references/memo-use-callback.md) — MEDIUM (prevents child re-renders from reference changes)
   - 6.5 [Use useMemo for Expensive Calculations](references/memo-use-memo.md) — MEDIUM (skips expensive recalculation on re-renders)
7. [Effects & Events](references/_sections.md#7-effects-&-events) — **MEDIUM**
   - 7.1 [Always Clean Up Effect Side Effects](references/effect-cleanup.md) — MEDIUM (prevents memory leaks, stale callbacks)
   - 7.2 [Avoid Effects for Derived State and User Events](references/effect-avoid-unnecessary.md) — MEDIUM (eliminates sync bugs, simpler code)
   - 7.3 [Avoid Object and Array Dependencies in Effects](references/effect-object-dependencies.md) — MEDIUM (prevents infinite loops, unnecessary re-runs)
   - 7.4 [Use useEffectEvent for Non-Reactive Logic](references/effect-use-effect-event.md) — MEDIUM (separates reactive from non-reactive code)
   - 7.5 [Use useSyncExternalStore for External Subscriptions](references/effect-use-sync-external-store.md) — MEDIUM (correct subscription handling, SSR compatible)
8. [Component Patterns](references/_sections.md#8-component-patterns) — **LOW-MEDIUM**
   - 8.1 [Choose Controlled vs Uncontrolled Appropriately](references/rcomp-controlled-components.md) — LOW-MEDIUM (correct data flow, proper form handling)
   - 8.2 [Prefer Composition Over Props Explosion](references/rcomp-composition.md) — LOW-MEDIUM (more flexible, reusable components)
   - 8.3 [Use Key to Reset Component State](references/rcomp-key-reset.md) — LOW-MEDIUM (correct state isolation, proper resets)
   - 8.4 [Use Render Props for Inversion of Control](references/rcomp-render-props.md) — LOW-MEDIUM (flexible rendering, shared logic)

## References

1. [https://react.dev](https://react.dev)
2. [https://react.dev/blog/2024/12/05/react-19](https://react.dev/blog/2024/12/05/react-19)
3. [https://react.dev/blog/2025/10/01/react-19-2](https://react.dev/blog/2025/10/01/react-19-2)
4. [https://react.dev/learn/you-might-not-need-an-effect](https://react.dev/learn/you-might-not-need-an-effect)
5. [https://github.com/facebook/react](https://github.com/facebook/react)

## Related Skills

- For Next.js 16 App Router, see `nextjs-16-app-router` skill
- For client-side form handling, see `react-hook-form` skill
- For data caching with TanStack Query, see `tanstack-query` skill
