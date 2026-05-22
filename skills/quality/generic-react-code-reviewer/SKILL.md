---
name: generic-react-code-reviewer
description: Review React/TypeScript code for bugs, security vulnerabilities, performance issues, accessibility gaps, and CLAUDE.md workflow compliance. Enforces TypeScript strict mode, GPU-accelerated animations, WCAG AA accessibility, bundle size limits, and surgical simplicity. Use when completing features, before commits, or reviewing pull requests.
---

# React Code Reviewer

Review React/TypeScript code against production quality standards.

**Extends:** [Generic Code Reviewer](../generic-code-reviewer/SKILL.md) - Read base skill for full code review methodology, P0/P1/P2 priority system, and judgment calls.

## Pre-Commit Commands

```bash
npm run test        # Unit tests
npm run type-check  # TypeScript strict mode
npm run lint        # ESLint/Prettier
npm run build       # Production build
```

## React-Specific Checks

### TypeScript Strict Mode

```typescript
// Required tsconfig.json settings
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

- No `any` types for user input or API responses
- Validate external data with `unknown` first, then type guard
- Generic types over `any` in reusable utilities

### Component Patterns

| Pattern | Check                       |
| ------- | --------------------------- |
| Props   | Interface defined, no `any` |
| State   | Typed with Zustand/useState |
| Events  | Typed event handlers        |
| Refs    | `useRef<ElementType>(null)` |

### Hook Dependency Arrays

```typescript
// P1 Issue: Missing dependencies
useEffect(() => {
  fetchData(userId); // userId missing from deps
}, []); // ❌

// Correct
useEffect(() => {
  fetchData(userId);
}, [userId]); // ✓
```

**Rule:** Enable `react-hooks/exhaustive-deps` ESLint rule.

### State Management (Zustand/Redux)

- Store slices properly typed
- Actions return void (update state directly)
- Selectors memoized for derived state
- Large data (>1MB) in IndexedDB, not localStorage

### React Query/SWR Patterns

```typescript
// Proper typing
const { data } = useQuery<User>({
  queryKey: ["user", id],
  queryFn: () => fetchUser(id),
});

// Check: staleTime, cacheTime configured
// Check: error boundaries for query failures
```

## Performance (P1)

### Bundle Size Targets

| Target             | Threshold       |
| ------------------ | --------------- |
| Initial bundle     | < 100KB gzipped |
| Lazy-loaded chunks | < 50KB each     |
| Total JS           | < 300KB         |

### Lazy Loading

```typescript
// Heavy components (>20KB) MUST be lazy loaded
const HeavyChart = lazy(() => import('./HeavyChart'));
const RichTextEditor = lazy(() => import('./RichTextEditor'));

// Wrap in Suspense
<Suspense fallback={<Skeleton />}>
  <HeavyChart />
</Suspense>
```

### Memoization

```typescript
// Expensive calculations
const sortedItems = useMemo(() =>
  items.sort((a, b) => a.date - b.date),
  [items]
);

// Callback stability for child components
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

// Component memoization (when props are stable)
export const Item = memo(function Item({ data }: Props) {
  return <div>{data.name}</div>;
});
```

### Animation (GPU-Accelerated Only)

```css
/* ✓ DO animate */
transform: translateY(-4px);
opacity: 0.5;

/* ❌ NEVER animate */
width, height, margin, padding, top, left
```

## Accessibility (P1)

### Focus Management

```typescript
// Modal focus trapping
useEffect(() => {
  if (isOpen) {
    const firstFocusable = modalRef.current?.querySelector("button, input");
    firstFocusable?.focus();
  }
}, [isOpen]);

// Escape to close
useEffect(() => {
  const handleEscape = (e: KeyboardEvent) => {
    if (e.key === "Escape") onClose();
  };
  window.addEventListener("keydown", handleEscape);
  return () => window.removeEventListener("keydown", handleEscape);
}, [onClose]);
```

### ARIA in JSX

```tsx
// Icon-only buttons require labels
<button aria-label="Close modal">
  <X className="w-5 h-5" />
</button>

// Dialogs
<div role="dialog" aria-modal="true" aria-labelledby="title">
  <h2 id="title">Confirm Action</h2>
</div>
```

## Quick Review Checklist

**React-Specific (add to base checklist):**

- [ ] Hook dependencies correct
- [ ] Heavy components lazy loaded
- [ ] State management typed
- [ ] Memoization where beneficial
- [ ] Focus management in modals

## See Also

- [Generic Code Reviewer](../generic-code-reviewer/SKILL.md) - Base review methodology
- [Code Review Standards](../_shared/CODE_REVIEW_STANDARDS.md) - Full security/performance/accessibility
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - UI consistency
