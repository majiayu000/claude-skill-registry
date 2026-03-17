---
name: web-server-state-react-query
description: REST APIs, React Query, data fetching
---

# API Client Architecture

> **Quick Guide:** Using OpenAPI? Need type safety? Integrating with React Query? Use hey-api for automatic client generation with type-safe React Query hooks.

---

<critical_requirements>

## ⚠️ CRITICAL: Before Using This Skill

**(You MUST use generated query options from @hey-api - NEVER write custom React Query hooks)**

**(You MUST regenerate client code (`bun run build` in packages/api) when OpenAPI schema changes)**

**(You MUST use named constants for ALL timeout/retry values - NO magic numbers)**

**(You MUST configure API client base URL via environment variables)**

**(You MUST use named exports only - NO default exports in libraries)**

</critical_requirements>

---

**Auto-detection:** OpenAPI schema, hey-api code generation, generated React Query hooks, API client configuration

**When to use:**

- Setting up hey-api to generate client from OpenAPI specs
- Using generated React Query query options (getFeaturesOptions pattern)
- Troubleshooting API type generation or regeneration

**When NOT to use:**

- No OpenAPI spec available (consider writing one or using tRPC)
- GraphQL API (use Apollo or urql instead)
- Real-time WebSocket APIs (use socket.io or similar)
- Simple REST APIs where manual fetch calls suffice

**Key patterns covered:**

- OpenAPI-first development with hey-api (@hey-api/openapi-ts)
- Generated React Query hooks and query options (never custom hooks)
- Type safety from generated types (never manual type definitions)

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

OpenAPI-first development ensures a single source of truth for your API contract. The hey-api code generator (@hey-api/openapi-ts) transforms your OpenAPI schema into fully typed client code, React Query hooks, and query options—eliminating manual type definitions and reducing bugs.

This approach prioritizes:

- **Single source of truth**: OpenAPI schema drives types, client code, and mocks
- **Zero manual typing**: Generated code eliminates type drift
- **Consistent patterns**: All API calls use the same generated query options
- **Centralized configuration**: One place to configure client behavior

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: OpenAPI Schema Definition and Code Generation

Define your API contract in OpenAPI format, then use hey-api to generate TypeScript client code, types, and React Query hooks.

#### Constants

```typescript
// packages/api/openapi-ts.config.ts
const OUTPUT_PATH = "./src/apiClient";
```

#### OpenAPI Schema

```yaml
# packages/api/openapi.yaml
openapi: 3.1.0
info:
  title: Side project features API
  description: API for managing side project features
  version: 0.0.1

servers:
  - url: /api/v1
    description: API routes

components:
  schemas:
    Feature:
      type: object
      properties:
        id:
          type: string
          description: Auto-generated ID for the feature
        name:
          type: string
          description: Name of the feature
        description:
          type: string
          description: Description of the feature
        status:
          type: string
          description: Status 'not started' | 'in progress' | 'done'
      required: [id, name, description, status]

paths:
  /features:
    get:
      summary: Get features
      responses:
        "200":
          description: Features
          content:
            application/json:
              schema:
                type: object
                properties:
                  features:
                    type: array
                    items:
                      $ref: "#/components/schemas/Feature"
```

#### Configuration

```typescript
// packages/api/openapi-ts.config.ts
import { defaultPlugins, defineConfig } from "@hey-api/openapi-ts";

const OUTPUT_PATH = "./src/apiClient";

export default defineConfig({
  input: "./openapi.yaml",
  output: {
    format: "prettier",
    lint: "eslint",
    path: OUTPUT_PATH,
  },
  // Generate both fetch client AND React Query hooks
  plugins: [
    ...defaultPlugins,
    "@hey-api/client-fetch",
    "@tanstack/react-query",
  ],
});
```

#### Package Configuration

```json
// packages/api/package.json
{
  "name": "@repo/api",
  "scripts": {
    "build": "openapi-ts"
  },
  "exports": {
    "./types": "./src/apiClient/types.gen.ts",
    "./client": "./src/apiClient/services.gen.ts",
    "./reactQueries": "./src/apiClient/@tanstack/react-query.gen.ts"
  },
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.59.2",
    "@hey-api/client-fetch": "^0.3.3",
    "@tanstack/react-query": "^5.62.11"
  }
}
```

**Why good:** Single source of truth in OpenAPI eliminates type drift, automatic code generation removes manual typing errors, generated React Query hooks enforce consistent patterns, named exports enable tree-shaking

**When to use:** Always when backend provides OpenAPI specification.

---

### Pattern 2: Client Configuration with Environment Variables

Configure the API client base URL and global settings before React Query initialization using environment variables and named constants.

#### Constants

```typescript
// apps/client-next/lib/query-provider.tsx
const FIVE_MINUTES_MS = 5 * 60 * 1000;
const DEFAULT_RETRY_ATTEMPTS = 3;
```

#### Environment Variables

```bash
# apps/client-next/.env
NEXT_PUBLIC_API_URL=http://localhost:3000/api/v1

# apps/client-next/.env.production
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api/v1
```

#### Basic Setup

```typescript
// apps/client-next/lib/query-provider.tsx
"use client";

import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { client } from "@repo/api/client";

const FIVE_MINUTES_MS = 5 * 60 * 1000;

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: FIVE_MINUTES_MS,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  // Configure API client ONCE on initialization
  client.setConfig({
    baseUrl: process.env.NEXT_PUBLIC_API_URL || "",
  });

  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}

// Named export (project convention)
export { QueryProvider };
```

**Why good:** Environment variables enable different URLs per environment without code changes, named constants make timeouts self-documenting, single configuration point prevents scattered setConfig calls, client configures before any queries run

---

### Pattern 3: Using Generated Query Options

Use generated query options directly—never write custom React Query hooks.

#### Generated Query Options (Auto-Generated)

```typescript
// packages/api/src/apiClient/@tanstack/react-query.gen.ts (AUTO-GENERATED)
import type { QueryObserverOptions } from "@tanstack/react-query";
import { getFeaturesQueryKey, getFeatures } from "./services.gen";
import type { GetFeaturesResponse } from "./types.gen";

export const getFeaturesOptions =
  (): QueryObserverOptions<GetFeaturesResponse> => ({
    queryKey: getFeaturesQueryKey(),
    queryFn: () => getFeatures(),
  });

// Query key is also generated
export function getFeaturesQueryKey() {
  return ["api", "v1", "features"] as const;
}
```

#### Usage in Components

```typescript
// apps/client-next/app/features.tsx
import { useQuery } from "@tanstack/react-query";
import { getFeaturesOptions } from "@repo/api/reactQueries";

export function FeaturesPage() {
  // Use generated query options - fully typed!
  const { data, isPending, error } = useQuery(getFeaturesOptions());

  if (isPending) return <Skeleton />;
  if (error) return <Error message={error.message} />;

  return (
    <ul>
      {data?.features?.map((feature) => (
        <li key={feature.id}>{feature.name}</li>
      ))}
    </ul>
  );
}

// Named export (project convention)
export { FeaturesPage };
```

#### Customizing Generated Options

```typescript
import { useQuery } from "@tanstack/react-query";
import { getFeaturesOptions } from "@repo/api/reactQueries";

const TEN_MINUTES_MS = 10 * 60 * 1000;
const THIRTY_SECONDS_MS = 30 * 1000;

export function Features() {
  const someCondition = true; // Your condition

  const { data } = useQuery({
    ...getFeaturesOptions(),
    // Override defaults
    staleTime: TEN_MINUTES_MS,
    refetchInterval: THIRTY_SECONDS_MS,
    enabled: someCondition, // Conditional fetching
  });

  return <div>{/* ... */}</div>;
}

// Named export
export { Features };
```

**Why good:** Zero boilerplate eliminates custom hook bugs, type-safe options prevent runtime errors, consistent patterns across all API calls, query keys automatically namespaced, easy to customize by spreading, named constants make policies visible

</patterns>

---

<critical_reminders>

## ⚠️ CRITICAL REMINDERS

**(You MUST use generated query options from @hey-api - NEVER write custom React Query hooks)**

**(You MUST regenerate client code (`bun run build` in packages/api) when OpenAPI schema changes)**

**(You MUST use named constants for ALL timeout/retry values - NO magic numbers)**

**(You MUST configure API client base URL via environment variables)**

**(You MUST use named exports only - NO default exports in libraries)**

**Failure to follow these rules will cause type drift, bundle bloat, and production bugs.**

</critical_reminders>
