---
name: react_perf_perfection
description: A "No-Compromise" React performance checklist enforcing strict re-render discipline and bundle auditing.
allowed-tools: Read, Edit
---

# React Performance Perfection Protocol

## 1. Re-render Police

- **Strict Rule**: Every `useEffect`, `useCallback`, and `useMemo` must have a **justified** dependency array.
- **Check**:
  - Are object/array props creating new references on every render? -> Use `useMemo`.
  - Are function props defined inline? -> Move to `useCallback` or outside component.
- **Tool**: If available, use `React DevTools Profiler` mental model (Why did this render?).

## 2. Bundle Diet

- **Strict Rule**: No "Barrel File" imports for massive libraries (e.g., `import { X } from 'lodash'`). Use direct paths (`import X from 'lodash/X'`) unless tree-shaking is verified.
- **Images**: No `import img from './large.png'`. Use lazy loading or external hosting.
- **Lazy Loading**: Route-level components MUST be lazy loaded (`React.lazy`).

## 3. The "Interaction to Next Paint" (INP) Rule

- **Heavy computations** (>50ms) must strictly be wrapped in `useTransition` or moved to a Web Worker.
- Blocking the main thread for UI updates is **Forbidden**.

## 4. Checklist Before Edit

- [ ] Will this change cause a parent re-render?
- [ ] Am I importing a huge library for a small utility?
- [ ] Is this state strictly local, or am I polluting the global store?
