---
name: react-patterns
description: React development patterns. Use when building React components, managing state, creating custom hooks, or optimizing React applications. Covers React 19 features, TypeScript integration, and composition patterns.
---

# React Patterns

> **Platform:** Web and Mobile (shared React patterns). For React Native-specific patterns (Pressable, ScrollView, FlashList, safe areas), see the **react-native-patterns** skill.

## Overview
Patterns for building maintainable React applications with TypeScript, leveraging React 19 features and composition patterns.

## Workflows

- [ ] Choose appropriate component composition pattern
- [ ] Apply TypeScript types for props and events
- [ ] Implement custom hooks for shared logic
- [ ] Add performance optimizations where needed
- [ ] Handle loading and error states with Suspense/boundaries
- [ ] Validate component render behavior

## Feedback Loops

- [ ] Components render without TypeScript errors
- [ ] Props are properly typed and validated
- [ ] Custom hooks have clear return types
- [ ] No unnecessary re-renders (use React DevTools Profiler)
- [ ] Error boundaries catch component errors
- [ ] Loading states work with Suspense

## Reference Implementation

### 1. Component Composition

#### Compound Components
```tsx
// Shares implicit state between parent and children
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function Tabs({ children, defaultTab }: { children: ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: ReactNode }) {
  return <div role="tablist">{children}</div>;
}

function Tab({ id, children }: { id: string; children: ReactNode }) {
  const ctx = use(TabsContext);
  if (!ctx) throw new Error('Tab must be used within Tabs');
  const { activeTab, setActiveTab } = ctx;

  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
}

// Usage
<Tabs defaultTab="profile">
  <TabList>
    <Tab id="profile">Profile</Tab>
    <Tab id="settings">Settings</Tab>
  </TabList>
</Tabs>
```

#### Render Props
```tsx
// Share logic while giving consumer render control
interface MousePosition {
  x: number;
  y: number;
}

function MouseTracker({ render }: { render: (pos: MousePosition) => ReactNode }) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

  useEffect(() => {
    const handleMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  return <>{render(position)}</>;
}

// Usage
<MouseTracker render={({ x, y }) => <p>Mouse at {x}, {y}</p>} />
```

#### Slot Pattern
```tsx
// Named slots for flexible composition
interface CardProps {
  header?: ReactNode;
  footer?: ReactNode;
  children: ReactNode;
}

function Card({ header, footer, children }: CardProps) {
  return (
    <div className="card">
      {header && <div className="card-header">{header}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

// Usage
<Card
  header={<h2>Title</h2>}
  footer={<button>Action</button>}
>
  Content here
</Card>
```

### 2. React 19 Features

#### use() Hook
```tsx
// Unwrap promises and context
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // Suspends until resolved
  return <div>{user.name}</div>;
}

// Context without useContext
function ThemedButton() {
  const theme = use(ThemeContext); // Simpler than useContext
  return <button className={theme}>Click</button>;
}
```

#### Actions and useActionState
```tsx
// Server actions with pending states
async function updateUser(prevState: { error?: string }, formData: FormData) {
  'use server';
  const name = formData.get('name') as string;
  // Validate and update...
  return { error: undefined };
}

function UserForm() {
  const [state, formAction, isPending] = useActionState(updateUser, {});

  return (
    <form action={formAction}>
      <input name="name" disabled={isPending} />
      {state.error && <p className="error">{state.error}</p>}
      <button disabled={isPending}>
        {isPending ? 'Saving...' : 'Save'}
      </button>
    </form>
  );
}
```

#### useOptimistic
```tsx
// Optimistic UI updates
function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, newTodo]
  );

  async function handleAdd(formData: FormData) {
    const todo = { id: crypto.randomUUID(), text: formData.get('text') as string };
    addOptimisticTodo(todo);
    await saveTodo(todo);
  }

  return (
    <form action={handleAdd}>
      {optimisticTodos.map(todo => <li key={todo.id}>{todo.text}</li>)}
      <input name="text" />
      <button>Add</button>
    </form>
  );
}
```

### 3. Custom Hooks

#### Object Return Pattern (multiple values)
```tsx
// Return object for named access
function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const login = async (credentials: Credentials) => {
    const user = await api.login(credentials);
    setUser(user);
  };

  return { user, loading, login, logout };
}

// Usage
const { user, login } = useAuth();
```

#### Tuple Return Pattern (2-3 values)
```tsx
// Return tuple for positional access (like useState)
function useToggle(initial = false): [boolean, () => void] {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue(v => !v), []);
  return [value, toggle];
}

// Usage
const [isOpen, toggleOpen] = useToggle();
```

#### Composing Hooks
```tsx
// Build complex hooks from simple ones
function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initial;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}

function useDarkMode() {
  const [isDark, setIsDark] = useLocalStorage('darkMode', false);

  useEffect(() => {
    document.body.classList.toggle('dark', isDark);
  }, [isDark]);

  return [isDark, setIsDark] as const;
}
```

### 4. TypeScript + React

#### Props Typing
```tsx
// Use interface for extensibility
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  loading?: boolean;
}

function Button({ variant = 'primary', loading, children, ...props }: ButtonProps) {
  return (
    <button className={variant} disabled={loading} {...props}>
      {loading ? 'Loading...' : children}
    </button>
  );
}
```

#### Generic Components
```tsx
// Type-safe data components
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Usage with full type inference
<List
  items={users}
  renderItem={user => <span>{user.name}</span>}
  keyExtractor={user => user.id}
/>
```

#### Refs as Props (React 19+)
```tsx
// React 19 simplifies ref forwarding - refs are regular props
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  ref?: React.Ref<HTMLInputElement>;
}

function Input({ label, ref, ...props }: InputProps) {
  return (
    <label>
      {label}
      <input ref={ref} {...props} />
    </label>
  );
}

// Usage - ref works like any other prop
function Form() {
  const inputRef = useRef<HTMLInputElement>(null);
  return <Input label="Name" ref={inputRef} />;
}
```

**Note**: `forwardRef` is deprecated in React 19. Use ref as a regular prop instead.

#### Event Handlers
```tsx
// Properly typed event handlers
function Form() {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    // Process formData...
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
  };

  return <form onSubmit={handleSubmit}><input onChange={handleChange} /></form>;
}
```

### 5. State Management

#### useReducer for Complex State
```tsx
// Better than multiple useState for related state
interface State {
  data: User[];
  loading: boolean;
  error: string | null;
}

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: User[] }
  | { type: 'FETCH_ERROR'; payload: string };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, loading: true, error: null };
    case 'FETCH_SUCCESS':
      return { ...state, loading: false, data: action.payload };
    case 'FETCH_ERROR':
      return { ...state, loading: false, error: action.payload };
  }
}

function UserList() {
  const [state, dispatch] = useReducer(reducer, {
    data: [],
    loading: false,
    error: null,
  });

  useEffect(() => {
    dispatch({ type: 'FETCH_START' });
    fetchUsers()
      .then(data => dispatch({ type: 'FETCH_SUCCESS', payload: data }))
      .catch(err => dispatch({ type: 'FETCH_ERROR', payload: err.message }));
  }, []);

  return <>{/* render state */}</>;
}
```

### 6. Performance Patterns

#### React.memo
```tsx
// Prevent re-renders when props haven't changed
interface ItemProps {
  item: Item;
  onDelete: (id: string) => void;
}

const ListItem = memo(function ListItem({ item, onDelete }: ItemProps) {
  console.log('Rendering', item.id);
  return (
    <li>
      {item.name}
      <button onClick={() => onDelete(item.id)}>Delete</button>
    </li>
  );
});

// Parent component
function List() {
  const [items, setItems] = useState<Item[]>([]);

  const handleDelete = useCallback((id: string) => {
    setItems(items => items.filter(item => item.id !== id));
  }, []);

  return (
    <>
      {items.map(item => (
        <ListItem key={item.id} item={item} onDelete={handleDelete} />
      ))}
    </>
  );
}
```

#### useMemo and useCallback
```tsx
// useMemo for expensive computations
function DataTable({ data }: { data: Row[] }) {
  const sortedData = useMemo(() => {
    console.log('Sorting...');
    return [...data].sort((a, b) => a.name.localeCompare(b.name));
  }, [data]);

  return <>{/* render sortedData */}</>;
}

// useCallback for stable function references
function Parent() {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []); // Stable reference

  return <MemoizedChild onClick={handleClick} />;
}
```

#### Code Splitting
```tsx
// Lazy load components
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### 7. Error Handling

#### Error Boundary
```tsx
// Catch rendering errors
interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <div>Something went wrong</div>;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<ErrorMessage />}>
  <App />
</ErrorBoundary>
```

#### Suspense for Loading
```tsx
// Handle async data loading
function UserProfile({ userId }: { userId: string }) {
  const user = use(fetchUser(userId)); // Suspends
  return <div>{user.name}</div>;
}

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <UserProfile userId="123" />
    </Suspense>
  );
}
```

## Best Practices

- **Composition over inheritance** - Use composition patterns for flexibility
- **Type everything** - Leverage TypeScript for compile-time safety
- **Colocate state** - Keep state as close to where it's used as possible
- **Extract custom hooks** - Share logic across components with hooks
- **Name hooks with use prefix** - Follow React naming conventions
- **Stable references** - Use useCallback/useMemo to prevent unnecessary re-renders
- **Error boundaries** - Wrap component trees to catch rendering errors
- **Suspense for loading** - Use Suspense instead of manual loading states
- **Server boundaries** - Mark client-only components with 'use client' directive
- **Avoid prop drilling** - Use context or composition for deeply nested props

## Anti-Patterns

- **Using forwardRef in React 19** - Use ref as a regular prop instead
- **Class components for new code** - Use function components and hooks
- **Mutating state directly** - Always use setState or reducer actions
- **Missing dependency arrays** - Include all dependencies in useEffect/useMemo/useCallback
- **Overusing useMemo/useCallback** - Only optimize when necessary (profile first)
- **Context for everything** - Use context sparingly; prefer props or state management library
- **Derived state in useState** - Compute derived values during render instead
- **useEffect for derived state** - Use useMemo or compute directly in render
- **Index as key** - Use stable unique IDs for list keys
- **Spreading {...props} blindly** - Be explicit about which props are passed down
- **Ignoring TypeScript errors** - Never use 'any' or '// @ts-ignore' as shortcuts
