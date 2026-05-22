---
skill_id: frontend-patterns
name: React + Vite + Shopify Polaris Web Components Frontend Patterns
description: Frontend development patterns for React with Vite and Shopify Polaris Web Components - Form handling with React Hook Form + Zod, data fetching with TanStack Query, and App Bridge integration
category: frontend
tags: [react, vite, shopify-polaris, polaris-web-components, app-bridge, tanstack-query, react-hook-form, zod, typescript]
applies_to: [typescript, javascript]
auto_trigger: ["react", "vite", "polaris", "s-page", "s-button", "app-bridge", "shopify", "react-hook-form", "zod"]
---

# React + Vite + Shopify Polaris Web Components Frontend Patterns

Modern frontend patterns for building Shopify embedded apps with React 19, Vite 7, TypeScript, and Shopify Polaris Web Components.

## Core Stack

```
React 19 + TypeScript
     |
     +-> Vite 7 (Build Tool)
     |     +-> Fast HMR
     |     +-> ESM imports
     |     +-> Optimized builds
     |
     +-> Shopify Polaris Web Components (UI)
     |     +-> CDN script loading
     |     +-> s-* prefixed components
     |     +-> Standard DOM events
     |     +-> No AppProvider needed
     |
     +-> App Bridge (Shopify Integration)
     |     +-> Session tokens
     |     +-> Navigation
     |     +-> Direct initialization (no React Provider)
     |
     +-> React Hook Form + Zod (Forms)
     |     +-> Schema-based validation
     |     +-> Type inference from schemas
     |     +-> Controller pattern for Web Components
     |
     +-> TanStack Query (Data Fetching)
           +-> Query key factories
           +-> Prefetching
           +-> Parallel & dependent queries
           +-> Optimistic updates
```

---

## 1. Vite Setup & Configuration

### 1.1 Vite Config

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'forms': ['react-hook-form', '@hookform/resolvers', 'zod'],
          'app-bridge': ['@shopify/app-bridge'],
          'tanstack': ['@tanstack/react-query'],
        },
      },
    },
  },
})
```

### 1.2 HTML Entry Point with Polaris CDN

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="shopify-api-key" content="%VITE_SHOPIFY_API_KEY%" />

    <!-- Shopify App Bridge -->
    <script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>

    <!-- Shopify Polaris Web Components -->
    <script src="https://cdn.shopify.com/shopifycloud/polaris.js" type="module"></script>

    <title>My Shopify App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### 1.3 Environment Variables with Zod Validation

```typescript
// src/env.ts
import { z } from 'zod'

const envSchema = z.object({
  VITE_SHOPIFY_API_KEY: z.string().min(1, 'API key required'),
  VITE_API_URL: z.string().url('Invalid API URL'),
  VITE_APP_URL: z.string().url('Invalid App URL'),
})

// Validate at startup - will throw if invalid
export const env = envSchema.parse({
  VITE_SHOPIFY_API_KEY: import.meta.env.VITE_SHOPIFY_API_KEY,
  VITE_API_URL: import.meta.env.VITE_API_URL,
  VITE_APP_URL: import.meta.env.VITE_APP_URL,
})

// src/env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_SHOPIFY_API_KEY: string
  readonly VITE_API_URL: string
  readonly VITE_APP_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

### 1.4 Lazy Loading & Code Splitting

```typescript
import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))
const Products = lazy(() => import('./pages/Products'))

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<s-spinner size="large" />}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/products" element={<Products />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}
```

---

## 2. Shopify Polaris Web Components

### 2.1 TypeScript Declarations

Shopify provides official TypeScript type packages for both App Bridge and Polaris Web Components. Use these packages instead of manual type declarations.

#### App Bridge Types

The `@shopify/app-bridge-types` package provides TypeScript types for the global `shopify` object and all App Bridge APIs.

**Installation:**

```bash
# npm
npm install --save-dev @shopify/app-bridge-types

# yarn
yarn add --dev @shopify/app-bridge-types
```

**Configuration (tsconfig.json):**

```json
{
  "compilerOptions": {
    "types": ["@shopify/app-bridge-types"]
  }
}
```

> **Note:** If you're using the `@shopify/app-bridge-react` library, the types package is already included.

#### Polaris Web Components Types

The `@shopify/polaris-types` package provides TypeScript types for all Polaris web components (`s-page`, `s-button`, `s-text-field`, etc.).

**Installation:**

```bash
# npm
npm install --save-dev @shopify/polaris-types

# yarn
yarn add --dev @shopify/polaris-types
```

**For CDN usage** (https://cdn.shopify.com/shopifycloud/polaris.js), specify `latest` in package.json:

```json
{
  "devDependencies": {
    "@shopify/polaris-types": "latest"
  }
}
```

**Configuration (tsconfig.json):**

```json
{
  "compilerOptions": {
    "types": ["@shopify/polaris-types"]
  }
}
```

#### Combined Configuration

If using both App Bridge and Polaris Web Components:

```json
{
  "compilerOptions": {
    "types": ["@shopify/app-bridge-types", "@shopify/polaris-types"]
  }
}
```

#### Optional ESLint Configuration

If your app uses ESLint, add the global `shopify` object to your configuration:

```javascript
// .eslintrc.cjs
module.exports = {
  globals: {
    shopify: 'readonly',
  },
};
```

### 2.2 Component Reference

| Category | Web Component | Description |
|----------|---------------|-------------|
| **Layout** | `s-page`, `s-section`, `s-stack`, `s-grid`, `s-box` | Page structure and spacing |
| **Forms** | `s-text-field`, `s-select`, `s-checkbox`, `s-choice-list`, `s-switch`, `s-drop-zone` | Form inputs |
| **Actions** | `s-button`, `s-button-group`, `s-link`, `s-menu` | Interactive elements |
| **Feedback** | `s-badge`, `s-banner`, `s-spinner` | Status indicators |
| **Overlays** | `s-modal`, `s-popover` | Dialogs and popovers |
| **Typography** | `s-heading`, `s-text`, `s-paragraph` | Text elements |
| **Media** | `s-thumbnail`, `s-avatar`, `s-icon` | Visual elements |

### 2.3 Page Layout

```typescript
// src/pages/Dashboard.tsx
export default function Dashboard() {
  const handleCreateOrder = () => {
    // Handle create order
  }

  return (
    <s-page title="Dashboard">
      <s-section heading="Overview">
        <s-stack gap="base">
          <s-grid gridTemplateColumns="1fr 1fr 1fr" gap="base">
            <s-box padding="base" background="subdued" borderRadius="base">
              <s-stack gap="small-100">
                <s-text color="subdued">Total Revenue</s-text>
                <s-heading>$12,345</s-heading>
              </s-stack>
            </s-box>

            <s-box padding="base" background="subdued" borderRadius="base">
              <s-stack gap="small-100">
                <s-text color="subdued">Orders</s-text>
                <s-heading>123</s-heading>
              </s-stack>
            </s-box>

            <s-box padding="base" background="subdued" borderRadius="base">
              <s-stack gap="small-100">
                <s-text color="subdued">Customers</s-text>
                <s-heading>456</s-heading>
              </s-stack>
            </s-box>
          </s-grid>

          <s-button variant="primary" onClick={handleCreateOrder}>
            Create Order
          </s-button>
        </s-stack>
      </s-section>
    </s-page>
  )
}
```

### 2.4 Common Components

```typescript
// Buttons - use variant for visual style, tone for semantic meaning
<s-button variant="primary" onClick={handleSave}>Save</s-button>
<s-button variant="secondary" onClick={handleCancel}>Cancel</s-button>
<s-button tone="critical" onClick={handleDelete}>Delete</s-button>

<s-button-group>
  <s-button slot="secondary-actions">Cancel</s-button>
  <s-button slot="primary-action" variant="primary">Save</s-button>
</s-button-group>

// Banners - use tone (not status)
<s-banner tone="success" heading="Order created">
  Your order has been created successfully.
</s-banner>

<s-banner tone="critical" heading="Error">
  Something went wrong. Please try again.
</s-banner>

// Badges - use tone (not status)
<s-badge tone="success">Active</s-badge>
<s-badge tone="warning">Pending</s-badge>
<s-badge tone="critical">Failed</s-badge>

// Modal
const [modalOpen, setModalOpen] = useState(false)

<s-button onClick={() => setModalOpen(true)}>Open Modal</s-button>

{modalOpen && (
  <s-modal open title="Confirm Delete" onClose={() => setModalOpen(false)}>
    <s-section>
      <s-text>Are you sure you want to delete this item?</s-text>
    </s-section>
    <div slot="footer">
      <s-button-group>
        <s-button onClick={() => setModalOpen(false)}>Cancel</s-button>
        <s-button tone="critical" onClick={handleDelete}>Delete</s-button>
      </s-button-group>
    </div>
  </s-modal>
)}
```

### 2.5 Event Handling

```typescript
// Web Components use native DOM events
function FormExample() {
  const [value, setValue] = useState('')

  // onInput fires on every keystroke
  const handleInput = (e: React.FormEvent<HTMLElement>) => {
    setValue((e.target as HTMLInputElement).value)
  }

  // onChange fires when focus is lost or Enter is pressed
  const handleChange = (e: React.FormEvent<HTMLElement>) => {
    console.log('Final value:', (e.target as HTMLInputElement).value)
  }

  return (
    <s-text-field
      label="Product Name"
      value={value}
      onInput={handleInput}
      onChange={handleChange}
    />
  )
}
```

---

## 3. Shopify App Bridge (Direct Initialization)

### 3.1 App Bridge Setup

```typescript
// src/lib/app-bridge.ts
import { createApp, type ClientApplication } from '@shopify/app-bridge'
import { getSessionToken } from '@shopify/app-bridge/utilities'
import { env } from '@/env'

let app: ClientApplication | null = null

export function getAppBridge(): ClientApplication {
  if (!app) {
    const host = new URLSearchParams(window.location.search).get('host')
    if (!host) {
      throw new Error('Missing host parameter. Access app from Shopify admin.')
    }
    app = createApp({
      apiKey: env.VITE_SHOPIFY_API_KEY,
      host,
    })
  }
  return app
}

export async function getAuthToken(): Promise<string> {
  const app = getAppBridge()
  return getSessionToken(app)
}
```

### 3.2 Authenticated Fetch Hook

```typescript
// src/hooks/useAuthenticatedFetch.ts
import { useCallback } from 'react'
import { getAuthToken } from '@/lib/app-bridge'
import { env } from '@/env'

export function useAuthenticatedFetch() {
  const authenticatedFetch = useCallback(
    async (uri: string, options?: RequestInit) => {
      const sessionToken = await getAuthToken()
      const url = uri.startsWith('http') ? uri : `${env.VITE_API_URL}${uri}`

      const response = await fetch(url, {
        ...options,
        headers: {
          ...options?.headers,
          'Authorization': `Bearer ${sessionToken}`,
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`Request failed: ${response.statusText}`)
      }

      return response
    },
    []
  )

  return authenticatedFetch
}
```

### 3.3 Navigation Hook

```typescript
// src/hooks/useNavigation.ts
import { Redirect } from '@shopify/app-bridge/actions'
import { getAppBridge } from '@/lib/app-bridge'

export function useNavigation() {
  const navigateTo = (path: string) => {
    const app = getAppBridge()
    const redirect = Redirect.create(app)
    redirect.dispatch(Redirect.Action.APP, path)
  }

  const navigateToAdmin = (path: string) => {
    const app = getAppBridge()
    const redirect = Redirect.create(app)
    redirect.dispatch(Redirect.Action.ADMIN_PATH, path)
  }

  const navigateExternal = (url: string) => {
    const app = getAppBridge()
    const redirect = Redirect.create(app)
    redirect.dispatch(Redirect.Action.REMOTE, url)
  }

  return { navigateTo, navigateToAdmin, navigateExternal }
}
```

### 3.4 Toast Hook

```typescript
// src/hooks/useToast.ts
import { Toast } from '@shopify/app-bridge/actions'
import { getAppBridge } from '@/lib/app-bridge'

export function useToast() {
  const showToast = (message: string, options?: { isError?: boolean; duration?: number }) => {
    const app = getAppBridge()
    const toast = Toast.create(app, {
      message,
      duration: options?.duration ?? 3000,
      isError: options?.isError ?? false,
    })
    toast.dispatch(Toast.Action.SHOW)
  }

  return { showToast }
}

// Usage
function MyComponent() {
  const { showToast } = useToast()

  const handleSave = async () => {
    try {
      await saveData()
      showToast('Saved successfully')
    } catch (error) {
      showToast('Failed to save', { isError: true })
    }
  }

  return <s-button onClick={handleSave}>Save</s-button>
}
```

---

## 4. Data Fetching with TanStack Query

### 4.1 Query Client Setup

```typescript
// src/main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: (failureCount, error) => {
        // Don't retry on 4xx errors
        if (error instanceof Error && error.message.includes('4')) {
          return false
        }
        return failureCount < 2
      },
      refetchOnWindowFocus: false,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </React.StrictMode>
)
```

### 4.2 Query Key Factory Pattern

```typescript
// src/lib/query-keys.ts

// Product keys
export const productKeys = {
  all: ['products'] as const,
  lists: () => [...productKeys.all, 'list'] as const,
  list: (filters: ProductFilters) => [...productKeys.lists(), filters] as const,
  details: () => [...productKeys.all, 'detail'] as const,
  detail: (id: string) => [...productKeys.details(), id] as const,
}

// Order keys
export const orderKeys = {
  all: ['orders'] as const,
  lists: () => [...orderKeys.all, 'list'] as const,
  list: (filters: OrderFilters) => [...orderKeys.lists(), filters] as const,
  details: () => [...orderKeys.all, 'detail'] as const,
  detail: (id: string) => [...orderKeys.details(), id] as const,
}

// Customer keys
export const customerKeys = {
  all: ['customers'] as const,
  lists: () => [...customerKeys.all, 'list'] as const,
  list: (filters: CustomerFilters) => [...customerKeys.lists(), filters] as const,
  details: () => [...customerKeys.all, 'detail'] as const,
  detail: (id: string) => [...customerKeys.details(), id] as const,
}
```

### 4.3 useQuery with Zod Validation

```typescript
// src/hooks/useProducts.ts
import { useQuery } from '@tanstack/react-query'
import { z } from 'zod'
import { useAuthenticatedFetch } from './useAuthenticatedFetch'
import { productKeys } from '@/lib/query-keys'

// Define response schema
const productSchema = z.object({
  id: z.string(),
  name: z.string(),
  price: z.number(),
  status: z.enum(['active', 'draft', 'archived']),
  createdAt: z.string().datetime(),
})

const productsResponseSchema = z.object({
  success: z.boolean(),
  data: z.array(productSchema),
  meta: z.object({
    total: z.number(),
    page: z.number(),
    pageSize: z.number(),
  }),
})

export type Product = z.infer<typeof productSchema>
export type ProductFilters = { status?: string; search?: string }

export function useProducts(filters?: ProductFilters) {
  const fetch = useAuthenticatedFetch()

  return useQuery({
    queryKey: productKeys.list(filters ?? {}),
    queryFn: async () => {
      const params = new URLSearchParams(filters as Record<string, string>)
      const response = await fetch(`/api/v1/products?${params}`)
      const json = await response.json()

      // Validate response with Zod
      const validated = productsResponseSchema.parse(json)
      return validated.data
    },
  })
}

// Usage
function ProductList() {
  const { data: products, isLoading, error } = useProducts({ status: 'active' })

  if (isLoading) return <s-spinner size="large" />
  if (error) return <s-banner tone="critical">Failed to load products</s-banner>

  return (
    <s-page title="Products">
      <s-section>
        <s-stack gap="base">
          {products?.map((product) => (
            <s-box key={product.id} padding="base" background="surface">
              <s-stack direction="inline" gap="base">
                <s-text type="strong">{product.name}</s-text>
                <s-badge tone={product.status === 'active' ? 'success' : 'warning'}>
                  {product.status}
                </s-badge>
                <s-text>${product.price}</s-text>
              </s-stack>
            </s-box>
          ))}
        </s-stack>
      </s-section>
    </s-page>
  )
}
```

### 4.4 useMutation Pattern

```typescript
// src/hooks/useCreateProduct.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { z } from 'zod'
import { useAuthenticatedFetch } from './useAuthenticatedFetch'
import { productKeys } from '@/lib/query-keys'
import { useToast } from './useToast'

const createProductSchema = z.object({
  name: z.string().min(3),
  price: z.number().positive(),
  description: z.string().optional(),
})

export type CreateProductDto = z.infer<typeof createProductSchema>

export function useCreateProduct() {
  const fetch = useAuthenticatedFetch()
  const queryClient = useQueryClient()
  const { showToast } = useToast()

  return useMutation({
    mutationFn: async (data: CreateProductDto) => {
      // Validate input before sending
      const validated = createProductSchema.parse(data)

      const response = await fetch('/api/v1/products', {
        method: 'POST',
        body: JSON.stringify(validated),
      })
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: productKeys.lists() })
      showToast('Product created successfully')
    },
    onError: (error) => {
      showToast(error.message, { isError: true })
    },
  })
}
```

### 4.5 Optimistic Updates

```typescript
// src/hooks/useUpdateProduct.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useAuthenticatedFetch } from './useAuthenticatedFetch'
import { productKeys, type Product } from '@/lib/query-keys'

interface UpdateProductDto {
  name?: string
  price?: number
  status?: string
}

export function useUpdateProduct(productId: string) {
  const fetch = useAuthenticatedFetch()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: UpdateProductDto) => {
      const response = await fetch(`/api/v1/products/${productId}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      })
      return response.json()
    },
    onMutate: async (updatedData) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: productKeys.detail(productId) })

      // Snapshot previous value
      const previousProduct = queryClient.getQueryData<Product>(
        productKeys.detail(productId)
      )

      // Optimistically update
      queryClient.setQueryData<Product>(
        productKeys.detail(productId),
        (old) => old ? { ...old, ...updatedData } : undefined
      )

      return { previousProduct }
    },
    onError: (err, updatedData, context) => {
      // Rollback on error
      if (context?.previousProduct) {
        queryClient.setQueryData(
          productKeys.detail(productId),
          context.previousProduct
        )
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: productKeys.detail(productId) })
    },
  })
}
```

### 4.6 Prefetching Pattern

```typescript
// Prefetch on hover
function ProductList({ products }: { products: Product[] }) {
  const queryClient = useQueryClient()
  const fetch = useAuthenticatedFetch()

  const prefetchProduct = (id: string) => {
    queryClient.prefetchQuery({
      queryKey: productKeys.detail(id),
      queryFn: async () => {
        const response = await fetch(`/api/v1/products/${id}`)
        return response.json()
      },
      staleTime: 5 * 60 * 1000,
    })
  }

  return (
    <s-stack gap="base">
      {products.map((product) => (
        <s-link
          key={product.id}
          url={`/products/${product.id}`}
          onMouseEnter={() => prefetchProduct(product.id)}
        >
          {product.name}
        </s-link>
      ))}
    </s-stack>
  )
}
```

### 4.7 Parallel Queries

```typescript
import { useQueries } from '@tanstack/react-query'

function Dashboard() {
  const fetch = useAuthenticatedFetch()

  const results = useQueries({
    queries: [
      {
        queryKey: orderKeys.lists(),
        queryFn: async () => {
          const response = await fetch('/api/v1/orders')
          return response.json()
        },
      },
      {
        queryKey: productKeys.lists(),
        queryFn: async () => {
          const response = await fetch('/api/v1/products')
          return response.json()
        },
      },
      {
        queryKey: customerKeys.lists(),
        queryFn: async () => {
          const response = await fetch('/api/v1/customers')
          return response.json()
        },
      },
    ],
  })

  const [orders, products, customers] = results
  const isLoading = results.some((r) => r.isLoading)

  if (isLoading) return <s-spinner size="large" />

  return (
    <s-page title="Dashboard">
      <s-grid columns="3">
        <s-box>Orders: {orders.data?.length}</s-box>
        <s-box>Products: {products.data?.length}</s-box>
        <s-box>Customers: {customers.data?.length}</s-box>
      </s-grid>
    </s-page>
  )
}
```

### 4.8 Dependent Queries

```typescript
function ProductDetails({ productId }: { productId: string }) {
  const fetch = useAuthenticatedFetch()

  // First query - get product
  const { data: product } = useQuery({
    queryKey: productKeys.detail(productId),
    queryFn: async () => {
      const response = await fetch(`/api/v1/products/${productId}`)
      return response.json()
    },
  })

  // Dependent query - get related products (only when product loaded)
  const { data: relatedProducts } = useQuery({
    queryKey: ['products', 'related', product?.categoryId],
    queryFn: async () => {
      const response = await fetch(`/api/v1/products?category=${product!.categoryId}`)
      return response.json()
    },
    enabled: !!product?.categoryId, // Only fetch when product has categoryId
  })

  // ...
}
```

---

## 5. Form Handling with React Hook Form + Zod

### 5.1 Basic Form with Validation

```typescript
// src/components/ProductForm.tsx
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useCreateProduct } from '@/hooks/useCreateProduct'

// Define schema
const productSchema = z.object({
  name: z.string()
    .min(3, 'Name must be at least 3 characters')
    .max(100, 'Name must be less than 100 characters'),
  price: z.number()
    .positive('Price must be positive')
    .max(999999, 'Price must be less than $999,999'),
  status: z.enum(['draft', 'active', 'archived']),
  description: z.string().optional(),
})

type ProductFormData = z.infer<typeof productSchema>

export function ProductForm({ onSuccess }: { onSuccess?: () => void }) {
  const createProduct = useCreateProduct()

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ProductFormData>({
    resolver: zodResolver(productSchema),
    defaultValues: {
      name: '',
      price: 0,
      status: 'draft',
      description: '',
    },
  })

  const onSubmit = async (data: ProductFormData) => {
    await createProduct.mutateAsync(data)
    reset()
    onSuccess?.()
  }

  return (
    <s-page title="Create Product">
      <form onSubmit={handleSubmit(onSubmit)}>
        <s-section>
          <s-stack gap="base">
            <Controller
              name="name"
              control={control}
              render={({ field }) => (
                <s-text-field
                  label="Product Name"
                  value={field.value}
                  onInput={(e) => field.onChange((e.target as HTMLInputElement).value)}
                  onBlur={field.onBlur}
                  error={errors.name?.message}
                  required
                />
              )}
            />

            <Controller
              name="price"
              control={control}
              render={({ field }) => (
                <s-text-field
                  label="Price"
                  type="number"
                  value={field.value.toString()}
                  onInput={(e) => field.onChange(parseFloat((e.target as HTMLInputElement).value) || 0)}
                  onBlur={field.onBlur}
                  error={errors.price?.message}
                  required
                />
              )}
            />

            <Controller
              name="status"
              control={control}
              render={({ field }) => (
                <s-select
                  label="Status"
                  value={field.value}
                  onChange={(e) => field.onChange((e.target as HTMLSelectElement).value)}
                  options={JSON.stringify([
                    { label: 'Draft', value: 'draft' },
                    { label: 'Active', value: 'active' },
                    { label: 'Archived', value: 'archived' },
                  ])}
                />
              )}
            />

            <Controller
              name="description"
              control={control}
              render={({ field }) => (
                <s-text-field
                  label="Description"
                  value={field.value || ''}
                  onInput={(e) => field.onChange((e.target as HTMLInputElement).value)}
                  onBlur={field.onBlur}
                  error={errors.description?.message}
                />
              )}
            />

            <s-button-group>
              <s-button type="button" onClick={() => reset()}>
                Reset
              </s-button>
              <s-button
                type="submit"
                variant="primary"
                loading={isSubmitting}
                disabled={isSubmitting}
              >
                Create Product
              </s-button>
            </s-button-group>
          </s-stack>
        </s-section>
      </form>
    </s-page>
  )
}
```

### 5.2 Edit Form with Existing Data

```typescript
// src/components/EditProductForm.tsx
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useUpdateProduct } from '@/hooks/useUpdateProduct'
import { useProduct } from '@/hooks/useProduct'

const productSchema = z.object({
  name: z.string().min(3),
  price: z.number().positive(),
  status: z.enum(['draft', 'active', 'archived']),
})

type ProductFormData = z.infer<typeof productSchema>

export function EditProductForm({ productId }: { productId: string }) {
  const { data: product, isLoading } = useProduct(productId)
  const updateProduct = useUpdateProduct(productId)

  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting, isDirty },
  } = useForm<ProductFormData>({
    resolver: zodResolver(productSchema),
    values: product ? {
      name: product.name,
      price: product.price,
      status: product.status,
    } : undefined,
  })

  if (isLoading) return <s-spinner size="large" />

  const onSubmit = async (data: ProductFormData) => {
    await updateProduct.mutateAsync(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <s-section heading="Edit Product">
        <s-stack gap="base">
          <Controller
            name="name"
            control={control}
            render={({ field }) => (
              <s-text-field
                label="Name"
                value={field.value}
                onInput={(e) => field.onChange((e.target as HTMLInputElement).value)}
                error={errors.name?.message}
              />
            )}
          />

          <Controller
            name="price"
            control={control}
            render={({ field }) => (
              <s-text-field
                label="Price"
                type="number"
                value={field.value.toString()}
                onInput={(e) => field.onChange(parseFloat((e.target as HTMLInputElement).value) || 0)}
                error={errors.price?.message}
              />
            )}
          />

          <s-button
            type="submit"
            variant="primary"
            loading={isSubmitting}
            disabled={!isDirty || isSubmitting}
          >
            Save Changes
          </s-button>
        </s-stack>
      </s-section>
    </form>
  )
}
```

### 5.3 Complex Validation with Zod

```typescript
// Complex schema with refinements
const orderSchema = z.object({
  customer: z.object({
    email: z.string().email('Invalid email'),
    name: z.string().min(2, 'Name required'),
  }),
  items: z.array(z.object({
    productId: z.string(),
    quantity: z.number().int().positive(),
    price: z.number().positive(),
  })).min(1, 'At least one item required'),
  shipping: z.object({
    address: z.string().min(10, 'Full address required'),
    city: z.string().min(2),
    zip: z.string().regex(/^\d{5}(-\d{4})?$/, 'Invalid ZIP code'),
  }),
  discountCode: z.string().optional(),
}).refine(
  (data) => {
    const total = data.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
    return total > 0
  },
  { message: 'Order total must be greater than 0', path: ['items'] }
)

// Async validation
const usernameSchema = z.string()
  .min(3)
  .refine(
    async (username) => {
      const response = await fetch(`/api/check-username?username=${username}`)
      const { available } = await response.json()
      return available
    },
    { message: 'Username already taken' }
  )
```

### 5.4 Reusable Form Field Component

```typescript
// src/components/FormField.tsx
import { Controller, useFormContext } from 'react-hook-form'

interface FormFieldProps {
  name: string
  label: string
  type?: 'text' | 'number' | 'email' | 'password'
  required?: boolean
  placeholder?: string
}

export function FormField({ name, label, type = 'text', required, placeholder }: FormFieldProps) {
  const { control, formState: { errors } } = useFormContext()

  // Get nested error
  const error = name.split('.').reduce((err: any, key) => err?.[key], errors)

  return (
    <Controller
      name={name}
      control={control}
      render={({ field }) => (
        <s-text-field
          label={label}
          type={type}
          value={type === 'number' ? field.value?.toString() : field.value}
          onInput={(e) => {
            const value = (e.target as HTMLInputElement).value
            field.onChange(type === 'number' ? parseFloat(value) || 0 : value)
          }}
          onBlur={field.onBlur}
          error={error?.message}
          required={required}
          placeholder={placeholder}
        />
      )}
    />
  )
}

// Usage with FormProvider
import { useForm, FormProvider } from 'react-hook-form'

function MyForm() {
  const methods = useForm({ resolver: zodResolver(schema) })

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        <FormField name="email" label="Email" type="email" required />
        <FormField name="name" label="Name" required />
        <FormField name="age" label="Age" type="number" />
      </form>
    </FormProvider>
  )
}
```

---

## 6. Zod Validation Patterns

### 6.1 API Response Validation

```typescript
// src/lib/api-schemas.ts
import { z } from 'zod'

// Base response wrapper
const apiResponseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    success: z.boolean(),
    data: dataSchema,
    error: z.string().optional(),
  })

// Product schemas
export const productSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  price: z.number().nonnegative(),
  status: z.enum(['active', 'draft', 'archived']),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
})

export const productsResponseSchema = apiResponseSchema(z.array(productSchema))
export const productResponseSchema = apiResponseSchema(productSchema)

// Type exports
export type Product = z.infer<typeof productSchema>
export type ProductsResponse = z.infer<typeof productsResponseSchema>
```

### 6.2 Safe Fetch Wrapper

```typescript
// src/lib/safe-fetch.ts
import { z } from 'zod'

export async function safeFetch<T>(
  url: string,
  schema: z.ZodType<T>,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(url, options)

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`)
  }

  const json = await response.json()

  // Validate and parse response
  const result = schema.safeParse(json)

  if (!result.success) {
    console.error('API response validation failed:', result.error.issues)
    throw new Error('Invalid API response format')
  }

  return result.data
}

// Usage
const products = await safeFetch('/api/products', productsResponseSchema)
```

### 6.3 Form Schema Patterns

```typescript
// Reusable field schemas
const emailField = z.string().email('Invalid email address')
const phoneField = z.string().regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number')
const priceField = z.number().positive('Must be positive').multipleOf(0.01)
const slugField = z.string().regex(/^[a-z0-9-]+$/, 'Only lowercase letters, numbers, and hyphens')

// Compose schemas
const contactSchema = z.object({
  email: emailField,
  phone: phoneField.optional(),
})

const productSchema = z.object({
  name: z.string().min(1).max(200),
  slug: slugField,
  price: priceField,
  compareAtPrice: priceField.optional(),
}).refine(
  (data) => !data.compareAtPrice || data.compareAtPrice > data.price,
  { message: 'Compare at price must be higher than price', path: ['compareAtPrice'] }
)
```

---

## 7. Error Handling

### 7.1 Error Boundary

```typescript
// src/components/ErrorBoundary.tsx
import { Component, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('Error caught by boundary:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <s-page title="Error">
          <s-section>
            <s-banner tone="critical" heading="Something went wrong">
              <s-text>Please refresh the page and try again.</s-text>
              {this.state.error && (
                <s-text tone="subdued">{this.state.error.message}</s-text>
              )}
            </s-banner>
          </s-section>
        </s-page>
      )
    }

    return this.props.children
  }
}
```

### 7.2 Query Error Handling Component

```typescript
// src/components/QueryErrorBoundary.tsx
import { QueryErrorResetBoundary } from '@tanstack/react-query'
import { ErrorBoundary } from 'react-error-boundary'

function ErrorFallback({ error, resetErrorBoundary }: { error: Error; resetErrorBoundary: () => void }) {
  return (
    <s-section>
      <s-banner tone="critical" heading="Failed to load data">
        <s-text>{error.message}</s-text>
        <s-button onClick={resetErrorBoundary}>Try again</s-button>
      </s-banner>
    </s-section>
  )
}

export function QueryErrorBoundary({ children }: { children: React.ReactNode }) {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary onReset={reset} FallbackComponent={ErrorFallback}>
          {children}
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  )
}
```

---

## 8. Performance Optimization

### 8.1 Memoization

```typescript
import { useMemo, useCallback, memo } from 'react'

function ProductList({ products }: { products: Product[] }) {
  // Memoize expensive calculations
  const sortedProducts = useMemo(() => {
    return [...products].sort((a, b) => b.price - a.price)
  }, [products])

  const totalValue = useMemo(() => {
    return products.reduce((sum, p) => sum + p.price, 0)
  }, [products])

  // Stable callback reference
  const handleSelect = useCallback((id: string) => {
    console.log('Selected:', id)
  }, [])

  return (
    <s-section>
      <s-text>Total: ${totalValue}</s-text>
      <s-stack gap="base">
        {sortedProducts.map((p) => (
          <ProductCard key={p.id} product={p} onSelect={handleSelect} />
        ))}
      </s-stack>
    </s-section>
  )
}

// Memoized component
const ProductCard = memo(function ProductCard({
  product,
  onSelect,
}: {
  product: Product
  onSelect: (id: string) => void
}) {
  return (
    <s-box padding="base" background="surface">
      <s-stack direction="inline" gap="base">
        <s-text type="strong">{product.name}</s-text>
        <s-button onClick={() => onSelect(product.id)}>Select</s-button>
      </s-stack>
    </s-box>
  )
})
```

### 8.2 Virtual Scrolling for Large Lists

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'
import { useRef } from 'react'

export function VirtualizedProductList({ products }: { products: Product[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: products.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 80,
  })

  return (
    <div
      ref={parentRef}
      style={{ height: '600px', overflow: 'auto' }}
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: '100%',
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => {
          const product = products[virtualItem.index]
          return (
            <div
              key={virtualItem.key}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: `${virtualItem.size}px`,
                transform: `translateY(${virtualItem.start}px)`,
              }}
            >
              <s-box padding="base" background="surface">
                <s-text>{product.name}</s-text>
              </s-box>
            </div>
          )
        })}
      </div>
    </div>
  )
}
```

---

## 9. Custom Hooks

### 9.1 useDebounce

```typescript
import { useEffect, useState } from 'react'

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// Usage
function SearchProducts() {
  const [searchTerm, setSearchTerm] = useState('')
  const debouncedSearch = useDebounce(searchTerm, 500)

  const { data } = useProducts({ search: debouncedSearch })

  return (
    <s-text-field
      label="Search"
      value={searchTerm}
      onInput={(e) => setSearchTerm((e.target as HTMLInputElement).value)}
    />
  )
}
```

### 9.2 useLocalStorage

```typescript
import { useState, useEffect } from 'react'

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch {
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error('Failed to save to localStorage:', error)
    }
  }

  return [storedValue, setValue] as const
}
```

---

## 10. Best Practices

### DO

```typescript
// Use Polaris Web Components with s- prefix
<s-page title="Products">
  <s-section>
    <s-button variant="primary">Save</s-button>
  </s-section>
</s-page>

// Use React Hook Form with Zod
const { control, handleSubmit } = useForm({
  resolver: zodResolver(schema),
})

// Use query key factories
const { data } = useQuery({
  queryKey: productKeys.detail(id),
  queryFn: () => fetchProduct(id),
})

// Validate API responses with Zod
const data = responseSchema.parse(json)

// Use Controller for Web Components
<Controller
  name="email"
  control={control}
  render={({ field }) => (
    <s-text-field
      value={field.value}
      onInput={(e) => field.onChange(e.target.value)}
    />
  )}
/>

// Handle loading and error states
if (isLoading) return <s-spinner />
if (error) return <s-banner tone="critical">Error</s-banner>
```

### DON'T

```typescript
// Don't use React Polaris imports
import { Page, Button } from '@shopify/polaris' // WRONG - use Web Components

// Don't use AppProvider (not needed for Web Components)
<AppProvider i18n={translations}> // NOT NEEDED

// Don't use manual form validation with useState
const [errors, setErrors] = useState({}) // USE React Hook Form + Zod

// Don't use inline query keys
queryKey: ['products', id, 'details'] // USE query key factories

// Don't ignore TypeScript
const data: any = response // WRONG - use Zod schemas

// Don't use register() directly with Web Components
<s-text-field {...register('name')} /> // WRONG - use Controller
```

---

## 11. Project Structure

```
frontend/
+-- src/
|   +-- main.tsx              # App entry point
|   +-- App.tsx               # Root component
|   +-- env.ts                # Validated environment variables
|   +-- pages/                # Route components
|   |   +-- Dashboard.tsx
|   |   +-- Products.tsx
|   |   +-- Settings.tsx
|   +-- components/           # Reusable components
|   |   +-- ProductCard.tsx
|   |   +-- ProductForm.tsx
|   |   +-- ErrorBoundary.tsx
|   |   +-- FormField.tsx
|   +-- hooks/                # Custom hooks
|   |   +-- useAuthenticatedFetch.ts
|   |   +-- useProducts.ts
|   |   +-- useToast.ts
|   |   +-- useDebounce.ts
|   +-- lib/                  # Utilities and configs
|   |   +-- app-bridge.ts
|   |   +-- query-keys.ts
|   |   +-- api-schemas.ts
|   |   +-- safe-fetch.ts
|   +-- types/                # TypeScript types (use @shopify/polaris-types package)
|   |   +-- product.ts
|   +-- styles/
|       +-- index.css
+-- public/
+-- index.html                # With Polaris CDN scripts
+-- vite.config.ts
+-- tsconfig.json
+-- package.json
+-- .env
```

---

## 12. Migration Guide

### From React Polaris to Web Components

#### Step 1: Update Dependencies

```bash
# Remove React Polaris
npm uninstall @shopify/polaris @shopify/app-bridge-react

# Add new dependencies
npm install @shopify/app-bridge react-hook-form @hookform/resolvers zod

# Add TypeScript types for Web Components
npm install --save-dev @shopify/app-bridge-types @shopify/polaris-types
```

Update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["@shopify/app-bridge-types", "@shopify/polaris-types"]
  }
}
```

#### Step 2: Add CDN Scripts to index.html

```html
<head>
  <script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
  <script src="https://cdn.shopify.com/shopifycloud/polaris.js" type="module"></script>
</head>
```

#### Step 3: Component Migration Reference

| React Polaris | Web Component |
|---------------|---------------|
| `<Page>` | `<s-page>` |
| `<Layout>` | `<s-stack>` + `<s-grid>` |
| `<Card>` | `<s-section>` or `<s-box>` |
| `<Button>` | `<s-button>` |
| `<TextField>` | `<s-text-field>` |
| `<Select>` | `<s-select>` |
| `<Checkbox>` | `<s-checkbox>` |
| `<Banner>` | `<s-banner>` |
| `<Modal>` | `<s-modal>` |
| `<Spinner>` | `<s-spinner>` |
| `<Badge>` | `<s-badge>` |
| `<DataTable>` | `<s-table>` |

#### Step 4: Update App Bridge

```typescript
// Before: React Provider
import { Provider } from '@shopify/app-bridge-react'
<Provider config={config}>
  <App />
</Provider>

// After: Direct initialization
import { createApp } from '@shopify/app-bridge'
const app = createApp({ apiKey, host })
```

#### Step 5: Migrate Forms to React Hook Form + Zod

```typescript
// Before: Manual state management
const [name, setName] = useState('')
const [errors, setErrors] = useState({})

// After: React Hook Form + Zod
const { control, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(schema)
})
```

### Incremental Migration

React Polaris and Web Components can coexist during migration:

1. Add CDN scripts alongside existing React Polaris
2. Migrate one page at a time
3. Both `<Page>` and `<s-page>` work in the same app
4. Remove `@shopify/polaris` after all pages migrated

---

## Quick Reference

### Polaris Web Components

```typescript
<s-page title="Title">
  <s-section heading="Section">
    <s-stack gap="base">
      <s-text-field label="Name" />
      <s-button variant="primary">Save</s-button>
    </s-stack>
  </s-section>
</s-page>
```

### React Hook Form + Zod

```typescript
const schema = z.object({ name: z.string().min(1) })
const { control, handleSubmit } = useForm({ resolver: zodResolver(schema) })

<Controller name="name" control={control} render={({ field }) => (
  <s-text-field {...field} onInput={(e) => field.onChange(e.target.value)} />
)} />
```

### TanStack Query

```typescript
// Query with key factory
const { data } = useQuery({
  queryKey: productKeys.detail(id),
  queryFn: () => safeFetch(`/api/products/${id}`, productSchema),
})

// Mutation with invalidation
const mutation = useMutation({
  mutationFn: createProduct,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: productKeys.lists() }),
})
```

### App Bridge

```typescript
const app = getAppBridge()
const token = await getAuthToken()
```

---

## Resources

- [Shopify Polaris Web Components](https://shopify.dev/docs/api/app-home/polaris-web-components)
- [React Hook Form](https://react-hook-form.com/)
- [Zod Documentation](https://zod.dev/)
- [TanStack Query](https://tanstack.com/query/latest)
- [Shopify App Bridge](https://shopify.dev/docs/api/app-bridge)
- [Vite Documentation](https://vitejs.dev/)
