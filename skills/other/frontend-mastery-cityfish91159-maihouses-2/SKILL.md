---
name: frontend_mastery
description: Advanced React patterns, performance optimization, and state management rules.
allowed-tools: Read, Edit, Write
---

# Frontend Mastery Protocol (React + Vite + Tailwind)

## 1. Performance "Pro" Checklist

**Before submitting any UI component, verify:**

- [ ] **Re-renders**: Are we re-rendering unnecessarily? Use `React.memo` or `useCallback` for stable props.
- [ ] **Lazy Loading**: Are strict routes lazy-loaded? (`React.lazy`)
- [ ] **Image Optimization**: Are images using proper formats (WebP/AVIF) and `loading="lazy"`?
- [ ] **Zustand Selectors**: Are we selecting _only_ what we need?
  - ❌ `const { user, token } = useAuthStore()`
  - ✅ `const user = useAuthStore((s) => s.user)`
- [ ] **Bundle Size**: Did we import a huge library for one function? (e.g. import `lodash` vs `lodash/debounce`)

## 2. State Management Rules (Zustand + React Query)

- **Server State**: MUST use `React Query`.
  - NEVER store server data in global Zustand store manually (unless caching for UI sync).
  - Use `staleTime` and `cacheTime` appropriately.
- **Client State**: Use `Zustand` for global, `useState` for local.
  - Avoid "Prop Drilling" > 2 levels. Use Context or Zustand.

## 3. Architectectural Patterns

- **Container/Presenter**: Separate logic (Hooks) from View (JSX).
  - Complex components should have a custom hook (e.g., `useComponentLogic.ts`).
- **Composition**: Use `children` prop instead of passing components as props where possible.
- **Custom Hooks**: Extract reusable logic immediately. `useBoolean`, `useToggle`, etc.

## 4. Code Quality & Formatting

- **Naming**: `use[Action]` for hooks, `handle[Event]` for handlers.
- **CSS (Tailwind)**:
  - Group layout (`flex`, `grid`) first, then spacing, then visual (`bg`, `text`).
  - Use `clsx` or `tailwind-merge` for conditional classes.
  - NO inline styles (`style={{}}`) except for dynamic coordinates.

## 6. Error Boundaries

- Critical UI parts MUST have an `<ErrorBoundary>`.
- Async components (Suspense) must handle loading states gracefully.
