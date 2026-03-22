---
name: data-fetching
description: Data fetching patterns for server/client components using fetch API, TanStack Query, useSuspenseQuery, apiRouteWrapper, and apiRequestWrapper. Use when implementing data loading, API calls, server functions, queries, mutations, API routes, or when the user mentions TanStack Query, useSuspenseQuery, apiRouteWrapper, apiRequestWrapper, tmdb-server-functions, or data fetching.
---

# Data Fetching Architecture

## Overview

This project uses a structured data fetching pattern that differs between server and client components.

## Core Principles

1. **Server components** call server functions directly
2. **Client components** use TanStack Query to fetch from API routes
3. **API routes** wrap server functions using `apiRouteWrapper`
4. **Mutations** from client components call server functions directly
5. **TMDB API** uses auto-generated server functions from `tmdb-server-functions.ts`

## Server Components

Server components can directly `await` server functions.

```tsx
import { discoverMovies } from "@/utils/tmdb-server-functions";

function serverFunction() {
  return fetch(URL, headers);
}

function ServerComponent() {
  const movies = await discoverMovies({
    page: 1,
    with_genres: "28",
  });

  const myResults = await serverFunction();

  return <div>...</div>;
}
```

Use `await` directly in server components. Call TMDB server functions from `@/utils/tmdb-server-functions`.

## Client Components + API Routes

Client components use TanStack Query to call API routes, which wrap server functions.

### Step 1: Create API Route

API routes use `apiRouteWrapper` to wrap server functions:

```ts
// src/app/api/tmdb/discover-movies/route.ts
import { apiRouteWrapper } from "@/utils/api-route-wrapper";
import { discoverMovies } from "@/utils/tmdb-server-functions";

export const GET = apiRouteWrapper(discoverMovies);
```

For custom server functions:

```ts
// src/app/api/some-api-route/route.ts
import { apiRouteWrapper } from "@/utils/api-route-wrapper";
import { myServerFunction } from "@/some-server-function";

export const GET = apiRouteWrapper(async (params) => {
  return myServerFunction(params);
});
```

### Step 2: Call from Client Component

Use TanStack Query with `apiRequestWrapper`:

```tsx
"use client";
import { useSuspenseQuery } from "@tanstack/react-query";
import { apiRequestWrapper } from "@/utils/api-request-wrapper";

function ClientComponent() {
  const { data: movies } = useSuspenseQuery({
    queryKey: [{ scope: "movies", page: 1, with_genres: "28" }],
    queryFn: () =>
      apiRequestWrapper("/api/tmdb/movie-list", {
        page: 1,
        with_genres: "28",
      }),
  });

  const { data: results } = useSuspenseQuery({
    queryKey: [{ scope: "someApiRoute" }],
    queryFn: () =>
      apiRequestWrapper("/api/some-api-route", {
        foo: "bar",
      }),
  });

  return <div>...</div>;
}
```

## Mutations from Client Components

For mutations, client components call server functions directly (no API route needed).

```tsx
"use client";
import { useMutation } from "@tanstack/react-query";
import { updateMovie } from "@/server-functions/movies";

function ClientComponent() {
  const mutation = useMutation({
    mutationFn: updateMovie,
  });

  const handleUpdate = () => {
    mutation.mutate({ id: 1, title: "New Title" });
  };

  return <button onClick={handleUpdate}>Update</button>;
}
```

## TMDB API Integration

TMDB server functions are auto-generated from `src/_generated/tmdb-server-functions.ts`.

**Important**: These are auto-generated - **DO NOT edit manually**. Use `pnpm codegen:tmdb` to regenerate.

```tsx
// Import TMDB functions
import {
  discoverMovies,
  getMovieDetails,
  searchMovies,
} from "@/utils/tmdb-server-functions";

// Server component usage
async function MovieList() {
  const movies = await discoverMovies({
    page: 1,
    with_genres: "28",
  });

  return <div>...</div>;
}

// API route for client components
// src/app/api/tmdb/discover-movies/route.ts
export const GET = apiRouteWrapper(discoverMovies);
```

## Pattern Summary

### Server Component Data Flow

```
Server Component → Server Function → External API/Database
```

### Client Component Data Flow (Queries)

```
Client Component → TanStack Query → API Route → Server Function → External API/Database
```

### Client Component Data Flow (Mutations)

```
Client Component → TanStack Query Mutation → Server Function → External API/Database
```

## Best Practices

1. **Server components**: Call server functions directly with `await`
2. **Client queries**: Use TanStack Query + API routes
3. **Client mutations**: Call server functions directly
4. **TMDB**: Use auto-generated functions, never edit manually
5. **API routes**: Use `apiRouteWrapper`
6. **Client fetching**: Use `apiRequestWrapper`

## Common Mistakes

❌ Calling API routes from server components (use server functions directly)
❌ Using `fetch` directly in client components (use TanStack Query)
❌ Editing `tmdb-server-functions.ts` manually (regenerate with `pnpm codegen:tmdb`)
❌ Creating API routes for mutations (call server functions directly)
