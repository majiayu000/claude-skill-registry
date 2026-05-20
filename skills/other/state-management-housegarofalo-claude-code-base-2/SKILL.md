---
name: state-management
description: Master React state management with Zustand, Redux Toolkit, Jotai, and React Query. Covers global state, server state, atomic state, and persistence patterns. Use for complex applications requiring scalable state architecture.
---

# State Management

Choose the right state management approach for your React application.

## Instructions

1. **Start simple** - Use useState/useReducer before reaching for libraries
2. **Separate concerns** - UI state vs server state vs global state
3. **Collocate state** - Keep state close to where it's used
4. **Use the right tool** - Different state types need different solutions
5. **Avoid over-engineering** - Not everything needs global state

## State Types

| Type | Examples | Solution |
|------|----------|----------|
| **Local UI** | Form inputs, toggles, modals | useState, useReducer |
| **Server** | API data, cached responses | React Query, SWR |
| **Global UI** | Theme, sidebar state, user preferences | Zustand, Jotai |
| **Complex Global** | Shopping cart, multi-step forms | Zustand, Redux Toolkit |

## Zustand (Recommended)

### Basic Store

```tsx
import { create } from 'zustand';

interface CounterStore {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

const useCounterStore = create<CounterStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));

// Usage
function Counter() {
  const { count, increment, decrement } = useCounterStore();
  return (
    <div>
      <span>{count}</span>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

### Async Actions

```tsx
interface UserStore {
  user: User | null;
  loading: boolean;
  error: string | null;
  fetchUser: (id: string) => Promise<void>;
  logout: () => void;
}

const useUserStore = create<UserStore>((set) => ({
  user: null,
  loading: false,
  error: null,

  fetchUser: async (id) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`/api/users/${id}`);
      const user = await response.json();
      set({ user, loading: false });
    } catch (error) {
      set({ error: 'Failed to fetch user', loading: false });
    }
  },

  logout: () => set({ user: null }),
}));
```

### Selectors for Performance

```tsx
// Only re-render when specific value changes
function UserName() {
  const name = useUserStore((state) => state.user?.name);
  return <span>{name}</span>;
}

// Multiple values with shallow compare
import { shallow } from 'zustand/shallow';

function UserInfo() {
  const { name, email } = useUserStore(
    (state) => ({ name: state.user?.name, email: state.user?.email }),
    shallow
  );
  return <div>{name} - {email}</div>;
}
```

### Persistence

```tsx
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useSettingsStore = create(
  persist<SettingsStore>(
    (set) => ({
      theme: 'light',
      language: 'en',
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'settings-storage',
      partialize: (state) => ({ theme: state.theme, language: state.language }),
    }
  )
);
```

### Slices Pattern

```tsx
// auth-slice.ts
export const createAuthSlice = (set) => ({
  user: null,
  isAuthenticated: false,
  login: (user) => set({ user, isAuthenticated: true }),
  logout: () => set({ user: null, isAuthenticated: false }),
});

// cart-slice.ts
export const createCartSlice = (set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({
    items: state.items.filter((i) => i.id !== id),
  })),
});

// store.ts
const useStore = create((...args) => ({
  ...createAuthSlice(...args),
  ...createCartSlice(...args),
}));
```

## React Query (Server State)

### Basic Query

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function UserProfile({ userId }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return <Profile user={user} />;
}
```

### Mutations with Optimistic Updates

```tsx
function TodoList() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: updateTodo,
    onMutate: async (newTodo) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      const previousTodos = queryClient.getQueryData(['todos']);

      queryClient.setQueryData(['todos'], (old) =>
        old.map((todo) => (todo.id === newTodo.id ? newTodo : todo))
      );

      return { previousTodos };
    },
    onError: (err, newTodo, context) => {
      queryClient.setQueryData(['todos'], context.previousTodos);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => mutation.mutate({ ...todo, completed: !todo.completed })}
          />
          {todo.title}
        </li>
      ))}
    </ul>
  );
}
```

### Infinite Queries

```tsx
function InfiniteList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['posts'],
    queryFn: ({ pageParam = 0 }) => fetchPosts(pageParam),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });

  return (
    <div>
      {data?.pages.map((page) =>
        page.posts.map((post) => <PostCard key={post.id} post={post} />)
      )}

      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? 'Loading...' : hasNextPage ? 'Load More' : 'No more posts'}
      </button>
    </div>
  );
}
```

## Jotai (Atomic State)

### Basic Atoms

```tsx
import { atom, useAtom } from 'jotai';

const countAtom = atom(0);
const doubleCountAtom = atom((get) => get(countAtom) * 2);

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const [doubleCount] = useAtom(doubleCountAtom);

  return (
    <div>
      <p>Count: {count}</p>
      <p>Double: {doubleCount}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}
```

### Async Atoms

```tsx
const userIdAtom = atom(1);
const userAtom = atom(async (get) => {
  const id = get(userIdAtom);
  const response = await fetch(`/api/users/${id}`);
  return response.json();
});

function User() {
  const [user] = useAtom(userAtom);
  return <div>{user.name}</div>;
}
```

## Redux Toolkit (Complex State)

### Store Setup

```tsx
import { configureStore, createSlice, PayloadAction } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1; },
    decrement: (state) => { state.value -= 1; },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
});

const store = configureStore({
  reducer: {
    counter: counterSlice.reducer,
  },
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export type RootState = ReturnType<typeof store.getState>;
```

### Async Thunks

```tsx
import { createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUser = createAsyncThunk(
  'users/fetchById',
  async (userId: string) => {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
  }
);

const usersSlice = createSlice({
  name: 'users',
  initialState: { user: null, loading: false, error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? 'Failed';
      });
  },
});
```

## Decision Guide

```
Need to manage state?
    |
    v
Is it server data (API responses)?
    Yes -> React Query or SWR
    |
    No
    |
    v
Is it used by only one component?
    Yes -> useState or useReducer
    |
    No
    |
    v
Is it used by a few nearby components?
    Yes -> Lift state up or Context
    |
    No
    |
    v
Is it complex with many actions?
    Yes -> Redux Toolkit
    |
    No -> Zustand or Jotai
```

## When to Use

- **useState**: Simple local state, form inputs
- **useReducer**: Complex local state with multiple sub-values
- **Context**: Theme, auth status (rarely changing data)
- **Zustand**: Global UI state, shopping carts, preferences
- **React Query**: All server/API data
- **Redux Toolkit**: Very complex state, time-travel debugging needs
- **Jotai**: Fine-grained reactivity, many independent atoms

## Notes

- Don't put everything in global state
- Server state and UI state are different concerns
- Zustand is simpler than Redux for most use cases
- React Query eliminates most "loading/error/data" boilerplate
- Test your state management logic separately from components
