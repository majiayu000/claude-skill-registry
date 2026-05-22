---
name: react-tanstack-router
description: TanStack Router - 100% type-safe routing, file-based routes, loaders, search params. Use when implementing routing in React apps (NOT Next.js).
versions:
  tanstack-router: "1.x (latest)"
  react: 19
  zod: 3.x
user-invocable: true
references: references/installation.md, references/file-based-routing.md, references/route-params.md, references/search-params.md, references/loaders.md, references/navigation.md, references/route-context.md, references/nested-routes.md, references/error-handling.md, references/code-splitting.md, references/preloading.md, references/auth-guards.md, references/tanstack-query.md, references/ssr.md, references/typescript.md, references/devtools.md, references/hooks.md, references/components.md, references/templates/basic-setup.md, references/templates/feature-module.md, references/templates/auth-protected-routes.md, references/templates/search-filters.md, references/templates/dashboard-layout.md
related-skills: react-forms, react-state, react-19, solid-react
---

# TanStack Router

100% type-safe router for React with file-based routing, loaders, search params validation, and deep TanStack Query integration.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing routes and navigation patterns
2. **fuse-ai-pilot:research-expert** - Verify latest TanStack Router docs via Context7/Exa
3. **mcp__context7__query-docs** - Check file-based routing and type-safe patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### Why TanStack Router?

TanStack Router is the recommended choice for React SPAs requiring type-safe routing with search params validation.

| Feature | TanStack Router | React Router v7 |
|---------|----------------|-----------------|
| Type Safety | Full inference | Auto-generated |
| File-based Routing | Built-in | Framework mode |
| Search Params Validation | Zod, Valibot | Manual |
| Preloading | Intent, render | Limited |
| TanStack Query Integration | Native | Manual |

### When to Use

- **React SPA** with Vite, Webpack, or Rspack → See [installation.md](references/installation.md)
- **Type-safe routing** required → See [typescript.md](references/typescript.md)
- **Search params validation** needed → See [search-params.md](references/search-params.md)
- **TanStack Query** for data fetching → See [tanstack-query.md](references/tanstack-query.md)
- **NOT Next.js** (use App Router instead)

---

## Critical Rules

1. **ALWAYS use file-based routing** - Auto-generated type safety → [file-based-routing.md](references/file-based-routing.md)
2. **ALWAYS validate search params** - Use Zod schemas with `zodValidator` → [search-params.md](references/search-params.md)
3. **ALWAYS use Route.useLoaderData()** - Not global useLoaderData → [hooks.md](references/hooks.md)
4. **ALWAYS register router types** - `declare module '@tanstack/react-router'` → [typescript.md](references/typescript.md)
5. **PREFER loaders over useEffect** - Data fetching before render → [loaders.md](references/loaders.md)
6. **INTEGRATE TanStack Query** - For caching, mutations, optimistic updates → [tanstack-query.md](references/tanstack-query.md)
7. **FOLLOW SOLID architecture** - Modules, interfaces, file size limits → [solid-react skill](../solid-react/SKILL.md)

---

## Quick Reference: What to Read

### Starting a new project
1. Read [installation.md](references/installation.md) for configuration
2. Copy template [basic-setup.md](references/templates/basic-setup.md) as base

### Creating a feature module (posts, users, etc.)
1. Follow architecture in [templates/feature-module.md](references/templates/feature-module.md)
2. Use patterns from [tanstack-query.md](references/tanstack-query.md) for queries

### Implementing authentication
1. Read [auth-guards.md](references/auth-guards.md) for concepts
2. Copy template [auth-protected-routes.md](references/templates/auth-protected-routes.md)

### Creating a page with filters/search
1. Read [search-params.md](references/search-params.md) for Zod validation
2. Copy template [search-filters.md](references/templates/search-filters.md)

### Creating a dashboard with nested layouts
1. Read [nested-routes.md](references/nested-routes.md) for concepts
2. Copy template [dashboard-layout.md](references/templates/dashboard-layout.md)

---

## Project Structure (SOLID Architecture)

Recommended structure following SOLID principles from `solid-react` skill.

```text
src/
├── modules/
│   ├── cores/                      # Shared between features
│   │   ├── lib/
│   │   │   ├── router/router.ts    # Router configuration
│   │   │   └── query/client.ts     # QueryClient configuration
│   │   ├── components/layouts/     # Shared layouts
│   │   └── interfaces/             # Shared types
│   └── [feature]/                  # Feature module
│       ├── src/
│       │   ├── interfaces/         # Module types
│       │   ├── queries/            # TanStack Query options
│       │   └── components/         # Module components
│       └── index.ts                # Public exports
├── routes/                         # Route definitions ONLY
│   ├── __root.tsx
│   └── [feature]/
└── routeTree.gen.ts               # Auto-generated (DO NOT MODIFY)
```

> **Full template**: [templates/basic-setup.md](references/templates/basic-setup.md)

---

## Reference Guide

### Concepts (references/) - Conceptual Documentation

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **Setup** | [installation.md](references/installation.md) | Vite/Webpack config, React Router migration |
| **File Routing** | [file-based-routing.md](references/file-based-routing.md) | Naming conventions, routes/ structure |
| **URL Params** | [route-params.md](references/route-params.md) | Dynamic routes `$postId`, parsing |
| **Search Params** | [search-params.md](references/search-params.md) | Zod validation, URL filters, pagination |
| **Data Loading** | [loaders.md](references/loaders.md) | Loaders, prefetch, TanStack Query integration |
| **Navigation** | [navigation.md](references/navigation.md) | Link, useNavigate, redirects |
| **Context** | [route-context.md](references/route-context.md) | Dependency injection, QueryClient, user |
| **Layouts** | [nested-routes.md](references/nested-routes.md) | Nested layouts, Outlet, pathless routes |
| **Errors** | [error-handling.md](references/error-handling.md) | Error boundaries, 404, pending states |
| **Lazy Loading** | [code-splitting.md](references/code-splitting.md) | Code splitting, bundle optimization |
| **Preloading** | [preloading.md](references/preloading.md) | Preload intent/render, prefetch |
| **Auth** | [auth-guards.md](references/auth-guards.md) | Protected routes, RBAC, login redirect |
| **TanStack Query** | [tanstack-query.md](references/tanstack-query.md) | queryOptions, mutations, cache |
| **SSR** | [ssr.md](references/ssr.md) | Server-side rendering, TanStack Start |
| **TypeScript** | [typescript.md](references/typescript.md) | Type registration, inference, type safety |
| **DevTools** | [devtools.md](references/devtools.md) | Router DevTools setup |
| **Hooks API** | [hooks.md](references/hooks.md) | useParams, useSearch, useNavigate, etc. |
| **Components** | [components.md](references/components.md) | Link, Outlet, Navigate, RouterProvider |

### Templates (references/templates/) - Complete Copy-Paste Ready Code

| Template | When to use |
|----------|-------------|
| [**basic-setup.md**](references/templates/basic-setup.md) | Start a new project with SOLID architecture |
| [**feature-module.md**](references/templates/feature-module.md) | Create a complete feature module (interfaces, queries, components) |
| [**auth-protected-routes.md**](references/templates/auth-protected-routes.md) | Implement login, protected routes, RBAC |
| [**search-filters.md**](references/templates/search-filters.md) | Page with URL filters, pagination, sorting |
| [**dashboard-layout.md**](references/templates/dashboard-layout.md) | Dashboard with sidebar, tabs, nested layouts |

---

## Core Patterns

### 1. Root Route with Context

Router context configuration for dependency injection.

```typescript
// src/routes/__root.tsx
export const Route = createRootRouteWithContext<RouterContext>()({
  component: RootComponent,
})
```

> **Details**: [route-context.md](references/route-context.md)
> **Template**: [templates/basic-setup.md](references/templates/basic-setup.md)

### 2. File Route with Loader and TanStack Query

Recommended pattern for data loading with cache.

```typescript
// src/routes/posts/$postId.tsx
export const Route = createFileRoute('/posts/$postId')({
  loader: ({ context: { queryClient }, params }) =>
    queryClient.ensureQueryData(postQueryOptions(params.postId)),
  component: PostPage,
})
```

> **Details**: [loaders.md](references/loaders.md), [tanstack-query.md](references/tanstack-query.md)
> **Template**: [templates/feature-module.md](references/templates/feature-module.md)

### 3. Search Params with Zod Validation

Type-safe filters and pagination via URL.

```typescript
// src/routes/posts/index.tsx
const searchSchema = z.object({
  page: z.number().min(1).default(1),
  sort: z.enum(['newest', 'oldest']).default('newest'),
})

export const Route = createFileRoute('/posts/')({
  validateSearch: zodValidator(searchSchema),
})
```

> **Details**: [search-params.md](references/search-params.md)
> **Template**: [templates/search-filters.md](references/templates/search-filters.md)

### 4. Protected Routes

Authentication guard with redirect.

```typescript
// src/routes/_authenticated/_authenticated.tsx
export const Route = createFileRoute('/_authenticated')({
  beforeLoad: ({ context, location }) => {
    if (!context.user) {
      throw redirect({ to: '/login', search: { redirect: location.href } })
    }
  },
})
```

> **Details**: [auth-guards.md](references/auth-guards.md)
> **Template**: [templates/auth-protected-routes.md](references/templates/auth-protected-routes.md)

### 5. Nested Layouts with Outlet

Nested layouts for dashboards.

```typescript
// src/routes/_dashboard/_dashboard.tsx
export const Route = createFileRoute('/_dashboard')({
  component: () => (
    <DashboardLayout>
      <Outlet />
    </DashboardLayout>
  ),
})
```

> **Details**: [nested-routes.md](references/nested-routes.md)
> **Template**: [templates/dashboard-layout.md](references/templates/dashboard-layout.md)

---

## Best Practices

### Do's

| Pattern | Reference |
|---------|-----------|
| Use Route API (`Route.useParams()`) | [hooks.md](references/hooks.md) |
| Validate search params with Zod | [search-params.md](references/search-params.md) |
| Use `ensureQueryData` in loaders | [tanstack-query.md](references/tanstack-query.md) |
| Preload on intent for links | [preloading.md](references/preloading.md) |
| Separate interfaces in `interfaces/` | [solid-react skill](../solid-react/SKILL.md) |

### Don'ts

| Anti-pattern | Why | Alternative |
|--------------|-----|-------------|
| `useLoaderData()` without `from` | Not type-safe | `Route.useLoaderData()` |
| `useEffect` for fetch | Not optimal | Use loaders |
| Mutate search params | Immutability | `navigate({ search: {...} })` |
| Skip error boundaries | Degraded UX | Add `errorComponent` |
| Interfaces in components | Coupling | `interfaces/` folder |

---

## Migration from React Router

See [installation.md](references/installation.md) for complete migration guide.

| React Router | TanStack Router |
|--------------|-----------------|
| `useParams()` | `Route.useParams()` |
| `useSearchParams()` | `Route.useSearch()` |
| `useLoaderData()` | `Route.useLoaderData()` |
| `loader` function | `loader` option |
| `action` function | TanStack Query mutations |

---

## Version History

- **v1.x** - Frequent releases (incremental versioning)
- Key milestones: Head/meta tags, Search params middlewares, Zod adapter
