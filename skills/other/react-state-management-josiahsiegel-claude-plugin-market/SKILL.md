---
name: react-state-management
description: Complete React state management system. PROACTIVELY activate for: (1) Context API patterns and optimization, (2) Zustand store setup and usage, (3) Jotai atomic state, (4) TanStack Query (React Query) for server state, (5) SWR data fetching, (6) useState vs useReducer decisions, (7) State normalization, (8) Avoiding prop drilling. Provides: Store configuration, context optimization, server state caching, optimistic updates, infinite queries. Ensures scalable state architecture with proper tool selection.
---

## Quick Reference

| Library | Best For | Install |
|---------|----------|---------|
| Context | Small apps, themes | Built-in |
| Zustand | Simple global state | `npm i zustand` |
| Jotai | Atomic/granular state | `npm i jotai` |
| TanStack Query | Server state/caching | `npm i @tanstack/react-query` |
| SWR | Data fetching | `npm i swr` |

| Scenario | Recommended |
|----------|-------------|
| Simple local state | `useState` |
| Complex local state | `useReducer` |
| Shared state (small app) | Context + useReducer |
| Shared state (large app) | Zustand or Jotai |
| Server state | TanStack Query or SWR |

## When to Use This Skill

Use for **state management decisions**:
- Choosing between state management solutions
- Setting up Zustand, Jotai, or Context stores
- Configuring TanStack Query for server state
- Implementing optimistic updates
- Normalizing complex state structures
- Avoiding unnecessary re-renders

**For React hooks basics**: see `react-hooks-complete`

---

# React State Management

## Built-in State Management

### Component State with useState

```tsx
'use client';

import { useState } from 'react';

function ShoppingCart() {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  const addItem = (product: Product) => {
    setItems((prev) => {
      const existing = prev.find((item) => item.id === product.id);
      if (existing) {
        return prev.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };

  const total = items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>
        Cart ({items.length}) - ${total.toFixed(2)}
      </button>
      {isOpen && <CartDropdown items={items} />}
    </div>
  );
}
```

### Complex State with useReducer

```tsx
'use client';

import { useReducer, Dispatch, createContext, useContext } from 'react';

// Types
interface CartState {
  items: CartItem[];
  isLoading: boolean;
  error: string | null;
}

type CartAction =
  | { type: 'ADD_ITEM'; payload: Product }
  | { type: 'REMOVE_ITEM'; payload: string }
  | { type: 'UPDATE_QUANTITY'; payload: { id: string; quantity: number } }
  | { type: 'CLEAR_CART' }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string };

// Reducer
function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existing = state.items.find(
        (item) => item.id === action.payload.id
      );
      if (existing) {
        return {
          ...state,
          items: state.items.map((item) =>
            item.id === action.payload.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          ),
        };
      }
      return {
        ...state,
        items: [...state.items, { ...action.payload, quantity: 1 }],
      };
    }
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter((item) => item.id !== action.payload),
      };
    case 'UPDATE_QUANTITY':
      return {
        ...state,
        items: state.items.map((item) =>
          item.id === action.payload.id
            ? { ...item, quantity: action.payload.quantity }
            : item
        ),
      };
    case 'CLEAR_CART':
      return { ...state, items: [] };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
}

// Context
const CartContext = createContext<{
  state: CartState;
  dispatch: Dispatch<CartAction>;
} | null>(null);

// Provider
export function CartProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, {
    items: [],
    isLoading: false,
    error: null,
  });

  return (
    <CartContext.Provider value={{ state, dispatch }}>
      {children}
    </CartContext.Provider>
  );
}

// Hook
export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
}
```

## Context API

### Creating and Using Context

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

// Theme context
interface Theme {
  colors: { primary: string; secondary: string; background: string };
  spacing: { sm: number; md: number; lg: number };
}

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleDarkMode: () => void;
  isDark: boolean;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

const lightTheme: Theme = {
  colors: { primary: '#3b82f6', secondary: '#8b5cf6', background: '#ffffff' },
  spacing: { sm: 8, md: 16, lg: 24 },
};

const darkTheme: Theme = {
  colors: { primary: '#60a5fa', secondary: '#a78bfa', background: '#1f2937' },
  spacing: { sm: 8, md: 16, lg: 24 },
};

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [isDark, setIsDark] = useState(false);
  const [theme, setTheme] = useState<Theme>(lightTheme);

  const toggleDarkMode = () => {
    setIsDark((prev) => !prev);
    setTheme(isDark ? lightTheme : darkTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleDarkMode, isDark }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
```

### Optimizing Context Performance

```tsx
import { createContext, useContext, useMemo, useCallback, useState } from 'react';

// Split context to prevent unnecessary re-renders
const UserContext = createContext<User | null>(null);
const UserActionsContext = createContext<{
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  updateProfile: (data: Partial<User>) => Promise<void>;
} | null>(null);

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback(async (email: string, password: string) => {
    const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    const userData = await response.json();
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    setUser(null);
  }, []);

  const updateProfile = useCallback(async (data: Partial<User>) => {
    const response = await fetch('/api/profile', {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
    const updated = await response.json();
    setUser(updated);
  }, []);

  // Memoize actions object
  const actions = useMemo(
    () => ({ login, logout, updateProfile }),
    [login, logout, updateProfile]
  );

  return (
    <UserContext.Provider value={user}>
      <UserActionsContext.Provider value={actions}>
        {children}
      </UserActionsContext.Provider>
    </UserContext.Provider>
  );
}

// Separate hooks for data and actions
export function useUser() {
  return useContext(UserContext);
}

export function useUserActions() {
  const context = useContext(UserActionsContext);
  if (!context) {
    throw new Error('useUserActions must be used within UserProvider');
  }
  return context;
}
```

## Zustand

### Basic Zustand Store

```tsx
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';

interface CartStore {
  items: CartItem[];
  addItem: (product: Product) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  total: () => number;
}

export const useCartStore = create<CartStore>()(
  devtools(
    persist(
      (set, get) => ({
        items: [],

        addItem: (product) =>
          set((state) => {
            const existing = state.items.find((item) => item.id === product.id);
            if (existing) {
              return {
                items: state.items.map((item) =>
                  item.id === product.id
                    ? { ...item, quantity: item.quantity + 1 }
                    : item
                ),
              };
            }
            return { items: [...state.items, { ...product, quantity: 1 }] };
          }),

        removeItem: (id) =>
          set((state) => ({
            items: state.items.filter((item) => item.id !== id),
          })),

        updateQuantity: (id, quantity) =>
          set((state) => ({
            items: state.items.map((item) =>
              item.id === id ? { ...item, quantity } : item
            ),
          })),

        clearCart: () => set({ items: [] }),

        total: () =>
          get().items.reduce(
            (sum, item) => sum + item.price * item.quantity,
            0
          ),
      }),
      { name: 'cart-storage' }
    )
  )
);

// Usage in component
function CartButton() {
  const items = useCartStore((state) => state.items);
  const total = useCartStore((state) => state.total());

  return (
    <button>
      Cart ({items.length}) - ${total.toFixed(2)}
    </button>
  );
}
```

### Zustand with Immer

```tsx
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface TodoStore {
  todos: Todo[];
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
}

export const useTodoStore = create<TodoStore>()(
  immer((set) => ({
    todos: [],

    addTodo: (text) =>
      set((state) => {
        state.todos.push({
          id: crypto.randomUUID(),
          text,
          completed: false,
        });
      }),

    toggleTodo: (id) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id);
        if (todo) {
          todo.completed = !todo.completed;
        }
      }),

    deleteTodo: (id) =>
      set((state) => {
        const index = state.todos.findIndex((t) => t.id === id);
        if (index !== -1) {
          state.todos.splice(index, 1);
        }
      }),
  }))
);
```

## Jotai

### Basic Jotai Atoms

```tsx
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';
import { atomWithStorage } from 'jotai/utils';

// Primitive atoms
const countAtom = atom(0);
const textAtom = atom('');

// Derived atom (computed value)
const doubleCountAtom = atom((get) => get(countAtom) * 2);

// Writable derived atom
const uppercaseTextAtom = atom(
  (get) => get(textAtom).toUpperCase(),
  (get, set, newValue: string) => set(textAtom, newValue.toLowerCase())
);

// Async atom
const userAtom = atom(async () => {
  const response = await fetch('/api/user');
  return response.json();
});

// Persisted atom
const themeAtom = atomWithStorage<'light' | 'dark'>('theme', 'light');

// Usage
function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const doubleCount = useAtomValue(doubleCountAtom);

  return (
    <div>
      <p>Count: {count}</p>
      <p>Double: {doubleCount}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}
```

### Jotai with Async Actions

```tsx
import { atom, useAtom } from 'jotai';
import { atomWithQuery, atomWithMutation } from 'jotai-tanstack-query';

// Query atom
const postsAtom = atomWithQuery(() => ({
  queryKey: ['posts'],
  queryFn: async () => {
    const res = await fetch('/api/posts');
    return res.json();
  },
}));

// Mutation atom
const createPostAtom = atomWithMutation(() => ({
  mutationFn: async (newPost: { title: string; content: string }) => {
    const res = await fetch('/api/posts', {
      method: 'POST',
      body: JSON.stringify(newPost),
    });
    return res.json();
  },
}));

function Posts() {
  const [{ data: posts, isLoading }] = useAtom(postsAtom);
  const [{ mutate: createPost, isPending }] = useAtom(createPostAtom);

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      {posts.map((post) => (
        <article key={post.id}>{post.title}</article>
      ))}
      <button onClick={() => createPost({ title: 'New', content: 'Content' })}>
        {isPending ? 'Creating...' : 'Add Post'}
      </button>
    </div>
  );
}
```

## TanStack Query (React Query)

### Basic Queries

```tsx
import { useQuery, useMutation, useQueryClient, QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Query client setup
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30, // 30 minutes
      retry: 3,
      refetchOnWindowFocus: true,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Posts />
    </QueryClientProvider>
  );
}

// Fetching data
function Posts() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const res = await fetch('/api/posts');
      if (!res.ok) throw new Error('Failed to fetch');
      return res.json();
    },
  });

  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div>
      {data.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
      <button onClick={() => refetch()}>Refresh</button>
    </div>
  );
}
```

### Mutations with Optimistic Updates

```tsx
function useCreatePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (newPost: CreatePostInput) => {
      const res = await fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPost),
      });
      if (!res.ok) throw new Error('Failed to create post');
      return res.json();
    },
    onMutate: async (newPost) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['posts'] });

      // Snapshot previous value
      const previousPosts = queryClient.getQueryData(['posts']);

      // Optimistically update
      queryClient.setQueryData(['posts'], (old: Post[]) => [
        { ...newPost, id: 'temp-id', createdAt: new Date() },
        ...old,
      ]);

      return { previousPosts };
    },
    onError: (err, newPost, context) => {
      // Rollback on error
      queryClient.setQueryData(['posts'], context?.previousPosts);
    },
    onSettled: () => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}

function CreatePostForm() {
  const createPost = useCreatePost();

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createPost.mutate({
      title: formData.get('title') as string,
      content: formData.get('content') as string,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit" disabled={createPost.isPending}>
        {createPost.isPending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
}
```

### Infinite Queries

```tsx
import { useInfiniteQuery } from '@tanstack/react-query';

function InfinitePosts() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
  } = useInfiniteQuery({
    queryKey: ['posts', 'infinite'],
    queryFn: async ({ pageParam = 0 }) => {
      const res = await fetch(`/api/posts?cursor=${pageParam}&limit=10`);
      return res.json();
    },
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    initialPageParam: 0,
  });

  if (isLoading) return <Spinner />;

  return (
    <div>
      {data?.pages.map((page, i) => (
        <Fragment key={i}>
          {page.posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </Fragment>
      ))}

      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage
          ? 'Loading more...'
          : hasNextPage
          ? 'Load More'
          : 'No more posts'}
      </button>
    </div>
  );
}
```

## SWR

### Basic SWR Usage

```tsx
import useSWR, { SWRConfig } from 'swr';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

function App() {
  return (
    <SWRConfig
      value={{
        fetcher,
        refreshInterval: 0,
        revalidateOnFocus: true,
        dedupingInterval: 2000,
      }}
    >
      <Dashboard />
    </SWRConfig>
  );
}

function Dashboard() {
  const { data, error, isLoading, mutate } = useSWR('/api/dashboard');

  if (error) return <div>Failed to load</div>;
  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Total Users: {data.totalUsers}</p>
      <button onClick={() => mutate()}>Refresh</button>
    </div>
  );
}
```

### SWR Mutation

```tsx
import useSWRMutation from 'swr/mutation';

async function createUser(url: string, { arg }: { arg: CreateUserInput }) {
  const res = await fetch(url, {
    method: 'POST',
    body: JSON.stringify(arg),
  });
  return res.json();
}

function CreateUserForm() {
  const { trigger, isMutating } = useSWRMutation('/api/users', createUser);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    await trigger({
      name: formData.get('name') as string,
      email: formData.get('email') as string,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button disabled={isMutating}>
        {isMutating ? 'Creating...' : 'Create'}
      </button>
    </form>
  );
}
```

## Best Practices

### 1. Choose the Right Tool

| Scenario | Recommended |
|----------|-------------|
| Simple local state | useState |
| Complex local state | useReducer |
| Shared state (small app) | Context + useReducer |
| Shared state (large app) | Zustand or Jotai |
| Server state | TanStack Query or SWR |

### 2. Avoid Prop Drilling

```tsx
// Instead of passing props through many levels
<Parent user={user}>
  <Child user={user}>
    <GrandChild user={user} />
  </Child>
</Parent>

// Use context or state management
<UserProvider>
  <Parent>
    <Child>
      <GrandChild /> {/* Access user via useUser() */}
    </Child>
  </Parent>
</UserProvider>
```

### 3. Normalize Complex State

```tsx
// Instead of nested objects
const badState = {
  posts: [
    { id: 1, title: 'Post 1', author: { id: 1, name: 'Alice' } },
    { id: 2, title: 'Post 2', author: { id: 1, name: 'Alice' } },
  ],
};

// Use normalized structure
const goodState = {
  posts: {
    byId: { 1: { id: 1, title: 'Post 1', authorId: 1 } },
    allIds: [1, 2],
  },
  authors: {
    byId: { 1: { id: 1, name: 'Alice' } },
    allIds: [1],
  },
};
```

## Additional References

For detailed patterns and advanced use cases, see:

- `references/zustand-patterns.md` - Advanced Zustand patterns including slices, middleware, and testing
