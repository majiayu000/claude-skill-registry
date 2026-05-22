---
name: swr
description: SWR data fetching - useSWR, mutations, revalidation, caching. Use when fetching API data, implementing real-time updates, or managing server state.
---

# SWR Data Fetching

## Basic Usage

```tsx
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

function Profile() {
  const { data, error, isLoading } = useSWR('/api/user', fetcher)

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  return <div>Hello, {data.name}</div>
}
```

## With TypeScript

```tsx
interface User {
  id: string
  name: string
  email: string
}

function Profile() {
  const { data, error, isLoading } = useSWR<User>('/api/user', fetcher)

  return <div>{data?.name}</div>
}
```

## Fetcher Options

```tsx
// Simple fetcher
const fetcher = (url: string) => fetch(url).then(r => r.json())

// With headers
const fetcher = (url: string) =>
  fetch(url, {
    headers: { Authorization: `Bearer ${token}` }
  }).then(r => r.json())

// With error handling
const fetcher = async (url: string) => {
  const res = await fetch(url)
  if (!res.ok) {
    const error = new Error('An error occurred')
    error.info = await res.json()
    error.status = res.status
    throw error
  }
  return res.json()
}
```

## SWR Options

```tsx
const { data, error, isLoading, isValidating, mutate } = useSWR('/api/data', fetcher, {
  revalidateOnFocus: true,       // Revalidate on window focus
  revalidateOnReconnect: true,   // Revalidate on network reconnect
  refreshInterval: 0,            // Polling interval (ms), 0 = disabled
  refreshWhenHidden: false,      // Refresh when tab hidden
  refreshWhenOffline: false,     // Refresh when offline
  shouldRetryOnError: true,      // Retry on error
  dedupingInterval: 2000,        // Dedupe requests within interval
  focusThrottleInterval: 5000,   // Throttle focus revalidation
  loadingTimeout: 3000,          // Loading timeout before onLoadingSlow
  errorRetryInterval: 5000,      // Error retry interval
  errorRetryCount: 3,            // Max retry count
  fallbackData: undefined,       // Initial data
  keepPreviousData: false,       // Keep previous data on key change
  suspense: false,               // Enable React Suspense
})
```

## Conditional Fetching

```tsx
// Only fetch when condition is met
const { data } = useSWR(shouldFetch ? '/api/data' : null, fetcher)

// Dependent fetching
const { data: user } = useSWR('/api/user', fetcher)
const { data: projects } = useSWR(
  user ? `/api/projects?userId=${user.id}` : null,
  fetcher
)
```

## Arguments

```tsx
// Multiple arguments
const { data } = useSWR(['/api/data', token], ([url, token]) =>
  fetchWithToken(url, token)
)

// Object key
const { data } = useSWR(
  { url: '/api/data', args: { page: 1, limit: 10 } },
  fetcher
)
```

## Mutation (Modify Data)

```tsx
import useSWR, { mutate } from 'swr'

function Profile() {
  const { data, mutate: boundMutate } = useSWR('/api/user', fetcher)

  const updateUser = async (newName: string) => {
    // Optimistic update
    boundMutate({ ...data, name: newName }, false)

    // Send request
    await fetch('/api/user', {
      method: 'PATCH',
      body: JSON.stringify({ name: newName })
    })

    // Revalidate
    boundMutate()
  }

  return <button onClick={() => updateUser('New Name')}>Update</button>
}

// Global mutate
mutate('/api/user')                    // Revalidate
mutate('/api/user', newData)           // Update and revalidate
mutate('/api/user', newData, false)    // Update without revalidation
mutate(key => key.startsWith('/api/')) // Mutate multiple keys
```

## useSWRMutation (for POST/PUT/DELETE)

```tsx
import useSWRMutation from 'swr/mutation'

async function sendRequest(url: string, { arg }: { arg: { name: string } }) {
  return fetch(url, {
    method: 'POST',
    body: JSON.stringify(arg)
  }).then(r => r.json())
}

function CreateUser() {
  const { trigger, isMutating, error } = useSWRMutation('/api/user', sendRequest)

  const handleCreate = async () => {
    try {
      const result = await trigger({ name: 'New User' })
      console.log('Created:', result)
    } catch (e) {
      console.error('Failed:', e)
    }
  }

  return (
    <button onClick={handleCreate} disabled={isMutating}>
      {isMutating ? 'Creating...' : 'Create User'}
    </button>
  )
}
```

## Pagination

```tsx
import useSWRInfinite from 'swr/infinite'

function PaginatedList() {
  const getKey = (pageIndex: number, previousPageData: any) => {
    if (previousPageData && !previousPageData.length) return null
    return `/api/items?page=${pageIndex}&limit=10`
  }

  const { data, size, setSize, isLoading, isValidating } = useSWRInfinite(getKey, fetcher)

  const items = data ? data.flat() : []
  const isLoadingMore = isLoading || (size > 0 && data && typeof data[size - 1] === 'undefined')
  const isEmpty = data?.[0]?.length === 0
  const isReachingEnd = isEmpty || (data && data[data.length - 1]?.length < 10)

  return (
    <div>
      {items.map((item) => <div key={item.id}>{item.name}</div>)}
      <button
        onClick={() => setSize(size + 1)}
        disabled={isLoadingMore || isReachingEnd}
      >
        {isLoadingMore ? 'Loading...' : isReachingEnd ? 'No more' : 'Load More'}
      </button>
    </div>
  )
}
```

## Global Configuration

```tsx
import { SWRConfig } from 'swr'

function App() {
  return (
    <SWRConfig
      value={{
        fetcher: (url) => fetch(url).then(r => r.json()),
        refreshInterval: 3000,
        revalidateOnFocus: false,
        onError: (error, key) => {
          console.error('SWR Error:', key, error)
        },
        onSuccess: (data, key) => {
          console.log('SWR Success:', key, data)
        },
      }}
    >
      <MyApp />
    </SWRConfig>
  )
}
```

## Preloading

```tsx
import { preload } from 'swr'

// Preload on hover
function Link({ href }) {
  return (
    <a
      href={href}
      onMouseEnter={() => preload('/api/data', fetcher)}
    >
      Hover to preload
    </a>
  )
}

// Preload on mount
useEffect(() => {
  preload('/api/data', fetcher)
}, [])
```

## Custom Hook Pattern

```tsx
function useSolarData(lat: number, lng: number) {
  const { data, error, isLoading, mutate } = useSWR(
    lat && lng ? `/api/solar/irradiance?lat=${lat}&lng=${lng}` : null,
    fetcher,
    {
      refreshInterval: 300000,  // 5 minutes
      revalidateOnFocus: false,
    }
  )

  return {
    solarData: data,
    isLoading,
    isError: error,
    refresh: mutate,
  }
}

// Usage
function Dashboard() {
  const { solarData, isLoading } = useSolarData(34.0522, -118.2437)

  if (isLoading) return <Skeleton />
  return <SolarMeter data={solarData} />
}
```

## Error Retry

```tsx
useSWR('/api/data', fetcher, {
  onErrorRetry: (error, key, config, revalidate, { retryCount }) => {
    // Never retry on 404
    if (error.status === 404) return

    // Only retry up to 3 times
    if (retryCount >= 3) return

    // Retry after 5 seconds
    setTimeout(() => revalidate({ retryCount }), 5000)
  }
})
```

## Suspense Mode

```tsx
import { Suspense } from 'react'

function Profile() {
  const { data } = useSWR('/api/user', fetcher, { suspense: true })
  return <div>{data.name}</div>
}

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Profile />
    </Suspense>
  )
}
```
