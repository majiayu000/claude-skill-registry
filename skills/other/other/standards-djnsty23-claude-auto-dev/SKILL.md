---
name: standards
description: Type safety, design tokens, UI states, React/Next.js patterns from production.
user-invocable: false
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
model: opus
---

# Code Standards

Senior developer judgment. Patterns learned from production.

## Core Standards

1. **Correct** — It works. Types pass, builds succeed, features function.
2. **Clear** — Easy to read. Names obvious, flow simple, matches patterns.
3. **Complete** — Handles reality. Errors, edge cases, all UI states.

## All UI States

Every component handles: `loading → error → empty → content`

```tsx
if (isLoading) return <Skeleton />;
if (error) return <ErrorState message={error.message} />;
if (!data?.length) return <EmptyState />;
return <Content data={data} />;
```

## Responsive Layout

Every page works at 3 breakpoints: mobile (375px), tablet (768px), desktop (1280px+).

- Sidebars: hidden or collapsible on mobile (`md:block hidden`)
- Grids: stack to single column (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`)
- Navigation: hamburger or bottom nav on mobile
- Touch targets: minimum 44x44px
- No horizontal overflow or clipped content
- Modals/drawers: full-screen on mobile, centered on desktop

## Frontend Engineering

### Accessibility
- `<button>` for actions, `<a>`/`<Link>` for navigation (not `<div onClick>`)
- Icon-only buttons need `aria-label`
- Form controls need `<label>` or `aria-label`
- Images need `alt` (or `alt=""` if decorative)
- Interactive elements need keyboard handlers

### Focus & Interaction
- Visible focus: `focus-visible:ring-*` (not bare `outline-none`)
- Hover states on all interactive elements
- `touch-action: manipulation` on touch targets

### Forms
- Correct `type` and `inputmode` on inputs
- `autocomplete` on form fields
- Do not block paste
- Errors inline next to fields; focus first error on submit
- Disable spellcheck on emails, codes, usernames

### Animation
- Honor `prefers-reduced-motion`
- Only animate `transform`/`opacity` (compositor-friendly)
- List properties explicitly (not `transition: all`)
- Animations must be interruptible

### Hydration Safety (Next.js/RSC)
- Inputs with `value` need `onChange` (or use `defaultValue`)
- Guard date/time rendering against hydration mismatch
- Server Components by default; `'use client'` only for state/effects/handlers

### Images & Performance
- `<img>` needs explicit `width` and `height` (prevents CLS)
- Below-fold: `loading="lazy"`; above-fold: `priority` or `fetchpriority="high"`
- Large lists (50+): virtualize with `virtua` or `content-visibility: auto`

## Type Safety

| Rule | Wrong | Right |
|------|-------|-------|
| No `any` or `@ts-ignore` | `data as any` | Proper typing |
| Single source of truth | Define type in 3 files | Define once, import |
| Complete Records | Missing union members | Include all members |
| Supabase typing | Untyped `.insert()` | `Database['table']['Insert']` |
| Safe access | `obj[key]` | `'key' in obj && ...` |

## React Patterns

| Rule | Wrong | Right |
|------|-------|-------|
| No nested interactives | `<button><button>` | `role="button"` |
| Hooks at top level | `onClick={() => useState()}` | Hooks in component body |
| No conditional hooks | `if (x) useEffect()` | `useEffect(() => { if (x) })` |

## Error Handling

```typescript
// Auth errors
if (error?.error_type === 'reauth_required') {
  toast.error('Session expired');
}

// Storage quota
try {
  localStorage.setItem(key, value);
} catch (e) {
  if (e.name === 'QuotaExceededError') {
    toast.error('Storage full');
  }
}
```

## Query Keys

```typescript
export const queryKeys = {
  reports: {
    all: ['reports'] as const,
    detail: (id: string) => ['reports', id] as const,
  }
} as const;
```

## React/Next.js Optimization Priority

Fix in this order — earlier items have bigger impact:

### 1. Eliminate Waterfalls
```typescript
// Bad - sequential (600ms)
const user = await getUser(id);
const posts = await getPosts(id);

// Good - parallel (200ms)
const [user, posts] = await Promise.all([getUser(id), getPosts(id)]);
```
- Use `Promise.all()` for independent operations
- Use `React.cache()` for per-request deduplication
- Wrap slow components in `<Suspense>` for streaming

### 2. Bundle Size
- Avoid barrel files (`index.ts` re-exports) — they prevent tree-shaking
- Dynamic import heavy components: `dynamic(() => import('./Chart'), { ssr: false })`
- Direct imports: `import format from 'date-fns/format'` not `import { format } from 'date-fns'`
- Mark `'use client'` as low as possible in the component tree

### 3. Server Performance
- Server Components by default
- `React.cache()` to deduplicate identical server-side fetches
- `Cache-Control` headers for static data
- Avoid serializing large objects across server/client boundary

### 4. Client Data Fetching
- SWR or React Query over raw `useEffect` + `fetch`
- Optimistic updates for mutations
- Prefer uncontrolled inputs for forms
- Add `staleTime` to avoid refetching on every mount

### 5. Re-render Optimization (do last)
- Lift state up only as far as needed
- `useCallback` for handlers passed to memoized children
- Split context providers by update frequency
- Lazy state initialization: `useState(() => expensiveComputation())`

### 6. Component Architecture
```tsx
// Bad - boolean prop explosion
<Card isCompact isHighlighted hasBorder isClickable />

// Good - composition
<Card variant="compact">
  <Card.Highlight>Content</Card.Highlight>
</Card>
```
- Prefer composition over boolean props
- Eliminate `forwardRef` (React 19+), use `use()` instead of `useContext()`

## Anti-Patterns (Flag These)

- `user-scalable=no` or `maximum-scale=1`
- `transition: all`
- `outline-none` without focus-visible replacement
- `<div>`/`<span>` with click handlers (should be `<button>`)
- Images without dimensions
- Form inputs without labels
- Hardcoded date/number formats (use `Intl.*`)
- Hardcoded colors (use semantic tokens: `text-foreground`, not `text-gray-500`)
- Spacing with arbitrary values (use scale: `p-4`, not `p-[15px]`)

## Design System

- Semantic tokens only (`text-foreground`, `bg-background`, `text-muted-foreground`)
- Spacing scale (`p-4`, not `p-[15px]`)
- Reuse components — create variants for differences

## Mistake Logging

Log errors to `.claude/mistakes.md`:

```markdown
## [Category]: [Description]
**Task:** ID
**Error:** What
**Fix:** How
**Prevention:** Rule
```

Categories: `Type Safety`, `React`, `API`, `Performance`, `A11y`

## Token Efficiency

Be concise. Short responses = more runway.
- Do not repeat file contents
- Do not explain what you're about to do
- Just do it, report briefly
