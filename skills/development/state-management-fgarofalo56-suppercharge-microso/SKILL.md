---
name: state-management
description: Master React state management with Zustand, Redux Toolkit, Jotai, and React Query. Covers global state, server state, atomic state, and persistence patterns. Use for complex applications requiring scalable state architecture.
---

# State Management

Comprehensive state management patterns for React applications.

## State Types Overview

| Type             | Library                 | When to Use                 |
| ---------------- | ----------------------- | --------------------------- |
| **Server State** | React Query, SWR        | API data, caching, sync     |
| **Global State** | Zustand, Redux Toolkit  | App-wide UI state           |
| **Atomic State** | Jotai, Recoil           | Fine-grained reactivity     |
| **Form State**   | React Hook Form, Formik | Complex forms               |
| **URL State**    | nuqs, next-query-params | Search, filters, pagination |

## Zustand (Recommended for Most Cases)

### Basic Store

```tsx
// stores/useUserStore.ts
import { create } from "zustand";

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserState {
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User) => void;
  logout: () => void;
  updateProfile: (updates: Partial<User>) => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  isAuthenticated: false,

  login: (user) => set({ user, isAuthenticated: true }),

  logout: () => set({ user: null, isAuthenticated: false }),

  updateProfile: (updates) =>
    set((state) => ({
      user: state.user ? { ...state.user, ...updates } : null,
    })),
}));
```

### Using the Store

```tsx
// components/UserProfile.tsx
import { useUserStore } from "@/stores/useUserStore";

export function UserProfile() {
  // Subscribe to specific parts of state
  const user = useUserStore((state) => state.user);
  const logout = useUserStore((state) => state.logout);

  if (!user) return null;

  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

// Only re-renders when isAuthenticated changes
function AuthStatus() {
  const isAuthenticated = useUserStore((state) => state.isAuthenticated);
  return <span>{isAuthenticated ? "Logged in" : "Guest"}</span>;
}
```

### Zustand with Middleware

```tsx
// stores/useAppStore.ts
import { create } from "zustand";
import { devtools, persist, subscribeWithSelector } from "zustand/middleware";
import { immer } from "zustand/middleware/immer";

interface AppState {
  theme: "light" | "dark";
  sidebarOpen: boolean;
  notifications: Notification[];
  setTheme: (theme: "light" | "dark") => void;
  toggleSidebar: () => void;
  addNotification: (notification: Notification) => void;
  removeNotification: (id: string) => void;
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      subscribeWithSelector(
        immer((set) => ({
          theme: "light",
          sidebarOpen: true,
          notifications: [],

          setTheme: (theme) =>
            set((state) => {
              state.theme = theme;
            }),

          toggleSidebar: () =>
            set((state) => {
              state.sidebarOpen = !state.sidebarOpen;
            }),

          addNotification: (notification) =>
            set((state) => {
              state.notifications.push(notification);
            }),

          removeNotification: (id) =>
            set((state) => {
              state.notifications = state.notifications.filter(
                (n) => n.id !== id,
              );
            }),
        })),
      ),
      {
        name: "app-storage",
        partialize: (state) => ({ theme: state.theme }),
      },
    ),
    { name: "AppStore" },
  ),
);

// Subscribe to changes outside React
useAppStore.subscribe(
  (state) => state.theme,
  (theme) => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  },
);
```

### Zustand Slices Pattern

```tsx
// stores/slices/userSlice.ts
import { StateCreator } from "zustand";

export interface UserSlice {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

export const createUserSlice: StateCreator<
  UserSlice & CartSlice,
  [],
  [],
  UserSlice
> = (set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
});

// stores/slices/cartSlice.ts
export interface CartSlice {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  clearCart: () => void;
}

export const createCartSlice: StateCreator<
  UserSlice & CartSlice,
  [],
  [],
  CartSlice
> = (set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) =>
    set((state) => ({ items: state.items.filter((i) => i.id !== id) })),
  clearCart: () => set({ items: [] }),
});

// stores/useStore.ts
import { create } from "zustand";
import { createUserSlice, UserSlice } from "./slices/userSlice";
import { createCartSlice, CartSlice } from "./slices/cartSlice";

export const useStore = create<UserSlice & CartSlice>()((...a) => ({
  ...createUserSlice(...a),
  ...createCartSlice(...a),
}));
```

## Redux Toolkit

### Store Setup

```tsx
// store/store.ts
import { configureStore } from "@reduxjs/toolkit";
import { TypedUseSelectorHook, useDispatch, useSelector } from "react-redux";
import userReducer from "./slices/userSlice";
import cartReducer from "./slices/cartSlice";
import { api } from "./api";

export const store = configureStore({
  reducer: {
    user: userReducer,
    cart: cartReducer,
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Typed hooks
export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

### Slice with Async Thunks

```tsx
// store/slices/userSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";

interface UserState {
  user: User | null;
  status: "idle" | "loading" | "succeeded" | "failed";
  error: string | null;
}

const initialState: UserState = {
  user: null,
  status: "idle",
  error: null,
};

export const fetchUser = createAsyncThunk(
  "user/fetchUser",
  async (userId: string, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw new Error("User not found");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : "Failed");
    }
  },
);

export const updateUser = createAsyncThunk(
  "user/updateUser",
  async (updates: Partial<User>, { getState, rejectWithValue }) => {
    const state = getState() as { user: UserState };
    if (!state.user.user) {
      return rejectWithValue("No user logged in");
    }

    const response = await fetch(`/api/users/${state.user.user.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updates),
    });

    return await response.json();
  },
);

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.status = "idle";
      state.error = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.user = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload as string;
      })
      .addCase(updateUser.fulfilled, (state, action) => {
        state.user = action.payload;
      });
  },
});

export const { logout, clearError } = userSlice.actions;
export default userSlice.reducer;
```

### RTK Query

```tsx
// store/api.ts
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

interface User {
  id: string;
  name: string;
  email: string;
}

export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  tagTypes: ["User", "Post"],
  endpoints: (builder) => ({
    // Queries
    getUsers: builder.query<User[], void>({
      query: () => "users",
      providesTags: ["User"],
    }),

    getUser: builder.query<User, string>({
      query: (id) => `users/${id}`,
      providesTags: (result, error, id) => [{ type: "User", id }],
    }),

    // Mutations
    createUser: builder.mutation<User, Partial<User>>({
      query: (body) => ({
        url: "users",
        method: "POST",
        body,
      }),
      invalidatesTags: ["User"],
    }),

    updateUser: builder.mutation<User, { id: string; updates: Partial<User> }>({
      query: ({ id, updates }) => ({
        url: `users/${id}`,
        method: "PATCH",
        body: updates,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "User", id }],
    }),

    deleteUser: builder.mutation<void, string>({
      query: (id) => ({
        url: `users/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: ["User"],
    }),
  }),
});

export const {
  useGetUsersQuery,
  useGetUserQuery,
  useCreateUserMutation,
  useUpdateUserMutation,
  useDeleteUserMutation,
} = api;
```

## React Query (TanStack Query)

### Setup

```tsx
// providers/QueryProvider.tsx
"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { useState } from "react";

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            gcTime: 5 * 60 * 1000, // 5 minutes
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      }),
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### Query Hooks

```tsx
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

const userKeys = {
  all: ["users"] as const,
  lists: () => [...userKeys.all, "list"] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, "detail"] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};

async function fetchUsers(filters?: UserFilters): Promise<User[]> {
  const params = new URLSearchParams(filters as Record<string, string>);
  const res = await fetch(`/api/users?${params}`);
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
}

async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error("User not found");
  return res.json();
}

export function useUsers(filters?: UserFilters) {
  return useQuery({
    queryKey: userKeys.list(filters ?? {}),
    queryFn: () => fetchUsers(filters),
  });
}

export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => fetchUser(id),
    enabled: !!id,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateUserData) => {
      const res = await fetch("/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error("Failed to create user");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<User> }) => {
      const res = await fetch(`/api/users/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error("Failed to update user");
      return res.json();
    },
    onSuccess: (data, { id }) => {
      // Update cache directly
      queryClient.setQueryData(userKeys.detail(id), data);
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}

export function useDeleteUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      const res = await fetch(`/api/users/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete user");
    },
    onSuccess: (_, id) => {
      queryClient.removeQueries({ queryKey: userKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}
```

### Optimistic Updates

```tsx
export function useToggleFavorite() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (postId: string) => {
      const res = await fetch(`/api/posts/${postId}/favorite`, {
        method: "POST",
      });
      return res.json();
    },
    onMutate: async (postId) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ["posts", postId] });

      // Snapshot previous value
      const previousPost = queryClient.getQueryData<Post>(["posts", postId]);

      // Optimistically update
      queryClient.setQueryData(["posts", postId], (old: Post | undefined) => {
        if (!old) return old;
        return { ...old, isFavorite: !old.isFavorite };
      });

      // Return context for rollback
      return { previousPost };
    },
    onError: (err, postId, context) => {
      // Rollback on error
      queryClient.setQueryData(["posts", postId], context?.previousPost);
    },
    onSettled: (_, __, postId) => {
      // Refetch to ensure sync
      queryClient.invalidateQueries({ queryKey: ["posts", postId] });
    },
  });
}
```

## Jotai (Atomic State)

### Basic Atoms

```tsx
// atoms/userAtoms.ts
import { atom } from "jotai";
import { atomWithStorage } from "jotai/utils";

// Primitive atom
export const userAtom = atom<User | null>(null);

// Derived atom (read-only)
export const isAuthenticatedAtom = atom((get) => get(userAtom) !== null);

// Derived atom (read-write)
export const userNameAtom = atom(
  (get) => get(userAtom)?.name ?? "Guest",
  (get, set, newName: string) => {
    const user = get(userAtom);
    if (user) {
      set(userAtom, { ...user, name: newName });
    }
  },
);

// Async atom
export const userProfileAtom = atom(async (get) => {
  const user = get(userAtom);
  if (!user) return null;

  const res = await fetch(`/api/users/${user.id}/profile`);
  return res.json();
});

// Persisted atom
export const themeAtom = atomWithStorage<"light" | "dark">("theme", "light");
```

### Using Atoms

```tsx
// components/UserName.tsx
import { useAtom, useAtomValue, useSetAtom } from "jotai";
import { userAtom, isAuthenticatedAtom, userNameAtom } from "@/atoms/userAtoms";

// Read-only
function AuthStatus() {
  const isAuthenticated = useAtomValue(isAuthenticatedAtom);
  return <span>{isAuthenticated ? "Logged in" : "Guest"}</span>;
}

// Write-only
function LogoutButton() {
  const setUser = useSetAtom(userAtom);
  return <button onClick={() => setUser(null)}>Logout</button>;
}

// Read and write
function UserNameEditor() {
  const [name, setName] = useAtom(userNameAtom);
  return <input value={name} onChange={(e) => setName(e.target.value)} />;
}
```

### Atom Families

```tsx
// atoms/todoAtoms.ts
import { atom } from "jotai";
import { atomFamily } from "jotai/utils";

interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

// Atom for todo IDs
export const todoIdsAtom = atom<string[]>([]);

// Atom family for individual todos
export const todoAtomFamily = atomFamily((id: string) =>
  atom<Todo>({
    id,
    text: "",
    completed: false,
  }),
);

// Derived: all todos
export const todosAtom = atom((get) =>
  get(todoIdsAtom).map((id) => get(todoAtomFamily(id))),
);

// Derived: completed count
export const completedCountAtom = atom(
  (get) => get(todosAtom).filter((t) => t.completed).length,
);

// Action: toggle todo
export const toggleTodoAtom = atom(null, (get, set, id: string) => {
  const todoAtom = todoAtomFamily(id);
  const todo = get(todoAtom);
  set(todoAtom, { ...todo, completed: !todo.completed });
});
```

## State Selection Patterns

### Zustand Selectors

```tsx
// Avoid: re-renders on any state change
const { user, theme, notifications } = useAppStore();

// Better: subscribe to specific values
const user = useAppStore((state) => state.user);
const theme = useAppStore((state) => state.theme);

// Best: shallow comparison for objects
import { shallow } from "zustand/shallow";

const { user, theme } = useAppStore(
  (state) => ({ user: state.user, theme: state.theme }),
  shallow,
);

// Custom equality
const notifications = useAppStore(
  (state) => state.notifications,
  (a, b) => a.length === b.length,
);
```

### Redux Selectors with Reselect

```tsx
// store/selectors.ts
import { createSelector } from "@reduxjs/toolkit";
import type { RootState } from "./store";

const selectCart = (state: RootState) => state.cart;
const selectItems = (state: RootState) => state.cart.items;

// Memoized selector
export const selectCartTotal = createSelector([selectItems], (items) =>
  items.reduce((total, item) => total + item.price * item.quantity, 0),
);

// Parameterized selector
export const selectItemById = createSelector(
  [selectItems, (_, id: string) => id],
  (items, id) => items.find((item) => item.id === id),
);

// Usage
function CartTotal() {
  const total = useAppSelector(selectCartTotal);
  return <span>${total.toFixed(2)}</span>;
}
```

## Combining State Solutions

### Zustand + React Query

```tsx
// Zustand for UI state
const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  selectedUserId: null,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  selectUser: (id) => set({ selectedUserId: id }),
}));

// React Query for server state
function UserList() {
  const { data: users, isLoading } = useUsers();
  const selectedUserId = useUIStore((s) => s.selectedUserId);
  const selectUser = useUIStore((s) => s.selectUser);

  if (isLoading) return <Loading />;

  return (
    <ul>
      {users?.map((user) => (
        <li
          key={user.id}
          onClick={() => selectUser(user.id)}
          className={user.id === selectedUserId ? "selected" : ""}
        >
          {user.name}
        </li>
      ))}
    </ul>
  );
}
```

## Best Practices

1. **Separate Server vs Client State** - Use React Query for API data
2. **Colocate State** - Keep state as close to usage as possible
3. **Minimize Global State** - Only globalize what's truly shared
4. **Use Selectors** - Prevent unnecessary re-renders
5. **Normalize Data** - Avoid deeply nested state
6. **Persist Strategically** - Only persist what's needed
7. **Type Everything** - Full TypeScript coverage
8. **Use DevTools** - Debug with Redux/Zustand/React Query devtools

## When to Use

| Scenario                   | Recommended               |
| -------------------------- | ------------------------- |
| Simple app, few components | React useState/useContext |
| Complex UI state           | Zustand                   |
| Large enterprise app       | Redux Toolkit             |
| Server data caching        | React Query               |
| Fine-grained reactivity    | Jotai                     |
| Complex forms              | React Hook Form           |
| URL-synced state           | nuqs                      |
