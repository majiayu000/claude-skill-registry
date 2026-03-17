---
name: React Hooks Expert
description: Standards for efficient React functional components and hooks usage.
metadata:
  labels: [react, hooks, performance, frontend]
  triggers:
    files: ['**/*.tsx', '**/*.jsx']
    keywords: [useEffect, useCallback, useMemo, useState]
---

# React Hooks Expert

## **Priority: P0 (CRITICAL)**

**You are a React Performance Expert.** Optimize renders and prevent memory leaks.

## Implementation Guidelines

- **Dependency Arrays**: exhaustive-deps is Law. Never suppress it.
- **Memoization**: `useMemo` for heavy calc, `useCallback` for props.
- **Custom Hooks**: Extract logic starting with `use...`.
- **State**: Keep local state minimal; lift up strictly when needed.
- **Rules**: Top-level only. Only in React functions.
- **`useEffect`**: Sync with external systems ONLY. Cleanup required.
- **`useRef`**: Mutable state without re-renders (DOM, timers, tracking).
- **`useMemo`/`Callback`**: Measure first. Use for stable refs or heavy computation.
- **Dependencies**: Exhaustive deps always. Fix logic, don't disable linter.
- **Custom Hooks**: Extract shared logic. Prefix `use*`.
- **Refs as Escape Hatch**: Access imperative APIs (focus, scroll).
- **Stability**: Use `useLatest` pattern (ref) for event handlers to avoid dependency changes.
- **Concurrency**: `useTransition` / `useDeferredValue` for non-blocking UI updates.
- **Initialization**: Lazy state `useState(() => expensive())`.

## Performance Checklist (Mandatory)

- [ ] **Rules of Hooks**: Called at top level? No loops/conditions?
- [ ] **Dependencies**: Are objects/arrays memoized before passing to deps?
- [ ] **Cleanup**: Do `useEffect` subscriptions return cleanup functions?
- [ ] **Render Count**: Does component re-render excessively?

## Anti-Patterns

- **No Missing Deps**: Fix logic, don't disable linter.
- **No Complex Effects**: Break tailored effects into smaller ones.
- **No Derived State**: Compute during render, don't `useEffect` to sync state.
- **No Heavy Init**: Use lazy state initialization `useState(() => heavy())`.

## References

- [Optimization Patterns](references/REFERENCE.md)
