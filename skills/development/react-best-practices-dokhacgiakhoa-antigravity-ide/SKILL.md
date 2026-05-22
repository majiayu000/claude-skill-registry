---
name: react-best-practices
description: React & Next.js engineering standards.
category: development
version: 4.1.0-fractal
layer: master-skill
---

# React & Next.js Best Practices

> **Goal**: Build high-performance, maintainable, and accessible React applications using modern patterns (React 19+, Next.js App Router).

## 1. Architecture & Rendering

- **App Router First**: Use Next.js App Router (`app/`) for all new projects.
- **Server Components (RSC)**: Default to Server Components. Only add `'use client'` when interactivity (state, hooks, event listeners) is strictly needed.
- **Suspense & Streaming**: Use `<Suspense>` boundaries to stream UI parts that depend on slow data.
- **Data Fetching**: Fetch data in Server Components directly (async/await components). Avoid `useEffect` for data fetching.

## 2. Component Patterns

- **Composition**: Use `children` prop to tackle prop drilling.
- **Atomic Design**: Organize components by atomicity (though feature-based folder structure is preferred for scale).
- **Custom Hooks**: Extract complex logic into `useHookName`.
- **Props**: Use strict TypeScript interfaces for props. Avoid `any`.

## 3. State Management

- **URL as State**: Store shareable state (filters, pagination) in URL Search Params.
- **Server State**: Use React Query (TanStack Query) or SWR for client-side data fetching/caching if RSC is not applicable.
- **Global State**: Minimal use of Zustand/Context. Prefer local state + composition.

## 4. Performance Optimization

- **Images**: Always use `next/image` with proper `width`, `height`, and `sizes`.
- **Fonts**: Use `next/font` to eliminate layout shift (CLS).
- **Lazy Loading**: Use `next/dynamic` or `React.lazy` for heavy client components below the fold.
- **Bundle Analysis**: Regularly check bundle size with `@next/bundle-analyzer`.

## 5. Styling

- **Tailwind CSS**: Use utility-first styling.
- **CN Utility**: Use `clsx` + `tailwind-merge` (typically `cn()` helper) for conditional class merging.
- **Mobile First**: Write styles for mobile first, then add `md:`, `lg:` prefixes.

## 6. Directory Structure (Feature-First)

```text
app/
├── (marketing)/     # Route group
├── dashboard/
│   ├── page.tsx
│   ├── layout.tsx
│   ├── _components/ # Private feature components
│   └── loading.tsx
components/          # Shared components (UI Kit)
lib/                 # Utilities and helpers
hooks/               # Shared hooks
types/               # Global types
```

## 7. Security

- **XSS**: React escapes by default, but be careful with `dangerouslySetInnerHTML`.
- **Auth**: Use `NextAuth.js` (Auth.js) or Clerk. Protect routes via Middleware.

---

**Checklist before PR**:
- [ ] Is `'use client'` used only where necessary?
- [ ] Are lists using stable `key` props?
- [ ] Is data fetched on the server where possible?
- [ ] Are images optimized?
