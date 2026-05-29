---
name: vani-async-client-only
description: Use async components, fallbacks, and client-only islands
---

# Async Components and Client-Only Islands

Instructions for async components with fallbacks and client-only rendering.

## When to Use

Use this when a component needs async setup or when a section should render only on the client.

## Steps

1. Define a component that returns a Promise of a render function.
2. Provide a `fallback` render function for DOM mode while async work runs.
3. Use `clientOnly: true` to skip SSR for a component and render it on the client.
4. Keep explicit updates for any local state changes after load.

## Arguments

- componentName - async component name (defaults to `AsyncCard`)
- includeFallback - whether to include a fallback (defaults to `true`)
- clientOnly - whether to mark the component as client-only (defaults to `false`)

## Examples

Example 1 usage pattern:

Render an async card with a loading fallback, then resolve to content.

Example 2 usage pattern:

Render a client-only widget inside an SSR page using `clientOnly: true`.

## Output

Example output:

```
Created: src/async-card.ts
Notes: Fallback renders in DOM mode; SSR awaits async components.
```

## Present Results to User

Clarify when the fallback appears, how client-only rendering behaves, and list file changes.
