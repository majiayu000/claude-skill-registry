---
name: react-typescript
description: Complete React TypeScript system. PROACTIVELY activate for: (1) Component props typing, (2) Event handler types, (3) Hooks with TypeScript, (4) Generic components, (5) forwardRef typing, (6) Context with type safety, (7) Utility types (Partial, Pick, Omit), (8) Discriminated unions for state. Provides: Props interfaces, event types, generic patterns, type-safe context, polymorphic components. Ensures type-safe React with proper TypeScript patterns.
---

## Quick Reference

| Type | Usage | Example |
|------|-------|---------|
| Props interface | Component props | `interface ButtonProps { variant: 'primary' }` |
| `ReactNode` | Children | `children: ReactNode` |
| `ChangeEvent` | Input change | `(e: ChangeEvent<HTMLInputElement>)` |
| `FormEvent` | Form submit | `(e: FormEvent<HTMLFormElement>)` |
| `MouseEvent` | Click | `(e: MouseEvent<HTMLButtonElement>)` |

| Pattern | Example |
|---------|---------|
| Extend HTML props | `extends ButtonHTMLAttributes<HTMLButtonElement>` |
| Generic component | `function List<T>({ items }: { items: T[] })` |
| forwardRef | `forwardRef<HTMLInputElement, Props>` |
| Discriminated union | `{ status: 'success'; data: T } \| { status: 'error'; error: Error }` |

| Utility Type | Purpose |
|--------------|---------|
| `Partial<T>` | All props optional |
| `Pick<T, K>` | Select specific props |
| `Omit<T, K>` | Exclude specific props |
| `ComponentProps<'button'>` | Get element props |

## When to Use This Skill

Use for **React TypeScript integration**:
- Typing component props and children
- Handling events with proper types
- Building generic reusable components
- Creating type-safe context and hooks
- Using utility types for prop manipulation
- Implementing polymorphic components

**For React basics**: see `react-fundamentals-19`

---

# React with TypeScript

## Component Props

### Basic Props Types

```tsx
// Inline props type
function Greeting({ name, age }: { name: string; age: number }) {
  return <p>Hello {name}, you are {age} years old</p>;
}

// Interface for props
interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;  // Optional prop
  role: 'admin' | 'user' | 'guest';  // Union type
}

function UserCard({ name, email, avatar, role }: UserCardProps) {
  return (
    <div className="user-card">
      {avatar && <img src={avatar} alt={name} />}
      <h3>{name}</h3>
      <p>{email}</p>
      <span className={`badge-${role}`}>{role}</span>
    </div>
  );
}

// Type alias
type ButtonVariant = 'primary' | 'secondary' | 'danger';
type ButtonSize = 'sm' | 'md' | 'lg';

type ButtonProps = {
  variant?: ButtonVariant;
  size?: ButtonSize;
  children: React.ReactNode;
  onClick?: () => void;
};

function Button({ variant = 'primary', size = 'md', children, onClick }: ButtonProps) {
  return (
    <button className={`btn btn-${variant} btn-${size}`} onClick={onClick}>
      {children}
    </button>
  );
}
```

### Children Props

```tsx
import { ReactNode, PropsWithChildren } from 'react';

// Using ReactNode
interface CardProps {
  title: string;
  children: ReactNode;
}

function Card({ title, children }: CardProps) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
}

// Using PropsWithChildren
type ContainerProps = PropsWithChildren<{
  className?: string;
}>;

function Container({ className, children }: ContainerProps) {
  return <div className={className}>{children}</div>;
}

// Render prop children
interface DataFetcherProps<T> {
  url: string;
  children: (data: T, loading: boolean) => ReactNode;
}

function DataFetcher<T>({ url, children }: DataFetcherProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  // ... fetch logic
  return <>{children(data as T, loading)}</>;
}
```

### Extending HTML Element Props

```tsx
import { ButtonHTMLAttributes, InputHTMLAttributes, forwardRef } from 'react';

// Extend button props
interface CustomButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  isLoading?: boolean;
}

const CustomButton = forwardRef<HTMLButtonElement, CustomButtonProps>(
  ({ variant = 'primary', isLoading, children, className, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={`btn btn-${variant} ${className || ''}`}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? 'Loading...' : children}
      </button>
    );
  }
);

CustomButton.displayName = 'CustomButton';

// Extend input props
interface TextInputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label: string;
  error?: string;
  size?: 'sm' | 'md' | 'lg';
}

const TextInput = forwardRef<HTMLInputElement, TextInputProps>(
  ({ label, error, size = 'md', className, ...props }, ref) => {
    return (
      <div className="form-field">
        <label>{label}</label>
        <input
          ref={ref}
          className={`input input-${size} ${error ? 'input-error' : ''} ${className || ''}`}
          {...props}
        />
        {error && <span className="error-message">{error}</span>}
      </div>
    );
  }
);

TextInput.displayName = 'TextInput';
```

### Polymorphic Components

```tsx
import { ElementType, ComponentPropsWithoutRef, ReactNode } from 'react';

type PolymorphicProps<E extends ElementType> = {
  as?: E;
  children: ReactNode;
} & Omit<ComponentPropsWithoutRef<E>, 'as' | 'children'>;

function Box<E extends ElementType = 'div'>({
  as,
  children,
  ...props
}: PolymorphicProps<E>) {
  const Component = as || 'div';
  return <Component {...props}>{children}</Component>;
}

// Usage
function App() {
  return (
    <>
      <Box>Default div</Box>
      <Box as="section" className="section">Section element</Box>
      <Box as="a" href="/about">Link element</Box>
      <Box as="button" onClick={() => console.log('clicked')}>Button</Box>
    </>
  );
}
```

## Event Handlers

### Common Event Types

```tsx
import {
  ChangeEvent,
  FormEvent,
  MouseEvent,
  KeyboardEvent,
  FocusEvent,
  DragEvent,
} from 'react';

function EventExamples() {
  // Input change
  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
  };

  // Select change
  const handleSelectChange = (e: ChangeEvent<HTMLSelectElement>) => {
    console.log(e.target.value);
  };

  // Form submit
  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    console.log(Object.fromEntries(formData));
  };

  // Button click
  const handleClick = (e: MouseEvent<HTMLButtonElement>) => {
    console.log(e.clientX, e.clientY);
  };

  // Keyboard
  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      console.log('Enter pressed');
    }
  };

  // Focus
  const handleFocus = (e: FocusEvent<HTMLInputElement>) => {
    console.log('Focused:', e.target.name);
  };

  // Drag
  const handleDragStart = (e: DragEvent<HTMLDivElement>) => {
    e.dataTransfer.setData('text/plain', 'dragging');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleInputChange} onKeyDown={handleKeyDown} onFocus={handleFocus} />
      <select onChange={handleSelectChange}>
        <option value="1">Option 1</option>
      </select>
      <div draggable onDragStart={handleDragStart}>Drag me</div>
      <button onClick={handleClick}>Submit</button>
    </form>
  );
}
```

### Event Handler Props

```tsx
interface FormFieldProps {
  onChange: (value: string) => void;
  onBlur?: () => void;
}

function FormField({ onChange, onBlur }: FormFieldProps) {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  return <input onChange={handleChange} onBlur={onBlur} />;
}

// Generic event handler
interface ListItemProps<T> {
  item: T;
  onSelect: (item: T) => void;
  onDelete?: (item: T) => void;
}

function ListItem<T extends { id: string; name: string }>({
  item,
  onSelect,
  onDelete,
}: ListItemProps<T>) {
  return (
    <li>
      <span onClick={() => onSelect(item)}>{item.name}</span>
      {onDelete && <button onClick={() => onDelete(item)}>Delete</button>}
    </li>
  );
}
```

## Hooks with TypeScript

### useState

```tsx
import { useState } from 'react';

// Inferred type
const [count, setCount] = useState(0);  // number

// Explicit type
const [user, setUser] = useState<User | null>(null);

// Union types
type Status = 'idle' | 'loading' | 'success' | 'error';
const [status, setStatus] = useState<Status>('idle');

// Complex state
interface FormState {
  name: string;
  email: string;
  errors: Record<string, string>;
}

const [form, setForm] = useState<FormState>({
  name: '',
  email: '',
  errors: {},
});

// Update partial state
setForm(prev => ({ ...prev, name: 'John' }));
```

### useReducer

```tsx
import { useReducer, Reducer } from 'react';

// State and action types
interface CounterState {
  count: number;
  step: number;
}

type CounterAction =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset' }
  | { type: 'setStep'; payload: number };

// Reducer function
const counterReducer: Reducer<CounterState, CounterAction> = (state, action) => {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step };
    case 'decrement':
      return { ...state, count: state.count - state.step };
    case 'reset':
      return { ...state, count: 0 };
    case 'setStep':
      return { ...state, step: action.payload };
    default:
      return state;
  }
};

function Counter() {
  const [state, dispatch] = useReducer(counterReducer, { count: 0, step: 1 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'setStep', payload: 5 })}>Set Step to 5</button>
    </div>
  );
}
```

### useRef

```tsx
import { useRef, useEffect } from 'react';

function RefExamples() {
  // DOM element ref
  const inputRef = useRef<HTMLInputElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Mutable value ref
  const countRef = useRef<number>(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    // Focus input on mount
    inputRef.current?.focus();

    // Access canvas context
    const ctx = canvasRef.current?.getContext('2d');
    if (ctx) {
      ctx.fillRect(0, 0, 100, 100);
    }

    // Start timer
    timerRef.current = setInterval(() => {
      countRef.current += 1;
    }, 1000);

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  return (
    <div>
      <input ref={inputRef} />
      <canvas ref={canvasRef} />
    </div>
  );
}
```

### useContext

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

// Theme context
interface Theme {
  primary: string;
  secondary: string;
  mode: 'light' | 'dark';
}

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleMode: () => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

// Provider
function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>({
    primary: '#007bff',
    secondary: '#6c757d',
    mode: 'light',
  });

  const toggleMode = () => {
    setTheme((prev) => ({
      ...prev,
      mode: prev.mode === 'light' ? 'dark' : 'light',
    }));
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleMode }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Hook with type safety
function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

// Usage
function ThemedButton() {
  const { theme, toggleMode } = useTheme();

  return (
    <button
      style={{ backgroundColor: theme.primary }}
      onClick={toggleMode}
    >
      Toggle {theme.mode === 'light' ? 'Dark' : 'Light'} Mode
    </button>
  );
}
```

### Custom Hooks

```tsx
import { useState, useEffect, useCallback } from 'react';

// Fetch hook with generics
interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Usage
interface User {
  id: number;
  name: string;
  email: string;
}

function UserProfile({ userId }: { userId: number }) {
  const { data: user, loading, error } = useFetch<User>(`/api/users/${userId}`);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>No user found</div>;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

## Generic Components

### Generic List

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => ReactNode;
  keyExtractor: (item: T) => string | number;
  emptyMessage?: string;
}

function List<T>({
  items,
  renderItem,
  keyExtractor,
  emptyMessage = 'No items',
}: ListProps<T>) {
  if (items.length === 0) {
    return <p>{emptyMessage}</p>;
  }

  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}

// Usage
interface Product {
  id: string;
  name: string;
  price: number;
}

function ProductList({ products }: { products: Product[] }) {
  return (
    <List
      items={products}
      keyExtractor={(product) => product.id}
      renderItem={(product) => (
        <div>
          <span>{product.name}</span>
          <span>${product.price}</span>
        </div>
      )}
    />
  );
}
```

### Generic Select

```tsx
interface SelectOption<T> {
  value: T;
  label: string;
}

interface SelectProps<T> {
  options: SelectOption<T>[];
  value: T | null;
  onChange: (value: T) => void;
  placeholder?: string;
  getOptionValue?: (option: SelectOption<T>) => string;
}

function Select<T>({
  options,
  value,
  onChange,
  placeholder = 'Select...',
  getOptionValue = (opt) => String(opt.value),
}: SelectProps<T>) {
  const selectedOption = options.find((opt) => opt.value === value);

  return (
    <select
      value={selectedOption ? getOptionValue(selectedOption) : ''}
      onChange={(e) => {
        const option = options.find(
          (opt) => getOptionValue(opt) === e.target.value
        );
        if (option) {
          onChange(option.value);
        }
      }}
    >
      <option value="" disabled>
        {placeholder}
      </option>
      {options.map((option) => (
        <option key={getOptionValue(option)} value={getOptionValue(option)}>
          {option.label}
        </option>
      ))}
    </select>
  );
}

// Usage
type Status = 'draft' | 'published' | 'archived';

function StatusSelect() {
  const [status, setStatus] = useState<Status | null>(null);

  const options: SelectOption<Status>[] = [
    { value: 'draft', label: 'Draft' },
    { value: 'published', label: 'Published' },
    { value: 'archived', label: 'Archived' },
  ];

  return <Select options={options} value={status} onChange={setStatus} />;
}
```

### Generic Table

```tsx
interface Column<T> {
  key: keyof T | string;
  header: string;
  render?: (item: T) => ReactNode;
  width?: string | number;
}

interface TableProps<T> {
  data: T[];
  columns: Column<T>[];
  keyExtractor: (item: T) => string | number;
  onRowClick?: (item: T) => void;
}

function Table<T extends Record<string, unknown>>({
  data,
  columns,
  keyExtractor,
  onRowClick,
}: TableProps<T>) {
  const getCellValue = (item: T, column: Column<T>): ReactNode => {
    if (column.render) {
      return column.render(item);
    }
    const value = item[column.key as keyof T];
    return value as ReactNode;
  };

  return (
    <table>
      <thead>
        <tr>
          {columns.map((column) => (
            <th key={String(column.key)} style={{ width: column.width }}>
              {column.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr
            key={keyExtractor(item)}
            onClick={() => onRowClick?.(item)}
            style={{ cursor: onRowClick ? 'pointer' : 'default' }}
          >
            {columns.map((column) => (
              <td key={String(column.key)}>{getCellValue(item, column)}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Usage
interface User {
  id: string;
  name: string;
  email: string;
  status: 'active' | 'inactive';
  createdAt: Date;
}

function UsersTable({ users }: { users: User[] }) {
  const columns: Column<User>[] = [
    { key: 'name', header: 'Name' },
    { key: 'email', header: 'Email' },
    {
      key: 'status',
      header: 'Status',
      render: (user) => (
        <span className={`badge badge-${user.status}`}>{user.status}</span>
      ),
    },
    {
      key: 'createdAt',
      header: 'Created',
      render: (user) => user.createdAt.toLocaleDateString(),
    },
  ];

  return (
    <Table
      data={users}
      columns={columns}
      keyExtractor={(user) => user.id}
      onRowClick={(user) => console.log('Clicked:', user)}
    />
  );
}
```

## Type Utilities

### Common Utility Types

```tsx
// Partial - all properties optional
interface User {
  id: string;
  name: string;
  email: string;
}

type PartialUser = Partial<User>;
// { id?: string; name?: string; email?: string }

// Required - all properties required
interface Config {
  host?: string;
  port?: number;
}

type RequiredConfig = Required<Config>;
// { host: string; port: number }

// Pick - select specific properties
type UserPreview = Pick<User, 'id' | 'name'>;
// { id: string; name: string }

// Omit - exclude specific properties
type CreateUserInput = Omit<User, 'id'>;
// { name: string; email: string }

// Record - object with specific key/value types
type UserRoles = Record<string, 'admin' | 'user' | 'guest'>;
// { [key: string]: 'admin' | 'user' | 'guest' }

// Extract - extract types from union
type Status = 'idle' | 'loading' | 'success' | 'error';
type LoadingStates = Extract<Status, 'loading' | 'idle'>;
// 'loading' | 'idle'

// Exclude - exclude types from union
type ErrorStates = Exclude<Status, 'success'>;
// 'idle' | 'loading' | 'error'
```

### Component Props Utilities

```tsx
import { ComponentProps, ComponentPropsWithRef, ComponentPropsWithoutRef } from 'react';

// Get props of a component
type ButtonProps = ComponentProps<'button'>;
type DivProps = ComponentProps<'div'>;

// Get props of a custom component
function MyButton(props: { variant: 'primary' | 'secondary' }) {
  return <button {...props} />;
}
type MyButtonProps = ComponentProps<typeof MyButton>;

// Props with ref
type InputPropsWithRef = ComponentPropsWithRef<'input'>;

// Props without ref
type InputPropsNoRef = ComponentPropsWithoutRef<'input'>;
```

### Discriminated Unions

```tsx
// API response states
type ApiResponse<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function useApiData<T>(url: string): ApiResponse<T> {
  // Implementation...
  return { status: 'idle' };
}

// Usage with type narrowing
function DataDisplay() {
  const response = useApiData<User[]>('/api/users');

  switch (response.status) {
    case 'idle':
      return <p>Ready to fetch</p>;
    case 'loading':
      return <p>Loading...</p>;
    case 'success':
      // TypeScript knows response.data exists here
      return <UserList users={response.data} />;
    case 'error':
      // TypeScript knows response.error exists here
      return <p>Error: {response.error.message}</p>;
  }
}
```

### Inference and Conditional Types

```tsx
// Infer return type
type ReturnTypeOf<T> = T extends (...args: any[]) => infer R ? R : never;

function fetchUser(id: string) {
  return { id, name: 'John', email: 'john@example.com' };
}

type FetchUserReturn = ReturnTypeOf<typeof fetchUser>;
// { id: string; name: string; email: string }

// Extract promise value
type Awaited<T> = T extends Promise<infer U> ? U : T;

async function getUsers() {
  return [{ id: '1', name: 'John' }];
}

type UsersData = Awaited<ReturnType<typeof getUsers>>;
// { id: string; name: string }[]

// Props inference from component
type PropsOf<T> = T extends React.ComponentType<infer P> ? P : never;
```

## Type-Safe Context

```tsx
import { createContext, useContext, ReactNode } from 'react';

// Create type-safe context factory
function createSafeContext<T>(displayName: string) {
  const Context = createContext<T | undefined>(undefined);
  Context.displayName = displayName;

  function useContextSafe() {
    const context = useContext(Context);
    if (context === undefined) {
      throw new Error(`use${displayName} must be used within ${displayName}Provider`);
    }
    return context;
  }

  return [Context.Provider, useContextSafe] as const;
}

// Usage
interface AuthContextValue {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const [AuthProvider, useAuth] = createSafeContext<AuthContextValue>('Auth');

// Provider component
function AuthContextProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    // Implementation
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthProvider value={{ user, login, logout }}>
      {children}
    </AuthProvider>
  );
}

// Consumer component - fully type-safe
function Profile() {
  const { user, logout } = useAuth();
  // TypeScript knows user can be null
  if (!user) return <p>Please log in</p>;

  return (
    <div>
      <p>Welcome, {user.name}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

## Best Practices

| Practice | Example |
|----------|---------|
| Use interface for component props | `interface ButtonProps { ... }` |
| Prefer type inference when obvious | `useState(0)` vs `useState<number>(0)` |
| Use generics for reusable components | `List<T>`, `Select<T>` |
| Discriminated unions for state | `{ status: 'success'; data: T }` |
| forwardRef with proper types | `forwardRef<HTMLButtonElement, Props>` |
| Avoid `any`, use `unknown` if needed | `catch (err: unknown)` |
| Use `as const` for literal types | `['a', 'b'] as const` |
