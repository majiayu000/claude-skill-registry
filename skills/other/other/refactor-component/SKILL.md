---
name: refactor-component
description: Refactor React components for better maintainability, performance, or patterns. Covers hook extraction, component splitting, type safety, memoization, and composition.
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
