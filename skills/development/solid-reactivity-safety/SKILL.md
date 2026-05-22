---
name: solid-reactivity-safety
description: "Solid reactivity safety: never destructure signals/stores/props, use getters and splitProps, keep render pure, use stable keys, and use children()/mergeProps for safe access."
metadata:
  globs:
    - "src/**/*"
---

# Solid Reactivity Safety

## Signals
- Do **not** destructure signals; always use getters.
  - ✅ `const [count, setCount] = createSignal(0); count();`
  - ❌ `const { count } = createSignal();`
- Keep render bodies pure: no side effects, no non-deterministic values (random/time) in JSX.
- Read signals inside reactive scopes (`createEffect`, `createMemo`) when you need derived values.

## Stores & Props
- Avoid destructuring reactive props/stores; access properties directly or with `splitProps`.
  - ✅ `const [local, others] = splitProps(props, ["title"]);`
  - ✅ `store.user.name` (fine-grained)
  - ❌ `const { user } = store;`
- Use `mergeProps` for defaults instead of spreading reactive objects into JSX.
- Use `children()` helper when accessing `props.children` multiple times or outside tracking; direct access is fine for a single pass.

## Derived Values
- Use `createMemo` for computed values; avoid recomputing in render.
- Don’t read signals in non-reactive closures that won’t rerun; wrap in `createEffect`/`createMemo`.

## Lists & Keys
- Use **stable keys** in `<For>`; prefer IDs, not array index or random.
- If data can reorder, never use `index` as key.

## Client-only & Guards
- Guard browser-only APIs with `if (!isServer)` or `typeof window !== "undefined"` before use.
- Use `onMount` for browser-only initialization.

## Quick Anti-Patterns to Avoid
- Destructuring signals/stores/props.
- Spreading reactive objects into JSX without care.
- Side effects in render bodies.
- Unstable IDs/keys or `Math.random()` in render.
