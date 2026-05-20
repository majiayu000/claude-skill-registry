---
name: react-patterns
description: Provides comprehensive React 19 patterns covering Server Components, Actions, use() hook, useOptimistic, useFormStatus, useFormState, React Compiler, concurrent features, Suspense, and modern TypeScript development. Proactively use for any React development, component architecture, state management, performance optimization, or when implementing React 19's latest features.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# React Development Patterns

## Overview

Expert guide for building modern React 19 applications with new concurrent features, Server Components, Actions, and advanced patterns. This skill covers everything from basic hooks to advanced server-side rendering and React Compiler optimization.

## When to Use

- Building React 19 components with TypeScript/JavaScript
- Managing component state with useState and useReducer
- Handling side effects with useEffect
- Optimizing performance with useMemo and useCallback
- Creating custom hooks for reusable logic
- Implementing component composition patterns
- Working with refs using useRef
- Using React 19's new features (use(), useOptimistic, useFormStatus)
- Implementing Server Components and Actions
- Working with Suspense and concurrent rendering
- Building forms with new form hooks

## Instructions

1. **Identify Component Type**: Determine if Server Component or Client Component is needed
2. **Start with Hooks**: Use appropriate hooks for state management and side effects
3. **Implement Component Logic**: Build component with proper TypeScript typing
4. **Add Event Handlers**: Create stable references with useCallback where needed
5. **Optimize Performance**: Use useMemo for expensive computations
6. **Handle Errors**: Implement error boundaries for graceful error handling
7. **Test Components**: Write unit tests with React Testing Library

## Examples

### Server Component with Client Interaction

```tsx
// Server Component (default)
async function ProductPage({ id }: { id: string }) {
  const product = await db.product.findUnique({ where: { id } });

  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={product.id} />
    </div>
  );
}

// Client Component
'use client';
function AddToCartButton({ productId }: { productId: string }) {
  const [isPending, startTransition] = useTransition();

  const handleAdd = () => {
    startTransition(async () => {
      await addToCart(productId);
    });
  };

  return (
    <button onClick={handleAdd} disabled={isPending}>
      {isPending ? 'Adding...' : 'Add to Cart'}
    </button>
  );
}
```

## Constraints and Warnings

- **Server vs Client**: Server Components cannot use hooks, event handlers, or browser APIs
- **use() Hook**: Can only be called during render, not in callbacks or effects
- **Server Actions**: Must include 'use server' directive at the top of the file
- **State Mutations**: Never mutate state directly; always create new references
- **Effect Dependencies**: Always include all dependencies in useEffect arrays
- **Key Stability**: Use stable IDs for list keys, not array indices
- **Memory Leaks**: Always clean up subscriptions and event listeners in useEffect

## Core Hooks Patterns

### useState - State Management

Basic state declaration and updates:

```typescript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

State with initializer function (expensive computation):

```typescript
const [state, setState] = useState(() => {
  const initialState = computeExpensiveValue();
  return initialState;
});
```

Multiple state variables:

```typescript
function UserProfile() {
  const [name, setName] = useState('');
  const [age, setAge] = useState(0);
  const [email, setEmail] = useState('');
  
  return (
    <form>
      <input value={name} onChange={e => setName(e.target.value)} />
      <input type="number" value={age} onChange={e => setAge(Number(e.target.value))} />
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
    </form>
  );
}
```

### useEffect - Side Effects

Basic effect with cleanup:

```typescript
import { useEffect } from 'react';

function ChatRoom({ roomId }: { roomId: string }) {
  useEffect(() => {
    const connection = createConnection(roomId);
    connection.connect();
    
    // Cleanup function
    return () => {
      connection.disconnect();
    };
  }, [roomId]); // Dependency array
  
  return <div>Connected to {roomId}</div>;
}
```

Effect with multiple dependencies:

```typescript
function ChatRoom({ roomId, serverUrl }: { roomId: string; serverUrl: string }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    
    return () => connection.disconnect();
  }, [roomId, serverUrl]); // Re-run when either changes
  
  return <h1>Welcome to {roomId}</h1>;
}
```

Effect for subscriptions:

```typescript
function StatusBar() {
  const [isOnline, setIsOnline] = useState(true);
  
  useEffect(() => {
    function handleOnline() {
      setIsOnline(true);
    }
    
    function handleOffline() {
      setIsOnline(false);
    }
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []); // Empty array = run once on mount
  
  return <h1>{isOnline ? '✅ Online' : '❌ Disconnected'}</h1>;
}
```

### useRef - Persistent References

Storing mutable values without re-renders:

```typescript
import { useRef } from 'react';

function Timer() {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  
  const startTimer = () => {
    intervalRef.current = setInterval(() => {
      console.log('Tick');
    }, 1000);
  };
  
  const stopTimer = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };
  
  return (
    <>
      <button onClick={startTimer}>Start</button>
      <button onClick={stopTimer}>Stop</button>
    </>
  );
}
```

DOM element references:

```typescript
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  
  const focusInput = () => {
    inputRef.current?.focus();
  };
  
  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus Input</button>
    </>
  );
}
```

## Custom Hooks Pattern

Extract reusable logic into custom hooks:

```typescript
// useOnlineStatus.ts
import { useState, useEffect } from 'react';

export function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(true);
  
  useEffect(() => {
    function handleOnline() {
      setIsOnline(true);
    }
    
    function handleOffline() {
      setIsOnline(false);
    }
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);
  
  return isOnline;
}

// Usage in components
function StatusBar() {
  const isOnline = useOnlineStatus();
  return <h1>{isOnline ? '✅ Online' : '❌ Disconnected'}</h1>;
}

function SaveButton() {
  const isOnline = useOnlineStatus();
  return (
    <button disabled={!isOnline}>
      {isOnline ? 'Save' : 'Reconnecting...'}
    </button>
  );
}
```

Custom hook with parameters:

```typescript
// useChatRoom.ts
import { useEffect } from 'react';

interface ChatOptions {
  serverUrl: string;
  roomId: string;
}

export function useChatRoom({ serverUrl, roomId }: ChatOptions) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    
    return () => connection.disconnect();
  }, [serverUrl, roomId]);
}

// Usage
function ChatRoom({ roomId }: { roomId: string }) {
  const [serverUrl, setServerUrl] = useState('https://localhost:1234');
  
  useChatRoom({ serverUrl, roomId });
  
  return (
    <>
      <input value={serverUrl} onChange={e => setServerUrl(e.target.value)} />
      <h1>Welcome to {roomId}</h1>
    </>
  );
}
```

## Component Composition Patterns

### Props and Children

Basic component with props:

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
  children: React.ReactNode;
}

function Button({ variant = 'primary', size = 'md', onClick, children }: ButtonProps) {
  return (
    <button 
      className={`btn btn-${variant} btn-${size}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

Composition with children:

```typescript
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

function Card({ children, className = '' }: CardProps) {
  return (
    <div className={`card ${className}`}>
      {children}
    </div>
  );
}

// Usage
function UserProfile() {
  return (
    <Card>
      <h2>John Doe</h2>
      <p>Software Engineer</p>
    </Card>
  );
}
```

### Lifting State Up

Shared state between siblings:

```typescript
function Parent() {
  const [activeIndex, setActiveIndex] = useState(0);
  
  return (
    <>
      <Panel
        isActive={activeIndex === 0}
        onShow={() => setActiveIndex(0)}
      >
        Panel 1 content
      </Panel>
      <Panel
        isActive={activeIndex === 1}
        onShow={() => setActiveIndex(1)}
      >
        Panel 2 content
      </Panel>
    </>
  );
}

interface PanelProps {
  isActive: boolean;
  onShow: () => void;
  children: React.ReactNode;
}

function Panel({ isActive, onShow, children }: PanelProps) {
  return (
    <div>
      <button onClick={onShow}>Show</button>
      {isActive && <div>{children}</div>}
    </div>
  );
}
```

## Performance Optimization

### Avoid Unnecessary Effects

❌ Bad - Using effect for derived state:

```typescript
function TodoList({ todos }: { todos: Todo[] }) {
  const [visibleTodos, setVisibleTodos] = useState<Todo[]>([]);
  
  useEffect(() => {
    setVisibleTodos(todos.filter(t => !t.completed));
  }, [todos]); // Unnecessary effect
  
  return <ul>{/* ... */}</ul>;
}
```

✅ Good - Compute during render:

```typescript
function TodoList({ todos }: { todos: Todo[] }) {
  const visibleTodos = todos.filter(t => !t.completed); // Direct computation
  
  return <ul>{/* ... */}</ul>;
}
```

### useMemo for Expensive Computations

```typescript
import { useMemo } from 'react';

function DataTable({ data }: { data: Item[] }) {
  const sortedData = useMemo(() => {
    return [...data].sort((a, b) => a.name.localeCompare(b.name));
  }, [data]); // Only recompute when data changes
  
  return <table>{/* render sortedData */}</table>;
}
```

### useCallback for Function Stability

```typescript
import { useCallback } from 'react';

function Parent() {
  const [count, setCount] = useState(0);
  
  const handleClick = useCallback(() => {
    console.log('Clicked', count);
  }, [count]); // Recreate only when count changes
  
  return <ExpensiveChild onClick={handleClick} />;
}
```

## TypeScript Best Practices

### Type-Safe Props

```typescript
interface UserProps {
  id: string;
  name: string;
  email: string;
  age?: number; // Optional
}

function User({ id, name, email, age }: UserProps) {
  return (
    <div>
      <h2>{name}</h2>
      <p>{email}</p>
      {age && <p>Age: {age}</p>}
    </div>
  );
}
```

### Generic Components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Usage
<List 
  items={users}
  renderItem={(user) => <span>{user.name}</span>}
/>
```

### Event Handlers

```typescript
function Form() {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Handle form submission
  };
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} />
    </form>
  );
}
```

## Common Patterns

### Controlled Components

```typescript
function ControlledInput() {
  const [value, setValue] = useState('');
  
  return (
    <input 
      value={value}
      onChange={e => setValue(e.target.value)}
    />
  );
}
```

### Conditional Rendering

```typescript
function Greeting({ isLoggedIn }: { isLoggedIn: boolean }) {
  return (
    <div>
      {isLoggedIn ? (
        <UserGreeting />
      ) : (
        <GuestGreeting />
      )}
    </div>
  );
}
```

### Lists and Keys

```typescript
function UserList({ users }: { users: User[] }) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>
          {user.name}
        </li>
      ))}
    </ul>
  );
}
```

## Best Practices

### General React Best Practices

1. **Dependency Arrays**: Always specify correct dependencies in useEffect
2. **State Structure**: Keep state minimal and avoid redundant state
3. **Component Size**: Keep components small and focused
4. **Custom Hooks**: Extract complex logic into reusable custom hooks
5. **TypeScript**: Use TypeScript for type safety
6. **Keys**: Use stable IDs as keys for list items, not array indices
7. **Immutability**: Never mutate state directly
8. **Effects**: Use effects only for synchronization with external systems
9. **Performance**: Profile before optimizing with useMemo/useCallback

### React 19 Specific Best Practices

1. **Server Components**: Use Server Components for data fetching and static content
2. **Client Components**: Mark components as 'use client' only when necessary
3. **Actions**: Use Server Actions for mutations and form submissions
4. **Optimistic Updates**: Implement useOptimistic for better UX
5. **use() Hook**: Use for reading promises and context conditionally
6. **Form State**: Use useFormState and useFormStatus for complex forms
7. **Concurrent Features**: Leverage useTransition for non-urgent updates
8. **Error Boundaries**: Implement proper error handling with error boundaries

## Common Pitfalls

### General React Pitfalls

❌ **Missing Dependencies**:
```typescript
useEffect(() => {
  // Uses 'count' but doesn't include it in deps
  console.log(count);
}, []); // Wrong!
```

❌ **Mutating State**:
```typescript
const [items, setItems] = useState([]);
items.push(newItem); // Wrong! Mutates state
setItems(items); // Won't trigger re-render
```

✅ **Correct Approach**:
```typescript
setItems([...items, newItem]); // Create new array
```

### React 19 Specific Pitfalls

❌ **Using use() outside of render**:
```typescript
// Wrong!
function handleClick() {
  const data = use(promise); // Error: use() can only be called in render
}
```

✅ **Correct usage**:
```tsx
function Component({ promise }) {
  const data = use(promise); // Correct: called during render
  return <div>{data}</div>;
}
```

❌ **Forgetting 'use server' directive**:
```typescript
// Wrong - missing 'use server'
export async function myAction() {
  // This will run on the client!
}
```

✅ **Correct Server Action**:
```typescript
'use server'; // Must be at the top

export async function myAction() {
  // Now runs on the server
}
```

❌ **Mixing Server and Client logic incorrectly**:
```tsx
// Wrong - trying to use browser APIs in Server Component
export default async function ServerComponent() {
  const width = window.innerWidth; // Error: window is not defined
  return <div>{width}</div>;
}
```

✅ **Correct separation**:
```tsx
// Server Component for data
export default async function ServerComponent() {
  const data = await fetchData();
  return <ClientComponent data={data} />;
}

// Client Component for browser APIs
'use client';

function ClientComponent({ data }) {
  const [width, setWidth] = useState(window.innerWidth);
  // Handle resize logic...
  return <div>{width}</div>;
}
```

## React 19 New Features

### use() Hook - Reading Resources

The `use()` hook reads the value from a resource like a Promise or Context:

```typescript
import { use } from 'react';

// Reading a Promise in a component
function MessageComponent({ messagePromise }) {
  const message = use(messagePromise);
  return <p>{message}</p>;
}

// Reading Context conditionally
function Button() {
  if (condition) {
    const theme = use(ThemeContext);
    return <button className={theme}>Click</button>;
  }
  return <button>Click</button>;
}
```

### useOptimistic Hook - Optimistic UI Updates

Manage optimistic UI updates for async operations:

```typescript
import { useOptimistic } from 'react';

function TodoList({ todos, addTodo }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo) => [...state, newTodo]
  );

  const handleSubmit = async (formData) => {
    const newTodo = { id: Date.now(), text: formData.get('text') };

    // Optimistically add to UI
    addOptimisticTodo(newTodo);

    // Actually add to backend
    await addTodo(newTodo);
  };

  return (
    <form action={handleSubmit}>
      {optimisticTodos.map(todo => (
        <div key={todo.id}>{todo.text}</div>
      ))}
      <input type="text" name="text" />
      <button type="submit">Add Todo</button>
    </form>
  );
}
```

### useFormStatus Hook - Form State

Access form submission status from child components:

```typescript
import { useFormStatus } from 'react';

function SubmitButton() {
  const { pending, data } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}

function ContactForm() {
  return (
    <form action={submitForm}>
      <input name="email" type="email" />
      <SubmitButton />
    </form>
  );
}
```

### useFormState Hook - Form State Management

Manage form state with error handling:

```typescript
import { useFormState } from 'react';

async function submitAction(prevState: string | null, formData: FormData) {
  const email = formData.get('email') as string;

  if (!email.includes('@')) {
    return 'Invalid email address';
  }

  await submitToDatabase(email);
  return null;
}

function EmailForm() {
  const [state, formAction] = useFormState(submitAction, null);

  return (
    <form action={formAction}>
      <input name="email" type="email" />
      <button type="submit">Subscribe</button>
      {state && <p className="error">{state}</p>}
    </form>
  );
}
```

### Server Actions

Define server-side functions for form handling:

```typescript
// app/actions.ts
'use server';

import { redirect } from 'next/navigation';
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  // Validate input
  if (!title || !content) {
    return { error: 'Title and content are required' };
  }

  // Save to database
  const post = await db.post.create({
    data: { title, content }
  });

  // Update cache and redirect
  revalidatePath('/posts');
  redirect(`/posts/${post.id}`);
}
```

### Server Components

Components that run exclusively on the server:

```typescript
// app/posts/page.tsx - Server Component
async function PostsPage() {
  // Server-side data fetching
  const posts = await db.post.findMany({
    orderBy: { createdAt: 'desc' },
    take: 10
  });

  return (
    <div>
      <h1>Latest Posts</h1>
      <PostsList posts={posts} />
    </div>
  );
}

// Client Component for interactivity
'use client';

function PostsList({ posts }: { posts: Post[] }) {
  const [selectedId, setSelectedId] = useState<number | null>(null);

  return (
    <ul>
      {posts.map(post => (
        <li
          key={post.id}
          onClick={() => setSelectedId(post.id)}
          className={selectedId === post.id ? 'selected' : ''}
        >
          {post.title}
        </li>
      ))}
    </ul>
  );
}
```

## React Compiler

### Automatic Optimization

React Compiler automatically optimizes your components:

```typescript
// Before React Compiler - manual memoization needed
const ExpensiveComponent = memo(function ExpensiveComponent({
  data,
  onUpdate
}) {
  const processedData = useMemo(() => {
    return data.map(item => ({
      ...item,
      computed: expensiveCalculation(item)
    }));
  }, [data]);

  const handleClick = useCallback((id) => {
    onUpdate(id);
  }, [onUpdate]);

  return (
    <div>
      {processedData.map(item => (
        <Item
          key={item.id}
          item={item}
          onClick={handleClick}
        />
      ))}
    </div>
  );
});

// After React Compiler - no manual optimization needed
function ExpensiveComponent({ data, onUpdate }) {
  const processedData = data.map(item => ({
    ...item,
    computed: expensiveCalculation(item)
  }));

  const handleClick = (id) => {
    onUpdate(id);
  };

  return (
    <div>
      {processedData.map(item => (
        <Item
          key={item.id}
          item={item}
          onClick={handleClick}
        />
      ))}
    </div>
  );
}
```

### Installation and Setup

```bash
# Install React Compiler
npm install -D babel-plugin-react-compiler@latest

# Install ESLint plugin for validation
npm install -D eslint-plugin-react-hooks@latest
```

```javascript
// babel.config.js
module.exports = {
  plugins: [
    'babel-plugin-react-compiler', // Must run first!
    // ... other plugins
  ],
};
```

```javascript
// vite.config.js for Vite users
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: ['babel-plugin-react-compiler'],
      },
    }),
  ],
});
```

### Compiler Configuration

```javascript
// babel.config.js with compiler options
module.exports = {
  plugins: [
    [
      'babel-plugin-react-compiler',
      {
        // Enable compilation for specific files
        target: '18', // or '19'
        // Debug mode for development
        debug: process.env.NODE_ENV === 'development'
      }
    ],
  ],
};

// Incremental adoption with overrides
module.exports = {
  plugins: [],
  overrides: [
    {
      test: './src/components/**/*.{js,jsx,ts,tsx}',
      plugins: ['babel-plugin-react-compiler']
    }
  ]
};
```

## Advanced Server Components Patterns

### Mixed Server/Client Architecture

```typescript
// Server Component for data fetching
async function ProductPage({ id }: { id: string }) {
  const product = await fetchProduct(id);
  const related = await fetchRelatedProducts(id);

  return (
    <div>
      <ProductDetails product={product} />
      <ProductGallery images={product.images} />
      <RelatedProducts products={related} />
    </div>
  );
}

// Client Component for interactivity
'use client';

function ProductDetails({ product }: { product: Product }) {
  const [quantity, setQuantity] = useState(1);
  const [isAdded, setIsAdded] = useState(false);

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>${product.price}</p>

      <QuantitySelector
        value={quantity}
        onChange={setQuantity}
      />

      <AddToCartButton
        productId={product.id}
        quantity={quantity}
        onAdded={() => setIsAdded(true)}
      />

      {isAdded && <p>Added to cart!</p>}
    </div>
  );
}
```

### Server Actions with Validation

```typescript
'use server';

import { z } from 'zod';

const checkoutSchema = z.object({
  items: z.array(z.object({
    productId: z.string(),
    quantity: z.number().min(1)
  })),
  shippingAddress: z.object({
    street: z.string().min(1),
    city: z.string().min(1),
    zipCode: z.string().regex(/^\d{5}$/)
  }),
  paymentMethod: z.enum(['credit', 'paypal', 'apple'])
});

export async function processCheckout(
  prevState: any,
  formData: FormData
) {
  // Extract and validate data
  const rawData = {
    items: JSON.parse(formData.get('items') as string),
    shippingAddress: {
      street: formData.get('street'),
      city: formData.get('city'),
      zipCode: formData.get('zipCode')
    },
    paymentMethod: formData.get('paymentMethod')
  };

  const result = checkoutSchema.safeParse(rawData);

  if (!result.success) {
    return {
      error: 'Validation failed',
      fieldErrors: result.error.flatten().fieldErrors
    };
  }

  try {
    // Process payment
    const order = await createOrder(result.data);

    // Update inventory
    await updateInventory(result.data.items);

    // Send confirmation
    await sendConfirmationEmail(order);

    // Revalidate cache
    revalidatePath('/orders');

    return { success: true, orderId: order.id };
  } catch (error) {
    return { error: 'Payment failed' };
  }
}
```

## Concurrent Features

### useTransition for Non-Urgent Updates

```typescript
import { useTransition, useState } from 'react';

function SearchableList({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();
  const [filteredItems, setFilteredItems] = useState(items);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Update input immediately
    setQuery(e.target.value);

    // Transition the filter operation
    startTransition(() => {
      setFilteredItems(
        items.filter(item =>
          item.name.toLowerCase().includes(e.target.value.toLowerCase())
        )
      );
    });
  };

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={handleChange}
        placeholder="Search items..."
      />

      {isPending && <div className="loading">Filtering...</div>}

      <ul>
        {filteredItems.map(item => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### useDeferredValue for Expensive UI

```typescript
import { useDeferredValue, useMemo } from 'react';

function DataGrid({ data }: { data: DataRow[] }) {
  const [searchTerm, setSearchTerm] = useState('');
  const deferredSearchTerm = useDeferredValue(searchTerm);

  const filteredData = useMemo(() => {
    return data.filter(row =>
      Object.values(row).some(value =>
        String(value).toLowerCase().includes(deferredSearchTerm.toLowerCase())
      )
    );
  }, [data, deferredSearchTerm]);

  return (
    <div>
      <input
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
        placeholder="Search..."
        className={searchTerm !== deferredSearchTerm ? 'stale' : ''}
      />

      <DataGridRows
        data={filteredData}
        isStale={searchTerm !== deferredSearchTerm}
      />
    </div>
  );
}
```

## Testing React 19 Features

### Testing Server Actions

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { jest } from '@jest/globals';
import ContactForm from './ContactForm';

// Mock server action
const mockSubmitForm = jest.fn();

describe('ContactForm', () => {
  it('submits form with server action', async () => {
    render(<ContactForm />);

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    });

    fireEvent.click(screen.getByText('Submit'));

    expect(mockSubmitForm).toHaveBeenCalledWith(
      expect.any(FormData)
    );
  });

  it('shows loading state during submission', async () => {
    mockSubmitForm.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));

    render(<ContactForm />);

    fireEvent.click(screen.getByText('Submit'));

    expect(screen.getByText('Submitting...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Submit')).toBeInTheDocument();
    });
  });
});
```

### Testing Optimistic Updates

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { jest } from '@jest/globals';
import TodoList from './TodoList';

describe('useOptimistic', () => {
  it('shows optimistic update immediately', async () => {
    const mockAddTodo = jest.fn(() => new Promise(resolve => setTimeout(resolve, 100)));

    render(
      <TodoList
        todos={[]}
        addTodo={mockAddTodo}
      />
    );

    fireEvent.change(screen.getByPlaceholderText('Add a todo'), {
      target: { value: 'New todo' }
    });

    fireEvent.click(screen.getByText('Add'));

    // Optimistic update appears immediately
    expect(screen.getByText('New todo')).toBeInTheDocument();

    // Wait for actual submission
    await waitFor(() => {
      expect(mockAddTodo).toHaveBeenCalledWith({
        id: expect.any(Number),
        text: 'New todo'
      });
    });
  });
});
```

## Performance Best Practices

### React Compiler Guidelines

1. **Write Standard React Code**: The compiler works best with idiomatic React patterns
2. **Avoid Manual Memoization**: Let the compiler handle useMemo, useCallback, and memo
3. **Keep Components Pure**: Avoid side effects in render
4. **Use Stable References**: Pass stable objects as props

```typescript
// Good: Clean, idiomatic React
function ProductCard({ product, onAddToCart }) {
  const [quantity, setQuantity] = useState(1);

  const handleAdd = () => {
    onAddToCart(product.id, quantity);
  };

  return (
    <div>
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      <input
        type="number"
        value={quantity}
        onChange={e => setQuantity(Number(e.target.value))}
        min="1"
      />
      <button onClick={handleAdd}>Add to Cart</button>
    </div>
  );
}

// Avoid: Manual optimization
function ProductCard({ product, onAddToCart }) {
  const [quantity, setQuantity] = useState(1);

  const handleAdd = useCallback(() => {
    onAddToCart(product.id, quantity);
  }, [product.id, quantity, onAddToCart]);

  return (
    <div>
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      <QuantityInput
        value={quantity}
        onChange={setQuantity}
      />
      <button onClick={handleAdd}>Add to Cart</button>
    </div>
  );
}
```

### Server Components Best Practices

1. **Keep Server Components Server-Only**: No event handlers, hooks, or browser APIs
2. **Minimize Client Components**: Only use 'use client' when necessary
3. **Pass Data as Props**: Serialize data when passing from Server to Client
4. **Use Server Actions for Mutations**: Keep data operations on the server

```typescript
// Good: Server Component for static content
async function ProductPage({ id }: { id: string }) {
  const product = await fetchProduct(id);

  return (
    <article>
      <header>
        <h1>{product.name}</h1>
        <p>{product.description}</p>
      </header>

      <img
        src={product.imageUrl}
        alt={product.name}
        width={600}
        height={400}
      />

      <PriceDisplay price={product.price} />
      <AddToCartForm productId={product.id} />
    </article>
  );
}

// Client Component only for interactivity
'use client';

function AddToCartForm({ productId }: { productId: string }) {
  const [isAdding, setIsAdding] = useState(false);

  async function handleSubmit() {
    setIsAdding(true);
    await addToCart(productId);
    setIsAdding(false);
  }

  return (
    <form action={handleSubmit}>
      <button type="submit" disabled={isAdding}>
        {isAdding ? 'Adding...' : 'Add to Cart'}
      </button>
    </form>
  );
}
```

## Migration Guide

### From React 18 to 19

1. **Update Dependencies**:
```bash
npm install react@19 react-dom@19
```

2. **Adopt Server Components**:
   - Identify data-fetching components
   - Remove client-side code from Server Components
   - Add 'use client' directive where needed

3. **Replace Manual Optimistic Updates**:
```typescript
// Before
function TodoList({ todos, addTodo }) {
  const [optimisticTodos, setOptimisticTodos] = useState(todos);

  const handleAdd = async (text) => {
    const newTodo = { id: Date.now(), text };
    setOptimisticTodos([...optimisticTodos, newTodo]);
    await addTodo(newTodo);
  };
}

// After
function TodoList({ todos, addTodo }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo) => [...state, newTodo]
  );

  const handleAdd = async (formData) => {
    const newTodo = { id: Date.now(), text: formData.get('text') };
    addOptimisticTodo(newTodo);
    await addTodo(newTodo);
  };
}
```

4. **Enable React Compiler**:
   - Install babel-plugin-react-compiler
   - Remove manual memoization
   - Let the compiler optimize automatically

## References

- React 19 Official Docs: https://react.dev/blog/2024/04/25/react-19
- React Server Components: https://react.dev/reference/rsc/server-components
- React Compiler: https://react.dev/learn/react-compiler
- TypeScript with React: https://react-typescript-cheatsheet.netlify.app/
