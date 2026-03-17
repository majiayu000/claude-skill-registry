---
name: component-design
description: Design React/Vue components following atomic design and composition
  patterns. Use when creating UI components.
---

# Component Design Skill

## Purpose
Create consistent, reusable UI components.

## Atomic Design
Reference: [patterns/atomic-design.md](patterns/atomic-design.md)

### Hierarchy
1. **Atoms**: Basic elements (Button, Input, Label)
2. **Molecules**: Simple groups (FormField, SearchBox)
3. **Organisms**: Complex sections (Header, Form, Card)
4. **Templates**: Page layouts
5. **Pages**: Specific instances

## Component Patterns
Reference: [patterns/composition.md](patterns/composition.md)

### Compound Components
```tsx
<Select>
  <Select.Trigger />
  <Select.Content>
    <Select.Item value="1">Option 1</Select.Item>
  </Select.Content>
</Select>
```

### Render Props
```tsx
<DataFetcher url="/api/users">
  {({ data, loading }) => (
    loading ? <Spinner /> : <UserList users={data} />
  )}
</DataFetcher>
```

### Custom Hooks
```tsx
function useUser(id: string) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  // ...
  return { user, loading, error };
}
```

## Props Interface
```tsx
interface ButtonProps {
  /** Visual variant of the button */
  variant?: 'primary' | 'secondary' | 'ghost';
  /** Size of the button */
  size?: 'sm' | 'md' | 'lg';
  /** Whether button is disabled */
  disabled?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Button content */
  children: React.ReactNode;
}
```

## Component Template
Use: [templates/component-template.tsx](templates/component-template.tsx)

## State Management
Reference: [patterns/state-management.md](patterns/state-management.md)

### Decision Tree
1. UI-only state → `useState`
2. Complex local state → `useReducer`
3. Shared between siblings → Lift to parent
4. Shared across app → Context or global store
5. Server state → React Query/SWR
