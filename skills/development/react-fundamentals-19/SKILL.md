---
name: react-fundamentals-19
description: Complete React 19 fundamentals system. PROACTIVELY activate for: (1) React 19 new features and changes, (2) Server vs Client Components, (3) Server Actions setup, (4) use() hook usage, (5) JSX and component basics, (6) Props and state patterns, (7) Suspense and Error Boundaries, (8) Fragments and Portals. Provides: React 19 syntax, Server Component patterns, async data handling, component composition, best practices. Ensures modern React 19 patterns with proper server/client architecture.
---

## Quick Reference

| Feature | Pattern | Example |
|---------|---------|---------|
| Server Component | Default (no directive) | `async function Page() {}` |
| Client Component | `'use client'` directive | `'use client'; function Counter() {}` |
| Server Action | `'use server'` directive | `async function submit(formData) {}` |
| use() hook | Read promises/context | `const data = use(promise)` |

| Concept | Syntax |
|---------|--------|
| Conditional render | `{condition && <Component />}` |
| List render | `{items.map(item => <Item key={item.id} />)}` |
| Props destructure | `function Card({ title, children }) {}` |
| State update | `setItems(prev => [...prev, newItem])` |

## When to Use This Skill

Use for **React 19 core concepts**:
- Learning React 19 new features and syntax
- Deciding between Server and Client Components
- Setting up Server Actions for forms
- Understanding the use() hook for async data
- Component composition and JSX patterns
- Error handling with Suspense and Error Boundaries

**For specific topics**: hooks → `react-hooks-complete`, state management → `react-state-management`, performance → `react-performance`

---

# React 19 Fundamentals

## Overview

React 19 (released December 2024) introduces significant improvements including the React Compiler, Server Components as first-class citizens, new hooks, and enhanced form handling.

## JSX and Components

### Function Components

```tsx
// Basic component
function Greeting({ name }: { name: string }) {
  return <h1>Hello, {name}!</h1>;
}

// With children
function Card({ children, title }: { children: React.ReactNode; title: string }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
}

// Arrow function component
const Button: React.FC<{ onClick: () => void; children: React.ReactNode }> = ({
  onClick,
  children,
}) => (
  <button onClick={onClick}>{children}</button>
);
```

### JSX Expressions

```tsx
function ProductCard({ product }: { product: Product }) {
  return (
    <div className="product">
      {/* Conditional rendering */}
      {product.onSale && <span className="badge">Sale!</span>}

      {/* Ternary */}
      {product.inStock ? (
        <button>Add to Cart</button>
      ) : (
        <span>Out of Stock</span>
      )}

      {/* Logical AND (short-circuit) */}
      {product.reviews.length > 0 && (
        <Reviews reviews={product.reviews} />
      )}

      {/* Mapping arrays */}
      <ul>
        {product.features.map((feature, index) => (
          <li key={feature.id || index}>{feature.name}</li>
        ))}
      </ul>

      {/* Nullish coalescing */}
      <span>{product.discount ?? 0}% off</span>
    </div>
  );
}
```

## Server vs Client Components

### Server Components (Default)

```tsx
// app/posts/page.tsx - Server Component by default
import { db } from '@/lib/db';

async function PostsPage() {
  // Direct database access - runs on server only
  const posts = await db.posts.findMany({
    orderBy: { createdAt: 'desc' },
  });

  return (
    <div>
      <h1>Posts</h1>
      {posts.map((post) => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </div>
  );
}

export default PostsPage;
```

### Client Components

```tsx
// components/Counter.tsx
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}
```

### Composing Server and Client Components

```tsx
// Server Component
import { db } from '@/lib/db';
import { LikeButton } from './LikeButton'; // Client Component

async function Post({ id }: { id: string }) {
  const post = await db.posts.findUnique({ where: { id } });

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
      {/* Client component for interactivity */}
      <LikeButton postId={id} initialLikes={post.likes} />
    </article>
  );
}
```

```tsx
// LikeButton.tsx - Client Component
'use client';

import { useState, useTransition } from 'react';
import { likePost } from './actions';

export function LikeButton({ postId, initialLikes }: { postId: string; initialLikes: number }) {
  const [likes, setLikes] = useState(initialLikes);
  const [isPending, startTransition] = useTransition();

  const handleLike = () => {
    startTransition(async () => {
      const newLikes = await likePost(postId);
      setLikes(newLikes);
    });
  };

  return (
    <button onClick={handleLike} disabled={isPending}>
      {isPending ? 'Liking...' : `Like (${likes})`}
    </button>
  );
}
```

## Server Actions

### Defining Server Actions

```tsx
// actions.ts
'use server';

import { db } from '@/lib/db';
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  await db.posts.create({
    data: { title, content },
  });

  revalidatePath('/posts');
}

export async function likePost(postId: string) {
  const post = await db.posts.update({
    where: { id: postId },
    data: { likes: { increment: 1 } },
  });

  return post.likes;
}
```

### Using Server Actions in Forms

```tsx
// Form with Server Action
import { createPost } from './actions';

function CreatePostForm() {
  return (
    <form action={createPost}>
      <input type="text" name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

### Using useActionState

```tsx
'use client';

import { useActionState } from 'react';
import { createPost } from './actions';

function CreatePostForm() {
  const [state, formAction, isPending] = useActionState(createPost, {
    error: null,
    success: false,
  });

  return (
    <form action={formAction}>
      <input type="text" name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />

      {state.error && <p className="error">{state.error}</p>}
      {state.success && <p className="success">Post created!</p>}

      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
}
```

## The use() Hook

### Reading Promises

```tsx
import { use, Suspense } from 'react';

// Fetch function that returns a promise
async function fetchComments(postId: string) {
  const res = await fetch(`/api/posts/${postId}/comments`);
  return res.json();
}

// Component that uses the promise
function Comments({ commentsPromise }: { commentsPromise: Promise<Comment[]> }) {
  const comments = use(commentsPromise);

  return (
    <ul>
      {comments.map((comment) => (
        <li key={comment.id}>{comment.text}</li>
      ))}
    </ul>
  );
}

// Parent component
function Post({ postId }: { postId: string }) {
  const commentsPromise = fetchComments(postId);

  return (
    <article>
      <h1>Post Title</h1>
      <Suspense fallback={<p>Loading comments...</p>}>
        <Comments commentsPromise={commentsPromise} />
      </Suspense>
    </article>
  );
}
```

### Reading Context Conditionally

```tsx
import { use } from 'react';
import { ThemeContext } from './ThemeContext';

function ThemedButton({ showTheme }: { showTheme: boolean }) {
  // use() can be called conditionally (unlike useContext)
  if (showTheme) {
    const theme = use(ThemeContext);
    return <button style={{ background: theme.primary }}>Themed</button>;
  }

  return <button>Default</button>;
}
```

## Props and State

### Props Patterns

```tsx
// Destructuring props
function UserCard({ user, onEdit, className = '' }: UserCardProps) {
  return (
    <div className={`user-card ${className}`}>
      <h3>{user.name}</h3>
      <button onClick={() => onEdit(user.id)}>Edit</button>
    </div>
  );
}

// Spreading props
function Button({ children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button {...props}>{children}</button>;
}

// Default props with TypeScript
interface CardProps {
  title: string;
  elevated?: boolean;
  padding?: 'sm' | 'md' | 'lg';
}

function Card({ title, elevated = false, padding = 'md' }: CardProps) {
  return (
    <div
      className={`card ${elevated ? 'elevated' : ''} padding-${padding}`}
    >
      <h2>{title}</h2>
    </div>
  );
}
```

### State Updates

```tsx
'use client';

import { useState } from 'react';

function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);

  // Functional update for derived state
  const addTodo = (text: string) => {
    setTodos((prev) => [
      ...prev,
      { id: Date.now(), text, completed: false },
    ]);
  };

  // Toggle item
  const toggleTodo = (id: number) => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  // Remove item
  const removeTodo = (id: number) => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => toggleTodo(todo.id)}
          />
          <span>{todo.text}</span>
          <button onClick={() => removeTodo(todo.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}
```

## Suspense and Error Boundaries

### Suspense for Loading States

```tsx
import { Suspense } from 'react';

function App() {
  return (
    <div>
      <h1>My App</h1>

      <Suspense fallback={<HeaderSkeleton />}>
        <Header />
      </Suspense>

      <Suspense fallback={<SidebarSkeleton />}>
        <Sidebar />
      </Suspense>

      <Suspense fallback={<ContentSkeleton />}>
        <MainContent />
      </Suspense>
    </div>
  );
}
```

### Error Boundaries

```tsx
'use client';

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary fallback={<ErrorPage />}>
      <MainContent />
    </ErrorBoundary>
  );
}
```

### React 19 Error Boundary Hook Pattern

```tsx
'use client';

import { useErrorBoundary } from 'react-error-boundary';

function DataLoader() {
  const { showBoundary } = useErrorBoundary();

  const loadData = async () => {
    try {
      const data = await fetchData();
      return data;
    } catch (error) {
      showBoundary(error);
    }
  };

  // ...
}
```

## Fragments and Portals

### Fragments

```tsx
// Short syntax
function List() {
  return (
    <>
      <li>Item 1</li>
      <li>Item 2</li>
    </>
  );
}

// With key (for mapping)
function DefinitionList({ items }: { items: { term: string; definition: string }[] }) {
  return (
    <dl>
      {items.map((item) => (
        <Fragment key={item.term}>
          <dt>{item.term}</dt>
          <dd>{item.definition}</dd>
        </Fragment>
      ))}
    </dl>
  );
}
```

### Portals

```tsx
'use client';

import { createPortal } from 'react-dom';
import { useEffect, useState } from 'react';

function Modal({ children, isOpen }: { children: ReactNode; isOpen: boolean }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted || !isOpen) return null;

  return createPortal(
    <div className="modal-overlay">
      <div className="modal-content">{children}</div>
    </div>,
    document.body
  );
}
```

## Best Practices

### 1. Component Organization

```
src/
  components/
    ui/              # Reusable UI components
      Button.tsx
      Card.tsx
    features/        # Feature-specific components
      auth/
        LoginForm.tsx
        SignupForm.tsx
    layout/          # Layout components
      Header.tsx
      Footer.tsx
  hooks/             # Custom hooks
    useAuth.ts
    useLocalStorage.ts
  lib/               # Utilities and helpers
    utils.ts
    api.ts
  types/             # TypeScript types
    index.ts
```

### 2. Naming Conventions

- Components: PascalCase (`UserProfile.tsx`)
- Hooks: camelCase with `use` prefix (`useAuth.ts`)
- Utilities: camelCase (`formatDate.ts`)
- Types: PascalCase (`User`, `ApiResponse`)

### 3. Key Prop Usage

```tsx
// Good - stable unique identifier
{items.map((item) => (
  <Item key={item.id} data={item} />
))}

// Avoid - index as key (unless list is static)
{items.map((item, index) => (
  <Item key={index} data={item} /> // Can cause issues with reordering
))}
```

### 4. Avoid Inline Object/Function Props

```tsx
// Bad - creates new object/function every render
<Component style={{ color: 'red' }} onClick={() => handleClick(id)} />

// Good - stable references
const style = useMemo(() => ({ color: 'red' }), []);
const handleClickMemo = useCallback(() => handleClick(id), [id]);
<Component style={style} onClick={handleClickMemo} />
```
