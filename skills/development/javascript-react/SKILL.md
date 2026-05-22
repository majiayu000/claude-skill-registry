---
name: javascript-react
description: Expert-level JavaScript and React development. Use when asked to (1) write JavaScript code requiring advanced patterns like closures, proxies, generators, or async iterators, (2) build React applications with hooks, context, suspense, or server components, (3) optimize JavaScript/React performance, (4) implement complex state management, (5) write TypeScript with advanced type patterns, or when phrases like "React component", "JavaScript function", "TypeScript", "hooks", "state management", "frontend", "web app" appear.
---

# Expert JavaScript & React Development

Write modern, performant, type-safe JavaScript and React code following current best practices.

## Core Principles

1. **Prefer composition over inheritance** - Use hooks, HOCs, and render props strategically
2. **Minimize re-renders** - Memoize appropriately, lift state only when necessary
3. **Type everything** - Use TypeScript for any non-trivial code
4. **Fail fast** - Validate inputs, use error boundaries, handle edge cases

## JavaScript Patterns

### Modern Syntax Defaults

```javascript
// Prefer const, use let only when reassignment needed
const config = { timeout: 5000 };
let count = 0;

// Destructuring with defaults
const { name, age = 18, ...rest } = user;
const [first, second, ...remaining] = items;

// Optional chaining and nullish coalescing
const value = obj?.deeply?.nested?.value ?? 'default';

// Template literals for complex strings
const query = `SELECT * FROM ${table} WHERE id = ${id}`;
```

### Async Patterns

```javascript
// Prefer async/await over raw promises
async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;
  }
}

// Parallel execution
const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);

// Sequential with error handling
const results = await Promise.allSettled([task1(), task2(), task3()]);
const successes = results.filter(r => r.status === 'fulfilled').map(r => r.value);
```

### Advanced patterns reference

See [references/modern-javascript.md](references/modern-javascript.md) for:
- Closures and module patterns
- Proxy and Reflect
- Generators and async iterators
- WeakMap/WeakSet for memory management
- Custom iterables

## React Patterns

### Component Structure

```tsx
// Functional components with TypeScript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  children,
}: ButtonProps) {
  return (
    <button
      className={cn(styles.button, styles[variant], styles[size])}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

### Hooks Best Practices

```tsx
// Custom hooks extract reusable logic
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// useMemo for expensive computations
const sortedItems = useMemo(
  () => items.slice().sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// useCallback for stable function references
const handleSubmit = useCallback(
  async (data: FormData) => {
    await submitForm(data);
    onSuccess();
  },
  [onSuccess]
);
```

### State Management Decision Tree

1. **Local UI state** → `useState`
2. **Complex local state with actions** → `useReducer`
3. **Shared state within subtree** → Context + `useReducer`
4. **Global app state** → Zustand, Jotai, or Redux Toolkit
5. **Server state (fetching/caching)** → TanStack Query or SWR

### Advanced React patterns reference

See [references/react-patterns.md](references/react-patterns.md) for:
- Compound components
- Render props and HOCs
- Controlled vs uncontrolled patterns
- Error boundaries
- Suspense and lazy loading
- Server components (React 19+)

## TypeScript Patterns

### Type Utilities

```typescript
// Discriminated unions for exhaustive checking
type Result<T> = { ok: true; value: T } | { ok: false; error: Error };

// Generic constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Conditional types
type Awaited<T> = T extends Promise<infer U> ? U : T;

// Template literal types
type EventName = `on${Capitalize<string>}`;
```

### Strict Configuration

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true
  }
}
```

## Performance Optimization

See [references/performance.md](references/performance.md) for comprehensive optimization strategies.

### Quick Reference

| Problem | Solution |
|---------|----------|
| Unnecessary re-renders | `React.memo`, `useMemo`, `useCallback` |
| Large bundle size | Code splitting, `React.lazy`, tree shaking |
| Slow lists | Virtualization (`@tanstack/react-virtual`) |
| Layout thrashing | `useLayoutEffect`, batch DOM reads |
| Memory leaks | Cleanup in `useEffect`, `AbortController` |

### Critical Anti-patterns

```tsx
// ❌ Creating objects/arrays in render
<Component style={{ color: 'red' }} items={[1, 2, 3]} />

// ✅ Stable references
const style = useMemo(() => ({ color: 'red' }), []);
const items = useMemo(() => [1, 2, 3], []);

// ❌ Index as key with dynamic lists
{items.map((item, i) => <Item key={i} {...item} />)}

// ✅ Stable unique keys
{items.map(item => <Item key={item.id} {...item} />)}
```

## Testing

See [references/testing.md](references/testing.md) for testing strategies.

### Testing Stack

- **Unit tests**: Vitest (fast, ESM-native)
- **Component tests**: React Testing Library
- **E2E tests**: Playwright
- **Type tests**: `tsd` or `expect-type`

### Testing Principles

1. Test behavior, not implementation
2. Prefer integration tests over unit tests
3. Mock at network boundary (MSW), not internal modules
4. Use realistic data with factories

## Project Structure

```
src/
├── components/       # Reusable UI components
│   └── Button/
│       ├── Button.tsx
│       ├── Button.test.tsx
│       └── index.ts
├── features/         # Feature-specific code
│   └── auth/
│       ├── components/
│       ├── hooks/
│       ├── api.ts
│       └── types.ts
├── hooks/           # Shared custom hooks
├── lib/             # Utilities and helpers
├── types/           # Shared TypeScript types
└── App.tsx
```

## Tooling Recommendations

| Category | Tool | Notes |
|----------|------|-------|
| Build | Vite | Fast dev, good defaults |
| Linting | ESLint + typescript-eslint | Use flat config |
| Formatting | Prettier | Or Biome for speed |
| Package manager | pnpm | Fast, disk efficient |
| Runtime validation | Zod | Infer TS types from schemas |
