---
name: web-data-fetching-graphql-urql
description: URQL GraphQL client patterns - useQuery, useMutation, exchange architecture, caching strategies, subscriptions
---

# URQL GraphQL Client Patterns

> **Quick Guide:** Use URQL for GraphQL APIs when you need a lightweight, customizable client with exchange-based architecture. Start minimal with document caching, add normalized caching via Graphcache when needed. Bundle size is ~12KB gzipped (core), ~20KB with Graphcache. **Current version: @urql/core v6.0.1 (urql v5.0.1)**

---

<critical_requirements>

## CRITICAL: Before Using This Skill

**(You MUST configure exchange order correctly - synchronous exchanges (cacheExchange) before asynchronous (fetchExchange))**

**(You MUST include `__typename` in optimistic responses for Graphcache cache normalization)**

**(You MUST set `preferGetMethod: false` if your GraphQL server does NOT support GET requests - v6+ defaults to GET for queries under 2048 characters)**

**(You MUST use named constants for ALL timeout, retry, and polling values - NO magic numbers)**

**(You MUST use named exports only - NO default exports)**

</critical_requirements>

---

**Auto-detection:** URQL, urql, useQuery, useMutation, useSubscription, cacheExchange, fetchExchange, Graphcache, exchanges, gql, Client

**When to use:**

- Fetching data from GraphQL APIs
- Applications needing lightweight GraphQL client (~12KB vs Apollo's ~30KB)
- Projects requiring customizable middleware via exchanges
- Progressive enhancement: start simple, add complexity as needed
- Real-time updates with GraphQL subscriptions

**When NOT to use:**

- REST APIs (use your data fetching solution instead)
- When team already has Apollo Client expertise and no bundle concerns
- Simple APIs without caching needs (consider fetch directly)

**Key patterns covered:**

- Client setup with exchange pipeline
- useQuery for queries with loading, error, and data states
- useMutation with optimistic updates via Graphcache
- useSubscription for real-time WebSocket data
- Exchange architecture and custom exchanges
- Document caching vs normalized caching (Graphcache)
- Request policies and caching strategies
- Authentication with authExchange

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md)
- For exchange patterns, see [examples/exchanges.md](examples/exchanges.md)
- For real-time subscriptions, see [examples/subscriptions.md](examples/subscriptions.md)
- For v6 features and breaking changes, see [examples/v6-features.md](examples/v6-features.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

URQL follows the principle of **progressive enhancement**. The core package provides document caching and basic fetching, while advanced features like normalized caching, authentication, and offline support are added through exchanges.

**Core Principles:**

1. **Minimal by Default**: Start with ~10KB, add features as needed
2. **Exchange-Based Architecture**: Middleware-style plugins for extensibility
3. **Stream-Based Operations**: All operations are Observable streams via Wonka
4. **Document Caching Default**: Simple query+variables hash caching, opt-in normalized cache

**URQL's Data Flow:**

1. Component requests data via useQuery/useMutation
2. Operation flows through exchange pipeline (cache → auth → retry → fetch)
3. Each exchange can inspect, modify, or short-circuit the operation
4. Results flow back through exchanges in reverse
5. Multiple results can emit over time (cache update triggers new emission)

**Three Architectural Layers:**

1. **Bindings** - Framework integrations (React, Vue, Svelte, Solid)
2. **Client** - Core engine managing operations and coordinating exchanges
3. **Exchanges** - Plugins providing functionality (caching, fetching, auth)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup and Configuration

Configure URQL Client with appropriate exchanges in the correct order.

#### Constants

```typescript
const GRAPHQL_ENDPOINT =
  process.env.NEXT_PUBLIC_GRAPHQL_URL || "http://localhost:4000/graphql";
```

#### Implementation

```typescript
// lib/urql-client.ts
import { Client, cacheExchange, fetchExchange } from "urql";

const GRAPHQL_ENDPOINT = process.env.NEXT_PUBLIC_GRAPHQL_URL || "";

const client = new Client({
  url: GRAPHQL_ENDPOINT,
  exchanges: [cacheExchange, fetchExchange],
});

export { client };
```

**Why good:** Environment variable for endpoint flexibility, default exchange order is correct (sync before async), named export enables tree-shaking

---

### Pattern 2: Provider Setup

Wrap your application with URQL Provider to enable hooks.

#### Implementation

```typescript
// app/providers.tsx
import { Provider } from "urql";
import { client } from "@/lib/urql-client";
import type { ReactNode } from "react";

interface ProvidersProps {
  children: ReactNode;
}

function Providers({ children }: ProvidersProps) {
  return <Provider value={client}>{children}</Provider>;
}

export { Providers };
```

**Why good:** Typed props interface, named export, clean separation of client creation from provider setup

---

### Pattern 3: useQuery for Data Fetching

Use useQuery to fetch data declaratively with loading, error, and data states.

#### Implementation

```typescript
// components/user-list.tsx
import { useQuery, gql } from "urql";

const USERS_QUERY = gql`
  query GetUsers($limit: Int!, $offset: Int) {
    users(limit: $limit, offset: $offset) {
      id
      name
      email
      avatar
    }
  }
`;

const DEFAULT_PAGE_SIZE = 20;
const INITIAL_OFFSET = 0;

interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
}

interface UsersData {
  users: User[];
}

interface UsersVariables {
  limit: number;
  offset?: number;
}

function UserList() {
  const [result, reexecuteQuery] = useQuery<UsersData, UsersVariables>({
    query: USERS_QUERY,
    variables: {
      limit: DEFAULT_PAGE_SIZE,
      offset: INITIAL_OFFSET,
    },
    requestPolicy: "cache-and-network",
  });

  const { data, fetching, error, stale } = result;

  if (fetching && !data) {
    return <Skeleton />;
  }

  if (error) {
    return (
      <Error
        message={error.message}
        onRetry={() => reexecuteQuery({ requestPolicy: "network-only" })}
      />
    );
  }

  if (!data?.users?.length) {
    return <EmptyState message="No users found" />;
  }

  return (
    <div>
      {stale && <span className="stale-indicator">Updating...</span>}
      <ul>
        {data.users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}

export { UserList };
```

**Why good:** TypeScript generics provide type safety, named constants for pagination, reexecuteQuery enables user-triggered refresh, stale indicator shows background refresh, checks `fetching && !data` for initial load vs background refresh

---

### Pattern 4: useMutation for Data Modifications

Use useMutation for creating, updating, or deleting data.

#### Implementation

```typescript
// components/create-todo-form.tsx
import { useState } from "react";
import type { FormEvent } from "react";
import { useMutation, gql } from "urql";

const CREATE_TODO = gql`
  mutation CreateTodo($input: CreateTodoInput!) {
    createTodo(input: $input) {
      id
      title
      completed
      createdAt
    }
  }
`;

interface CreateTodoInput {
  title: string;
  description?: string;
}

interface CreateTodoData {
  createTodo: {
    id: string;
    title: string;
    completed: boolean;
    createdAt: string;
  };
}

function CreateTodoForm() {
  const [title, setTitle] = useState("");
  const [result, executeMutation] = useMutation<CreateTodoData>(CREATE_TODO);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    const input: CreateTodoInput = { title: title.trim() };
    const response = await executeMutation({ input });

    if (response.error) {
      console.error("Failed to create todo:", response.error);
      return;
    }

    setTitle("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter todo title"
        disabled={result.fetching}
      />
      <button type="submit" disabled={result.fetching || !title.trim()}>
        {result.fetching ? "Creating..." : "Create Todo"}
      </button>
    </form>
  );
}

export { CreateTodoForm };
```

**Why good:** Proper form event handling, disabled state during mutation, error handling with user feedback, input trimming prevents empty submissions

---

### Pattern 5: Conditional and Dependent Queries

Use the `pause` option to control when queries execute.

#### Implementation

```typescript
import { useQuery } from "urql";

interface UserProfileProps {
  userId: string | null;
}

function UserProfile({ userId }: UserProfileProps) {
  const [result] = useQuery({
    query: USER_QUERY,
    variables: { id: userId },
    // Pause query when userId is null or empty
    pause: !userId,
  });

  const { data, fetching, error } = result;

  if (!userId) {
    return <div>Select a user to view profile</div>;
  }

  if (fetching) return <Skeleton />;
  if (error) return <Error message={error.message} />;
  if (!data?.user) return <NotFound />;

  return <ProfileCard user={data.user} />;
}

export { UserProfile };
```

**Why good:** Query pauses when userId is falsy, prevents unnecessary network requests, handles null state gracefully

---

### Pattern 6: Request Policies

Control caching behavior with request policies.

#### Request Policy Options

| Policy              | Behavior                                         | Use Case               |
| ------------------- | ------------------------------------------------ | ---------------------- |
| `cache-first`       | Return cached if available, else fetch (default) | Most queries           |
| `cache-only`        | Only return cached, never fetch                  | Offline-first          |
| `network-only`      | Always fetch, skip cache read                    | Critical fresh data    |
| `cache-and-network` | Return cached immediately, then fetch and update | Stale-while-revalidate |

#### Implementation

```typescript
// Cache-first (default) - uses cache if available
const [result] = useQuery({
  query: USERS_QUERY,
  requestPolicy: "cache-first",
});

// Cache-and-network - best UX for most cases
const [result] = useQuery({
  query: USERS_QUERY,
  requestPolicy: "cache-and-network",
});

// Force refetch
const handleRefresh = () => {
  reexecuteQuery({ requestPolicy: "network-only" });
};
```

**Why good:** Explicit policy selection based on use case, cache-and-network provides instant UI with background refresh

</patterns>

---

<integration>

## Integration Guide

**Styling Integration:**
Components are styling-agnostic. Apply styles via className prop or your styling solution.

**State Integration:**
Server state is managed by URQL's cache. Client state is a separate concern - use your client state management approach.

**Testing Integration:**
Mock GraphQL operations at the network level using your mocking solution. URQL provides test utilities for creating mock clients.

**Domain boundaries:**

- **Server-side GraphQL schema**: Defer to backend skills for schema design, resolvers, and server setup
- **REST APIs**: Use your REST data fetching solution instead - URQL is for GraphQL only
- **Complex client state**: Use your client state management solution for non-server state

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST configure exchange order correctly - synchronous exchanges (cacheExchange) before asynchronous (fetchExchange))**

**(You MUST include `__typename` in optimistic responses for Graphcache cache normalization)**

**(You MUST set `preferGetMethod: false` if your GraphQL server does NOT support GET requests - v6+ defaults to GET for queries under 2048 characters)**

**(You MUST use named constants for ALL timeout, retry, and polling values - NO magic numbers)**

**(You MUST use named exports only - NO default exports)**

**Failure to follow these rules will cause cache corruption, stale data, and production bugs.**

</critical_reminders>
