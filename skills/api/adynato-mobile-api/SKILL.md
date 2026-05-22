---
name: adynato-mobile-api
description: API integration patterns for Adynato mobile apps. Covers data fetching with TanStack Query, authentication flows, offline support, error handling, and optimistic updates in React Native/Expo apps. Use when integrating APIs into mobile applications.
---

# Mobile API Skill

Use this skill when integrating APIs into Adynato mobile apps.

## Stack

- **Data Fetching**: TanStack Query (React Query)
- **HTTP Client**: Fetch API or Axios
- **Auth Storage**: expo-secure-store
- **Offline**: TanStack Query persistence

## Setup

### Query Client Configuration

```typescript
// lib/query-client.ts
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30,   // 30 minutes (formerly cacheTime)
      retry: 2,
      refetchOnWindowFocus: false, // Mobile doesn't have window focus
    },
    mutations: {
      retry: 1,
    },
  },
})
```

### Provider Setup

```tsx
// app/_layout.tsx
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from '@/lib/query-client'

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <Stack />
    </QueryClientProvider>
  )
}
```

## API Client

### Base Configuration

```typescript
// lib/api.ts
import * as SecureStore from 'expo-secure-store'

const API_URL = process.env.EXPO_PUBLIC_API_URL

interface RequestOptions extends RequestInit {
  requireAuth?: boolean
}

export async function api<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { requireAuth = true, ...fetchOptions } = options

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...fetchOptions.headers,
  }

  if (requireAuth) {
    const token = await SecureStore.getItemAsync('auth_token')
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new ApiError(response.status, error.error || 'Request failed')
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = 'ApiError'
  }
}
```

### API Functions

```typescript
// lib/api/users.ts
import { api } from '@/lib/api'

export interface User {
  id: string
  email: string
  name: string
}

export const usersApi = {
  getMe: () => api<{ data: User }>('/api/users/me'),

  getById: (id: string) => api<{ data: User }>(`/api/users/${id}`),

  update: (id: string, data: Partial<User>) =>
    api<{ data: User }>(`/api/users/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
}
```

## Query Hooks

### Basic Query

```typescript
// hooks/useUser.ts
import { useQuery } from '@tanstack/react-query'
import { usersApi } from '@/lib/api/users'

export function useUser(id: string) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => usersApi.getById(id),
    enabled: !!id,
  })
}
```

### Query with Transform

```typescript
export function useCurrentUser() {
  return useQuery({
    queryKey: ['users', 'me'],
    queryFn: usersApi.getMe,
    select: (response) => response.data, // Extract data from wrapper
  })
}
```

### Paginated Query

```typescript
import { useInfiniteQuery } from '@tanstack/react-query'

export function useUsersList() {
  return useInfiniteQuery({
    queryKey: ['users', 'list'],
    queryFn: ({ pageParam = 1 }) =>
      api(`/api/users?page=${pageParam}&limit=20`),
    getNextPageParam: (lastPage, pages) => {
      if (lastPage.data.length < 20) return undefined
      return pages.length + 1
    },
    initialPageParam: 1,
  })
}
```

## Mutations

### Basic Mutation

```typescript
// hooks/useUpdateProfile.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { usersApi } from '@/lib/api/users'

export function useUpdateProfile() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<User> }) =>
      usersApi.update(id, data),

    onSuccess: (response, { id }) => {
      // Update cache
      queryClient.setQueryData(['users', id], response)
      queryClient.invalidateQueries({ queryKey: ['users', 'me'] })
    },
  })
}
```

### Optimistic Update

```typescript
export function useToggleFavorite() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (itemId: string) => api(`/api/favorites/${itemId}`, {
      method: 'POST'
    }),

    onMutate: async (itemId) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['items', itemId] })

      // Snapshot previous value
      const previousItem = queryClient.getQueryData(['items', itemId])

      // Optimistically update
      queryClient.setQueryData(['items', itemId], (old: any) => ({
        ...old,
        isFavorite: !old.isFavorite,
      }))

      return { previousItem }
    },

    onError: (err, itemId, context) => {
      // Rollback on error
      queryClient.setQueryData(['items', itemId], context?.previousItem)
    },

    onSettled: (data, error, itemId) => {
      // Refetch to ensure sync
      queryClient.invalidateQueries({ queryKey: ['items', itemId] })
    },
  })
}
```

## Authentication Flow

### Login

```typescript
// hooks/useAuth.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import * as SecureStore from 'expo-secure-store'
import { router } from 'expo-router'
import { api } from '@/lib/api'

interface LoginInput {
  email: string
  password: string
}

export function useLogin() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (input: LoginInput) =>
      api<{ token: string; user: User }>('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify(input),
        requireAuth: false,
      }),

    onSuccess: async (response) => {
      await SecureStore.setItemAsync('auth_token', response.token)
      queryClient.setQueryData(['users', 'me'], { data: response.user })
      router.replace('/(tabs)')
    },
  })
}

export function useLogout() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async () => {
      await SecureStore.deleteItemAsync('auth_token')
    },

    onSuccess: () => {
      queryClient.clear()
      router.replace('/(auth)/login')
    },
  })
}
```

### Auth State Check

```typescript
// hooks/useAuthState.ts
import { useQuery } from '@tanstack/react-query'
import * as SecureStore from 'expo-secure-store'

export function useAuthState() {
  return useQuery({
    queryKey: ['auth', 'state'],
    queryFn: async () => {
      const token = await SecureStore.getItemAsync('auth_token')
      return { isAuthenticated: !!token }
    },
    staleTime: Infinity,
  })
}
```

## Error Handling

### Global Error Handler

```typescript
// In query client setup
const queryClient = new QueryClient({
  defaultOptions: {
    mutations: {
      onError: (error) => {
        if (error instanceof ApiError) {
          if (error.status === 401) {
            // Handle unauthorized - redirect to login
            SecureStore.deleteItemAsync('auth_token')
            router.replace('/(auth)/login')
            return
          }
        }
        // Show toast or alert
        Alert.alert('Error', error.message)
      },
    },
  },
})
```

### Per-Query Error Handling

```tsx
function ProfileScreen() {
  const { data, error, isLoading, refetch } = useCurrentUser()

  if (isLoading) return <LoadingSpinner />

  if (error) {
    return (
      <ErrorView
        message={error.message}
        onRetry={refetch}
      />
    )
  }

  return <ProfileContent user={data} />
}
```

## Offline Support

### Query Persistence

```typescript
// lib/query-client.ts
import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister'
import AsyncStorage from '@react-native-async-storage/async-storage'
import { persistQueryClient } from '@tanstack/react-query-persist-client'

const asyncStoragePersister = createAsyncStoragePersister({
  storage: AsyncStorage,
})

persistQueryClient({
  queryClient,
  persister: asyncStoragePersister,
})
```

### Network Status

```typescript
// hooks/useNetworkStatus.ts
import { useEffect, useState } from 'react'
import NetInfo from '@react-native-community/netinfo'
import { onlineManager } from '@tanstack/react-query'

export function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(true)

  useEffect(() => {
    return NetInfo.addEventListener((state) => {
      const online = !!state.isConnected
      setIsOnline(online)
      onlineManager.setOnline(online)
    })
  }, [])

  return isOnline
}
```

## Usage in Components

```tsx
// screens/ProfileScreen.tsx
import { useCurrentUser, useUpdateProfile } from '@/hooks/useUser'

export function ProfileScreen() {
  const { data: user, isLoading } = useCurrentUser()
  const updateProfile = useUpdateProfile()

  const handleSave = (formData: Partial<User>) => {
    updateProfile.mutate(
      { id: user.id, data: formData },
      {
        onSuccess: () => {
          Alert.alert('Success', 'Profile updated!')
        },
      }
    )
  }

  if (isLoading) return <LoadingSpinner />

  return (
    <ProfileForm
      user={user}
      onSave={handleSave}
      isSaving={updateProfile.isPending}
    />
  )
}
```

## Checklist

Before shipping:

- [ ] Auth token stored in SecureStore (not AsyncStorage)
- [ ] 401 responses trigger logout/re-auth
- [ ] Loading states shown during fetches
- [ ] Error states with retry options
- [ ] Optimistic updates where appropriate
- [ ] Offline support if required
- [ ] Request timeouts configured
- [ ] No sensitive data logged
