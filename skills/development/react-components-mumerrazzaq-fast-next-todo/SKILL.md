---
name: react-components
description: Build production-ready React components with TypeScript. Use when creating UI components (buttons, inputs, modals, cards), implementing hooks patterns, component composition, or setting up component documentation/testing. Covers accessibility, error boundaries, and performance optimization.
---

# React Components

## Component Patterns

### Presentational vs Container

```tsx
// Presentational: UI only, receives data via props
function UserCard({ name, avatar }: { name: string; avatar: string }) {
  return <div><img src={avatar} alt="" /><span>{name}</span></div>;
}

// Container: data fetching/state logic
function UserCardContainer({ userId }: { userId: string }) {
  const { data, isLoading } = useUser(userId);
  if (isLoading) return <Skeleton />;
  return <UserCard name={data.name} avatar={data.avatar} />;
}
```

### Props Interface Design

```tsx
// Extend native HTML attributes for proper typing
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

// Use forwardRef for components wrapping DOM elements
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', isLoading, children, ...props }, ref) => (
    <button ref={ref} disabled={isLoading} {...props}>{children}</button>
  )
);
Button.displayName = 'Button';
```

### Compound Components

```tsx
// Card with composable sub-components
const Card = ({ children }: { children: ReactNode }) => (
  <div className="card">{children}</div>
);
Card.Header = ({ children }: { children: ReactNode }) => (
  <div className="card-header">{children}</div>
);
Card.Body = ({ children }: { children: ReactNode }) => (
  <div className="card-body">{children}</div>
);

// Usage: <Card><Card.Header>Title</Card.Header><Card.Body>Content</Card.Body></Card>
```

## Hooks Best Practices

### useState

```tsx
// Lazy initialization for expensive computations
const [state, setState] = useState(() => computeExpensiveValue());

// Functional updates when new state depends on previous
setState(prev => prev + 1);
```

### useEffect

```tsx
// Always include cleanup for subscriptions/timers
useEffect(() => {
  const subscription = api.subscribe(handler);
  return () => subscription.unsubscribe();
}, [handler]);

// Move objects inside effect to avoid dependency issues
useEffect(() => {
  const options = { serverUrl, roomId };
  const connection = createConnection(options);
  connection.connect();
  return () => connection.disconnect();
}, [serverUrl, roomId]);
```

### useCallback/useMemo

```tsx
// useCallback: memoize functions passed to optimized children
const handleSubmit = useCallback((data: FormData) => {
  submitForm(data, userId);
}, [userId]);

// useMemo: cache expensive calculations
const sortedItems = useMemo(
  () => items.slice().sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// For context values to prevent re-renders
const contextValue = useMemo(() => ({ user, login }), [user, login]);
```

### Custom Hooks

```tsx
// Extract reusable logic
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage: const debouncedSearch = useDebounce(searchTerm, 300);
```

## Error Boundary

```tsx
import { Component, type ReactNode, type ErrorInfo } from 'react';

interface Props { children: ReactNode; fallback?: ReactNode; }
interface State { hasError: boolean; }

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('Error:', error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <div>Something went wrong.</div>;
    }
    return this.props.children;
  }
}
```

## Accessibility

### Required Patterns

```tsx
// Buttons: clear accessible name
<button aria-label="Close dialog">×</button>
<button aria-busy={isLoading} disabled={isLoading}>Submit</button>

// Form inputs: always associate labels
<label htmlFor={id}>{label}</label>
<input id={id} aria-invalid={!!error} aria-describedby={errorId} />
{error && <span id={errorId} role="alert">{error}</span>}

// Modals: focus trap + aria attributes
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">Dialog Title</h2>
</div>
```

### Keyboard Navigation

```tsx
// Handle Escape key for dismissible components
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') onClose();
};

// Focus trap in modals (Tab/Shift+Tab cycles within modal)
// See assets/Modal.tsx for full implementation
```

## Resources

### Templates

Copy from `assets/` directory:
- `Button.tsx` - Accessible button with variants, sizes, loading state
- `Input.tsx` - Form input with labels, validation, addons
- `Modal.tsx` - Accessible modal with focus trap, portal
- `Card.tsx` - Card with compound components pattern

### Documentation

- [Storybook setup](references/storybook.md) - CSF3 stories, decorators, interaction testing
- [Testing patterns](references/testing.md) - React Testing Library, MSW mocking
