---
name: zustand
description: Zustand state management best practices for React applications. Use when writing, reviewing, or refactoring Zustand stores to ensure optimal performance and maintainability. Triggers on tasks involving state management, stores, selectors, re-renders, and Zustand patterns.
---

# Community Zustand Best Practices

Comprehensive performance and architecture guide for Zustand state management in React applications. Contains 43 rules across 8 categories, prioritized by impact from critical (store architecture, selector optimization) to incremental (advanced patterns).

## When to Apply

Reference these guidelines when:
- Creating new Zustand stores
- Optimizing re-render performance with selectors
- Implementing persistence or middleware
- Integrating Zustand with SSR/Next.js
- Reviewing code for state management patterns

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Store Architecture | CRITICAL | `store-` |
| 2 | Selector Optimization | CRITICAL | `select-` |
| 3 | Re-render Prevention | HIGH | `render-` |
| 4 | State Updates | MEDIUM-HIGH | `update-` |
| 5 | Middleware Configuration | MEDIUM | `mw-` |
| 6 | SSR and Hydration | MEDIUM | `ssr-` |
| 7 | TypeScript Patterns | LOW-MEDIUM | `ts-` |
| 8 | Advanced Patterns | LOW | `adv-` |

## Quick Reference

### 1. Store Architecture (CRITICAL)

- [`store-multiple-stores`](references/store-multiple-stores.md) - Use multiple small stores instead of one monolithic store
- [`store-separate-actions`](references/store-separate-actions.md) - Separate actions from state in dedicated namespace
- [`store-event-naming`](references/store-event-naming.md) - Name actions as events not setters
- [`store-colocate-logic`](references/store-colocate-logic.md) - Colocate actions with the state they modify
- [`store-avoid-derived-state`](references/store-avoid-derived-state.md) - Derive computed values instead of storing them
- [`store-domain-boundaries`](references/store-domain-boundaries.md) - Organize stores by feature domain

### 2. Selector Optimization (CRITICAL)

- [`select-always-use`](references/select-always-use.md) - Always use selectors never subscribe to entire store
- [`select-atomic-picks`](references/select-atomic-picks.md) - Use atomic selectors for single values
- [`select-stable-returns`](references/select-stable-returns.md) - Ensure selectors return stable references
- [`select-custom-hooks`](references/select-custom-hooks.md) - Export custom hooks not raw store
- [`select-auto-generate`](references/select-auto-generate.md) - Use auto-generated selectors for large stores
- [`select-memoize-computed`](references/select-memoize-computed.md) - Memoize expensive computed selectors
- [`select-avoid-inline`](references/select-avoid-inline.md) - Define selectors outside components

### 3. Re-render Prevention (HIGH)

- [`render-use-shallow`](references/render-use-shallow.md) - Use useShallow for multi-property selections
- [`render-equality-fn`](references/render-equality-fn.md) - Provide custom equality functions when needed
- [`render-memo-children`](references/render-memo-children.md) - Memo children affected by parent store updates
- [`render-subscribe-external`](references/render-subscribe-external.md) - Use subscribe for non-React consumers
- [`render-avoid-object-returns`](references/render-avoid-object-returns.md) - Avoid returning new objects from selectors
- [`render-split-components`](references/render-split-components.md) - Split components to minimize subscription scope

### 4. State Updates (MEDIUM-HIGH)

- [`update-functional-set`](references/update-functional-set.md) - Use functional form when updating based on previous state
- [`update-immutable`](references/update-immutable.md) - Never mutate state directly
- [`update-shallow-merge`](references/update-shallow-merge.md) - Understand set() shallow merge behavior
- [`update-async-actions`](references/update-async-actions.md) - Handle async actions with loading and error states
- [`update-batch-updates`](references/update-batch-updates.md) - Batch related updates in single set call

### 5. Middleware Configuration (MEDIUM)

- [`mw-devtools-actions`](references/mw-devtools-actions.md) - Name actions for DevTools debugging
- [`mw-persist-partialize`](references/mw-persist-partialize.md) - Use partialize for selective persistence
- [`mw-persist-migration`](references/mw-persist-migration.md) - Version and migrate persisted state
- [`mw-immer-nested`](references/mw-immer-nested.md) - Use immer for deeply nested state updates
- [`mw-combine-order`](references/mw-combine-order.md) - Apply middlewares in correct order
- [`mw-slice-middleware`](references/mw-slice-middleware.md) - Apply middleware at combined store level

### 6. SSR and Hydration (MEDIUM)

- [`ssr-skip-hydration`](references/ssr-skip-hydration.md) - Use skipHydration in SSR contexts
- [`ssr-manual-rehydrate`](references/ssr-manual-rehydrate.md) - Manually rehydrate on client mount
- [`ssr-hydration-hook`](references/ssr-hydration-hook.md) - Use custom hook to prevent hydration mismatch
- [`ssr-check-window`](references/ssr-check-window.md) - Guard browser APIs with typeof window check

### 7. TypeScript Patterns (LOW-MEDIUM)

- [`ts-state-creator`](references/ts-state-creator.md) - Use StateCreator for slice typing
- [`ts-middleware-inference`](references/ts-middleware-inference.md) - Preserve type inference with middleware
- [`ts-separate-types`](references/ts-separate-types.md) - Separate state and actions interfaces
- [`ts-generic-selectors`](references/ts-generic-selectors.md) - Type selectors for reusability
- [`ts-bound-store`](references/ts-bound-store.md) - Type combined stores correctly

### 8. Advanced Patterns (LOW)

- [`adv-context-stores`](references/adv-context-stores.md) - Combine Zustand with React Context for dependency injection
- [`adv-transient-updates`](references/adv-transient-updates.md) - Use subscribe for transient updates
- [`adv-computed-getters`](references/adv-computed-getters.md) - Implement computed state with getters
- [`adv-third-party-integration`](references/adv-third-party-integration.md) - Integrate with React Query and SWR

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
