---
name: tools-refactor
description: Refactor React components for better maintainability, performance, or patterns. Covers hook extraction, component splitting, type safety, memoization, and composition.
operating_mode: GENERATE
trigger_conditions: refactor, extract hook, split component, memoization, type safety, design tokens, component composition
related_skills: lp-do-build, tools-design-system, lp-design-qa
---

# Refactor Component

Improve existing components without changing behavior.

## Common Goals

1. Extract reusable logic into hooks
2. Split large components into sub-components
3. Simplify complex conditionals
4. Improve type safety
5. Apply design tokens (remove arbitrary values)
6. Add memoization for performance

## Patterns

### Extract Custom Hooks

```tsx
// Before: logic mixed in component
// After:
function useUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  // ... fetch logic
  return { users, loading, error }
}

function UserList() {
  const { users, loading, error } = useUsers()
  // ... render only
}
```

### Split Large Components

```tsx
// Before: 200+ line component with everything inline
// After: composed sub-components
function ProductCard({ product }) {
  return (
    <Card>
      <ProductImage src={product.image} alt={product.name} />
      <ProductInfo name={product.name} description={product.description} />
      <ProductActions price={product.price} />
    </Card>
  )
}
```

### Simplify Conditionals with Config Objects

```tsx
const statusConfig = {
  pending: { color: 'yellow', label: 'Pending' },
  approved: { color: 'green', label: 'Approved' },
} as const

function Status({ status }: { status: keyof typeof statusConfig }) {
  const config = statusConfig[status]
  return <Badge color={config.color}>{config.label}</Badge>
}
```

### Improve Type Safety

```tsx
// Before: untyped props
function Card({ user }) { ... }

// After: explicit interface
interface CardProps { user: User; onEdit?: (user: User) => void }
function Card({ user, onEdit }: CardProps) { ... }
```

### Memoization

```tsx
const processed = useMemo(() =>
  items.filter(i => i.type === filter).sort((a, b) => a.name.localeCompare(b.name)),
  [items, filter]
)

const Item = memo(({ name }: { name: string }) => <div>{name}</div>)
```

### Composition over Props

```tsx
// Before: flat prop drilling (title, content, footer)
// After: compound component
<Modal isOpen onClose={close}>
  <Modal.Header>Title</Modal.Header>
  <Modal.Body>Content</Modal.Body>
  <Modal.Footer>Actions</Modal.Footer>
</Modal>
```

## Checklist

- [ ] Tests still pass after refactor
- [ ] No regression in functionality
- [ ] Improved readability
- [ ] Better type safety
- [ ] Uses design tokens (no arbitrary values)
- [ ] Follows architectural layer rules
- [ ] Performance improved (if that was the goal)

## Entry Criteria

Invoke `tools-refactor` when at least one of the following is true:

- A QA report from `lp-design-qa` contains at least one finding citing: arbitrary CSS values (inline styles, hard-coded px/rem, Tailwind arbitrary classes), missing semantic tokens, or component structure issues (over-nesting, prop drilling, missing composition patterns).
- A sweep report from `tools-ui-contrast-sweep` (`contrast-sweep-report.md`) contains at least one actionable token-level fix (e.g., replace hard-coded color with semantic token).
- A sweep report from `tools-ui-breakpoint-sweep` (`breakpoint-sweep-report.md`) contains at least one layout fix requiring component restructuring (not just CSS class adjustments).
- Operator directs a refactor explicitly (no minimum findings threshold required).

**Minimum threshold:** at least 1 qualifying finding from any upstream QA source, OR explicit operator direction.

## Integration

- **Upstream:** QA reports from `lp-design-qa`, `tools-ui-contrast-sweep` (`contrast-sweep-report.md`), and `tools-ui-breakpoint-sweep` (`breakpoint-sweep-report.md`); or explicit operator direction.
- **Downstream:** `lp-do-build` (refactored components committed and verified); human PR review.
- **Loop position:** S9D (Conditional Refactor) — post-sweep QA, pre-merge. Skip if no QA findings meet the Entry Criteria above.
