---
name: react-19
description: React 19.2 features - use(), useOptimistic, useActionState, useEffectEvent, Activity component, React Compiler. Use when implementing React 19 patterns.
version: 19.2.0
user-invocable: true
references: references/new-hooks.md, references/activity-component.md, references/actions-api.md, references/react-compiler.md, references/ref-as-prop.md, references/context-improvements.md, references/suspense-patterns.md, references/document-metadata.md, references/resource-loading.md, references/migration-18-19.md, references/virtualization.md, references/lazy-loading.md, references/profiling.md, references/templates/action-form.md, references/templates/optimistic-update.md, references/templates/activity-tabs.md, references/templates/use-promise.md, references/templates/use-context.md, references/templates/use-effect-event.md, references/templates/error-boundary.md, references/templates/ref-as-prop.md, references/templates/document-metadata.md, references/templates/resource-loading.md, references/templates/virtual-list.md, references/templates/lazy-components.md, references/templates/profiling-devtools.md, references/hooks-improved.md, references/templates/use-deferred-value.md, references/templates/use-transition-async.md, references/use-state.md, references/use-effect.md, references/use-ref.md, references/use-memo.md, references/use-callback.md, references/use-layout-effect.md, references/use-id.md, references/use-imperative-handle.md, references/use-sync-external-store.md, references/custom-hooks-patterns.md, references/templates/state-patterns.md, references/templates/effect-patterns.md, references/templates/ref-patterns.md, references/templates/custom-hooks.md, references/templates/external-store.md
---

# React 19.2 Core Features

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing React patterns and component structure
2. **fuse-ai-pilot:research-expert** - Verify latest React 19.2 docs via Context7/Exa
3. **mcp__context7__query-docs** - Check use(), useOptimistic, useActionState, Activity patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## What's New in React 19.2

### New Hooks

| Hook | Purpose | Guide |
|------|---------|-------|
| `use()` | Read promises/context in render | `references/new-hooks.md` |
| `useOptimistic` | Optimistic UI updates | `references/new-hooks.md` |
| `useActionState` | Form action state management | `references/new-hooks.md` |
| `useFormStatus` | Form pending state (child components) | `references/new-hooks.md` |
| `useEffectEvent` | Non-reactive callbacks in effects | `references/new-hooks.md` |

→ See `references/new-hooks.md` for detailed usage

---

## Classic Hooks (React 18+)

### State Hooks

| Hook | Purpose | Guide |
|------|---------|-------|
| `useState` | Local component state | `references/use-state.md` |

→ For global state, see `react-state` skill

### Effect Hooks

| Hook | Purpose | Guide |
|------|---------|-------|
| `useEffect` | Side effects after paint | `references/use-effect.md` |
| `useLayoutEffect` | Sync DOM before paint | `references/use-layout-effect.md` |

### Ref Hooks

| Hook | Purpose | Guide |
|------|---------|-------|
| `useRef` | DOM access, mutable values | `references/use-ref.md` |
| `useImperativeHandle` | Customize ref API | `references/use-imperative-handle.md` |

### Performance Hooks (Rare with Compiler)

| Hook | Purpose | Guide |
|------|---------|-------|
| `useMemo` | Memoize expensive values | `references/use-memo.md` |
| `useCallback` | Memoize functions | `references/use-callback.md` |

→ React Compiler handles most memoization automatically

### Other Hooks

| Hook | Purpose | Guide |
|------|---------|-------|
| `useId` | Unique IDs for accessibility | `references/use-id.md` |
| `useSyncExternalStore` | External store subscription | `references/use-sync-external-store.md` |

### Custom Hooks

→ See `references/custom-hooks-patterns.md` for patterns
→ See `references/templates/custom-hooks.md` for implementations

---

### Activity Component (19.2)

Hide/show components while preserving state:

```typescript
<Activity mode={isActive ? 'visible' : 'hidden'}>
  <TabContent />
</Activity>
```

→ See `references/activity-component.md` for patterns

### React Compiler (19.1+)

Automatic memoization - useMemo/useCallback mostly obsolete:

- Build-time optimization
- No more manual memoization in most cases
- 2.5× faster interactions reported

→ See `references/react-compiler.md` for details

---

## Quick Reference

### use() Hook

```typescript
// Read promise in render (with Suspense)
const data = use(dataPromise)

// Read context conditionally (unique to use())
if (condition) {
  const theme = use(ThemeContext)
}
```

→ See `references/templates/use-promise.md`

### useOptimistic

```typescript
const [optimisticValue, setOptimistic] = useOptimistic(actualValue)
// Update UI immediately, server updates later
```

→ See `references/templates/optimistic-update.md`

### useActionState

```typescript
const [state, action, isPending] = useActionState(asyncFn, initialState)
```

→ See `references/templates/action-form.md`

### useEffectEvent (19.2)

```typescript
const onEvent = useEffectEvent(() => {
  // Always has fresh props/state, doesn't trigger re-run
})

useEffect(() => {
  connection.on('event', onEvent)
}, []) // No need to add onEvent to deps
```

→ See `references/new-hooks.md`

---

## Breaking Changes from 18

| Change | Migration |
|--------|-----------|
| `ref` is a prop | Remove `forwardRef` wrapper |
| `Context` is provider | Use `<Context value={}>` directly |
| `useFormStatus` | Import from `react-dom` |

→ See `references/migration-18-19.md`

---

## Best Practices

1. **Data fetching**: Use `use()` + Suspense, NOT useEffect
2. **Forms**: Use Actions + useActionState
3. **Optimistic UI**: Use `useOptimistic` for instant feedback
4. **Tabs/Modals**: Use `<Activity>` to preserve state
5. **Effect events**: Use `useEffectEvent` for non-reactive callbacks
6. **Memoization**: Let React Compiler handle it

---

## Templates

### React 19 Patterns

| Template | Use Case |
|----------|----------|
| `templates/action-form.md` | Form with useActionState |
| `templates/optimistic-update.md` | useOptimistic pattern |
| `templates/activity-tabs.md` | Activity component tabs |
| `templates/use-promise.md` | use() with promises |

### Classic Hooks Patterns

| Template | Use Case |
|----------|----------|
| `templates/state-patterns.md` | useState patterns |
| `templates/effect-patterns.md` | useEffect patterns |
| `templates/ref-patterns.md` | useRef patterns |
| `templates/custom-hooks.md` | Custom hooks implementations |
| `templates/external-store.md` | useSyncExternalStore patterns |

### Performance Patterns

| Template | Use Case |
|----------|----------|
| `templates/virtual-list.md` | TanStack Virtual for long lists |
| `templates/lazy-components.md` | Code splitting and lazy loading |
| `templates/profiling-devtools.md` | React DevTools Profiler |

---

## Performance

### Virtualization
Render only visible items for large lists (100+ items).
→ See `references/virtualization.md`

### Lazy Loading
Code split routes and heavy components for smaller bundles.
→ See `references/lazy-loading.md`

### Profiling
Measure render performance with DevTools Profiler.
→ See `references/profiling.md`

**Note:** With React Compiler (19.1+), manual memo/useMemo/useCallback optimizations are mostly obsolete. Profile first to verify if optimization is needed.

---

## Forbidden (Outdated Patterns)

- ❌ `useEffect` for data fetching → use `use()` + Suspense
- ❌ `forwardRef` → use `ref` as prop
- ❌ `<Context.Provider>` → use `<Context value={}>`
- ❌ Manual useMemo/useCallback everywhere → let Compiler handle it
- ❌ Conditional rendering for state preservation → use `<Activity>`
