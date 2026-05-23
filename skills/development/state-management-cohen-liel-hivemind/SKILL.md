---
name: state-management
description: Frontend state management patterns for React apps. Use when implementing Redux Toolkit, Zustand, Jotai, React Query, or any global state management solution.
---

# State Management Patterns

## Zustand (Recommended — simple & powerful)
```typescript
// store/useAuthStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  name: string
}

interface AuthStore {
  user: User | null
  token: string | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isLoading: false,

      login: async (email, password) => {
        set({ isLoading: true })
        try {
          const { user, token } = await api.login(email, password)
          set({ user, token, isLoading: false })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: () => set({ user: null, token: null }),
      setUser: (user) => set({ user }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ token: state.token }), // Only persist token
    }
  )
)

// Usage
const { user, login, logout } = useAuthStore()
const isLoggedIn = useAuthStore((state) => state.user !== null)
```

## React Query / TanStack Query (Server state)
```typescript
// lib/queryClient.ts
import { QueryClient } from '@tanstack/react-query'
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,  // 5 min
      retry: 1,
    },
  },
})

// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

export function useUsers(filters?: UserFilters) {
  return useQuery({
    queryKey: ['users', filters],
    queryFn: () => api.getUsers(filters),
    staleTime: 30_000,
  })
}

export function useUser(id: string) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => api.getUser(id),
    enabled: !!id,  // Don't run if no ID
  })
}

export function useUpdateUser() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: UpdateUserInput) => api.updateUser(data),
    onSuccess: (updatedUser) => {
      // Optimistic update
      qc.setQueryData(['users', updatedUser.id], updatedUser)
      // Invalidate list
      qc.invalidateQueries({ queryKey: ['users'] })
    },
  })
}

// Infinite scroll
export function useInfiniteUsers() {
  return useInfiniteQuery({
    queryKey: ['users', 'infinite'],
    queryFn: ({ pageParam = 1 }) => api.getUsers({ page: pageParam }),
    getNextPageParam: (lastPage) => lastPage.nextPage ?? undefined,
    initialPageParam: 1,
  })
}

// Component usage
function UserList() {
  const { data, isLoading, error } = useUsers()
  const { mutate: updateUser, isPending } = useUpdateUser()

  if (isLoading) return <Skeleton />
  if (error) return <ErrorMessage error={error} />

  return data?.map(user => (
    <UserCard
      key={user.id}
      user={user}
      onUpdate={(data) => updateUser({ id: user.id, ...data })}
    />
  ))
}
```

## Redux Toolkit (Complex state)
```typescript
// store/postsSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'

interface Post { id: string; title: string; body: string }
interface PostsState {
  items: Post[]
  status: 'idle' | 'loading' | 'succeeded' | 'failed'
  error: string | null
}

// Async thunk
export const fetchPosts = createAsyncThunk('posts/fetchAll', async () => {
  return await api.getPosts()
})

export const postsSlice = createSlice({
  name: 'posts',
  initialState: { items: [], status: 'idle', error: null } as PostsState,
  reducers: {
    addPost: (state, action: PayloadAction<Post>) => {
      state.items.push(action.payload)
    },
    removePost: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(p => p.id !== action.payload)
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchPosts.pending, (state) => { state.status = 'loading' })
      .addCase(fetchPosts.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.items = action.payload
      })
      .addCase(fetchPosts.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message ?? null
      })
  },
})

// store/index.ts
import { configureStore } from '@reduxjs/toolkit'
import { useSelector, useDispatch } from 'react-redux'

export const store = configureStore({
  reducer: { posts: postsSlice.reducer },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

// Typed hooks
export const useAppSelector = useSelector.withTypes<RootState>()
export const useAppDispatch = useDispatch.withTypes<AppDispatch>()
```

## Jotai (Atomic state)
```typescript
// atoms/userAtom.ts
import { atom, useAtom, useAtomValue } from 'jotai'
import { atomWithStorage } from 'jotai/utils'

export const userAtom = atomWithStorage<User | null>('user', null)
export const themeAtom = atomWithStorage<'light' | 'dark'>('theme', 'light')

// Derived atom
export const isAdminAtom = atom((get) => get(userAtom)?.role === 'ADMIN')

// Write-only atom (action)
export const logoutAtom = atom(null, (get, set) => {
  set(userAtom, null)
  set(themeAtom, 'light')
})

// Component
function Header() {
  const user = useAtomValue(userAtom)
  const isAdmin = useAtomValue(isAdminAtom)
  const [, logout] = useAtom(logoutAtom)

  return <nav>{user ? <button onClick={logout}>Logout</button> : null}</nav>
}
```

## Context + useReducer (Built-in, no deps)
```typescript
// context/CartContext.tsx
type CartAction =
  | { type: 'ADD_ITEM'; item: CartItem }
  | { type: 'REMOVE_ITEM'; id: string }
  | { type: 'CLEAR_CART' }

function cartReducer(state: CartItem[], action: CartAction): CartItem[] {
  switch (action.type) {
    case 'ADD_ITEM':
      const existing = state.find(i => i.id === action.item.id)
      if (existing) return state.map(i => i.id === action.item.id
        ? { ...i, quantity: i.quantity + 1 } : i)
      return [...state, { ...action.item, quantity: 1 }]
    case 'REMOVE_ITEM': return state.filter(i => i.id !== action.id)
    case 'CLEAR_CART': return []
    default: return state
  }
}

const CartContext = createContext<{ cart: CartItem[]; dispatch: Dispatch<CartAction> } | null>(null)

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, dispatch] = useReducer(cartReducer, [])
  return <CartContext value={{ cart, dispatch }}>{children}</CartContext>
}

export const useCart = () => {
  const ctx = use(CartContext)
  if (!ctx) throw new Error('useCart must be used within CartProvider')
  return ctx
}
```

## Rules
- **Server state** (API data): React Query / TanStack Query
- **Global client state** (auth, settings): Zustand or Jotai
- **Complex local state** (shopping cart, multi-step form): useReducer + Context
- **Redux only** for very large apps with complex cross-slice interactions
- Never store server data in Redux/Zustand — that's React Query's job
- Zustand: use selectors (`useStore(state => state.user)`) not full store (prevents re-renders)
- React Query: set `staleTime` appropriately — default is 0 (always refetch on mount)
- Always invalidate queries after mutations — never manually merge response into cache
