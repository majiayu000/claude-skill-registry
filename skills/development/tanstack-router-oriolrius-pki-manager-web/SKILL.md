---
name: TanStack Router
description: Expert guidance for TanStack Router including file-based routing, type-safe navigation, route loaders, search params, nested routes, and lazy loading. Use this when building type-safe React applications with client-side routing.
---

# TanStack Router

Expert assistance with TanStack Router - Type-safe routing for React.

## Overview

TanStack Router is a fully type-safe React router:
- **File-Based Routing**: Automatic route generation from file structure
- **Type Safety**: Full TypeScript inference for params, search, and more
- **Code Splitting**: Automatic route-based code splitting
- **Data Loading**: Built-in data loaders
- **Search Params**: Type-safe search parameter handling

## Installation

```bash
npm install @tanstack/react-router
npm install --save-dev @tanstack/router-vite-plugin
```

## Basic Setup

### Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { TanStackRouterVite } from '@tanstack/router-vite-plugin';

export default defineConfig({
  plugins: [
    react(),
    TanStackRouterVite(),
  ],
});
```

### Root Route

```typescript
// src/routes/__root.tsx
import { createRootRoute, Outlet } from '@tanstack/react-router';

export const Route = createRootRoute({
  component: () => (
    <>
      <div>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/certificates">Certificates</Link>
        </nav>
      </div>
      <hr />
      <Outlet />
    </>
  ),
});
```

### Index Route

```typescript
// src/routes/index.tsx
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/')({
  component: () => <div>Home Page</div>,
});
```

## File-Based Routing

```
src/routes/
├── __root.tsx                  -> /
├── index.tsx                   -> /
├── certificates/
│   ├── index.tsx              -> /certificates
│   └── $id.tsx                -> /certificates/:id
├── cas/
│   ├── index.tsx              -> /cas
│   ├── $id.tsx                -> /cas/:id
│   └── $id.edit.tsx           -> /cas/:id/edit
└── audit.tsx                   -> /audit
```

### Dynamic Routes

```typescript
// src/routes/certificates/$id.tsx
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/certificates/$id')({
  component: CertificateDetail,
});

function CertificateDetail() {
  const { id } = Route.useParams(); // Type-safe!
  return <div>Certificate: {id}</div>;
}
```

### Nested Routes

```typescript
// src/routes/certificates.tsx (layout)
import { createFileRoute, Outlet } from '@tanstack/react-router';

export const Route = createFileRoute('/certificates')({
  component: () => (
    <div>
      <h1>Certificates</h1>
      <Outlet /> {/* Render child routes */}
    </div>
  ),
});

// src/routes/certificates/index.tsx
export const Route = createFileRoute('/certificates/')({
  component: () => <div>Certificate List</div>,
});

// src/routes/certificates/$id.tsx
export const Route = createFileRoute('/certificates/$id')({
  component: () => {
    const { id } = Route.useParams();
    return <div>Certificate {id}</div>;
  },
});
```

## Navigation

```typescript
import { Link, useNavigate } from '@tanstack/react-router';

function MyComponent() {
  const navigate = useNavigate();

  return (
    <>
      {/* Link component */}
      <Link to="/certificates">Certificates</Link>

      {/* With params */}
      <Link to="/certificates/$id" params={{ id: '123' }}>
        Certificate 123
      </Link>

      {/* With search params */}
      <Link to="/certificates" search={{ filter: 'active' }}>
        Active Certificates
      </Link>

      {/* Programmatic navigation */}
      <button onClick={() => navigate({ to: '/certificates' })}>
        Go to Certificates
      </button>

      {/* Navigate with params */}
      <button onClick={() => navigate({
        to: '/certificates/$id',
        params: { id: '123' },
      })}>
        View Certificate
      </button>
    </>
  );
}
```

## Search Params

### Define Search Schema

```typescript
import { createFileRoute } from '@tanstack/react-router';
import { z } from 'zod';

const searchSchema = z.object({
  filter: z.enum(['all', 'active', 'revoked']).optional().default('all'),
  page: z.number().optional().default(1),
  pageSize: z.number().optional().default(10),
});

export const Route = createFileRoute('/certificates/')({
  validateSearch: searchSchema,
  component: CertificateList,
});

function CertificateList() {
  const { filter, page, pageSize } = Route.useSearch(); // Type-safe!

  return (
    <div>
      <p>Filter: {filter}, Page: {page}</p>
    </div>
  );
}
```

### Update Search Params

```typescript
import { useNavigate } from '@tanstack/react-router';

function FilterButtons() {
  const navigate = useNavigate({ from: '/certificates' });
  const search = Route.useSearch();

  return (
    <>
      <button onClick={() => navigate({
        search: (prev) => ({ ...prev, filter: 'active' }),
      })}>
        Active
      </button>

      <button onClick={() => navigate({
        search: { filter: 'revoked', page: 1 },
      })}>
        Revoked
      </button>
    </>
  );
}
```

## Route Loaders

```typescript
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/certificates/$id')({
  loader: async ({ params }) => {
    const certificate = await fetchCertificate(params.id);
    return { certificate };
  },
  component: CertificateDetail,
});

function CertificateDetail() {
  const { certificate } = Route.useLoaderData();
  return <div>{certificate.subject}</div>;
}
```

### Loader with Context

```typescript
// src/router.tsx
import { createRouter } from '@tanstack/react-router';

const router = createRouter({
  routeTree,
  context: {
    queryClient, // React Query client
    auth, // Auth context
  },
});

// Route with context
export const Route = createFileRoute('/certificates/$id')({
  loader: async ({ params, context }) => {
    const certificate = await context.queryClient.fetchQuery({
      queryKey: ['certificate', params.id],
      queryFn: () => fetchCertificate(params.id),
    });
    return { certificate };
  },
});
```

## Lazy Loading

```typescript
// src/routes/certificates/$id.lazy.tsx
import { createLazyFileRoute } from '@tanstack/react-router';

export const Route = createLazyFileRoute('/certificates/$id')({
  component: CertificateDetail,
});

// Component defined in same file (lazy loaded)
function CertificateDetail() {
  const { id } = Route.useParams();
  return <div>Certificate: {id}</div>;
}
```

## Error Handling

```typescript
export const Route = createFileRoute('/certificates/$id')({
  loader: async ({ params }) => {
    const certificate = await fetchCertificate(params.id);
    if (!certificate) {
      throw new Error('Certificate not found');
    }
    return { certificate };
  },
  errorComponent: ({ error }) => (
    <div>
      <h2>Error!</h2>
      <p>{error.message}</p>
    </div>
  ),
  component: CertificateDetail,
});
```

## Pending/Loading States

```typescript
export const Route = createFileRoute('/certificates/$id')({
  loader: async ({ params }) => {
    const certificate = await fetchCertificate(params.id);
    return { certificate };
  },
  pendingComponent: () => <div>Loading certificate...</div>,
  component: CertificateDetail,
});

// Or use hook
function CertificateDetail() {
  const { certificate } = Route.useLoaderData();
  const isPending = Route.useLoaderPending();

  if (isPending) return <div>Loading...</div>;

  return <div>{certificate.subject}</div>;
}
```

## Route Guards

```typescript
export const Route = createFileRoute('/admin')({
  beforeLoad: async ({ context }) => {
    if (!context.auth.isAuthenticated) {
      throw redirect({ to: '/login' });
    }
  },
  component: AdminPanel,
});
```

## Router Setup

```typescript
// src/router.tsx
import { createRouter } from '@tanstack/react-router';
import { routeTree } from './routeTree.gen';

export const router = createRouter({
  routeTree,
  defaultPreload: 'intent', // Preload on hover
  defaultPreloadStaleTime: 0,
});

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

// src/main.tsx
import { RouterProvider } from '@tanstack/react-router';
import { router } from './router';

function App() {
  return <RouterProvider router={router} />;
}
```

## Best Practices

1. **File Structure**: Organize routes by feature/domain
2. **Type Safety**: Leverage full type inference
3. **Search Params**: Define schemas for search params
4. **Code Splitting**: Use lazy routes for large components
5. **Error Boundaries**: Implement error components
6. **Loading States**: Show pending UI for better UX
7. **Preloading**: Use intent-based preloading
8. **Route Guards**: Protect routes with beforeLoad
9. **Loaders**: Fetch data in loaders, not components
10. **Context**: Share context through router

## Resources

- Documentation: https://tanstack.com/router
- GitHub: https://github.com/TanStack/router
