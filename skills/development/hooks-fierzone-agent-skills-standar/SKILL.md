---
name: React Hooks
description: Best practices for React Hooks usage and custom hook creation.
metadata:
  labels: [react, hooks, custom-hooks, useeffect]
  triggers:
    files: ['**/*.tsx', '**/*.jsx']
    keywords: [useEffect, useCallback, useMemo, useRef, custom hook]
---

# React Hooks

## **Priority: P1 (OPERATIONAL)**

Effective usage of React Hooks.

## Implementation Guidelines

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

## Anti-Patterns

- **No Effects for Data Flow**: Derive state in render.
- **No Missing Deps**: Causes stale closures.
- **No Complex Effects**: Split into multiple simple effects.
- **No Oversubscription**: Check `why-did-you-render`.

## Code

```tsx
// Custom Hook
function useWindowSize() {
  const [size, setSize] = useState({ w: 0, h: 0 });

  useEffect(() => {
    function handleResize() {
      setSize({ w: window.innerWidth, h: window.innerHeight });
    }
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []); // Empty = mount only

  return size;
}

// Lazy Init
const [state, setState] = useState(() => computeExpensiveValue());
```

## Reference & Examples

See [references/REFERENCE.md](references/REFERENCE.md).
