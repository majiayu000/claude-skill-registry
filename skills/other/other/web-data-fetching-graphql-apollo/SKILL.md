---
name: web-data-fetching-graphql-apollo
description: Apollo Client GraphQL patterns - useQuery, useMutation, cache management, optimistic updates, subscriptions
---

# Apollo Client GraphQL Patterns

> **Quick Guide:** Use Apollo Client for GraphQL APIs. Provides automatic caching, optimistic updates, and real-time subscriptions. Use GraphQL Codegen for type safety. **v3.9+** adds Suspense hooks (`useSuspenseQuery`, `useLoadableQuery`); **v4.0** moves React imports to `@apollo/client/react`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

**(You MUST use GraphQL Codegen for type generation - NEVER write manual TypeScript types for GraphQL)**

**(You MUST include `__typename` and `id` in all optimistic responses for cache normalization)**

**(You MUST configure type policies with appropriate `keyFields` for cache identification)**

**(You MUST use named constants for ALL timeout, retry, and polling values - NO magic numbers)**

**(You MUST use named exports only - NO default exports)**

</critical_requirements>

---

**Auto-detection:** Apollo Client, useQuery, useMutation, useSubscription, useSuspenseQuery, useLoadableQuery, useBackgroundQuery, useFragment, ApolloClient, InMemoryCache, gql, GraphQL, optimistic updates, cache policies, createQueryPreloader

**When to use:**

- Fetching data from GraphQL APIs
- Real-time updates with GraphQL subscriptions
- Complex cache management with normalized data
- Optimistic UI updates for mutations
- Applications already using GraphQL server

**When NOT to use:**

- REST APIs (use your data fetching solution instead)
- Simple APIs without caching needs (consider fetch directly)
- When GraphQL Codegen cannot be integrated

**Key patterns covered:**

- Client setup with InMemoryCache and type policies
- useQuery for queries with loading, error, and data states
- useMutation with optimistic updates and cache modification
- useSubscription for real-time WebSocket data
- Pagination with fetchMore and relayStylePagination
- Fragment colocation with useFragment
- GraphQL Codegen integration for type safety
- Local state with reactive variables
- **v3.9+**: useSuspenseQuery, useLoadableQuery, useBackgroundQuery for Suspense
- **v3.9+**: createQueryPreloader for preloading outside React
- **v3.10+**: Schema-based testing with createTestSchema

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md)
- For v3.9+ Suspense patterns, see [examples/suspense.md](examples/suspense.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Apollo Client is a comprehensive state management library for JavaScript that enables you to manage both local and remote data with GraphQL. It provides intelligent caching that normalizes your data, reducing redundant network requests and keeping your UI consistent.

**Core Principles:**

1. **Normalized Cache**: Data is stored once by type and ID, referenced everywhere
2. **Declarative Data Fetching**: Components declare what data they need, Apollo handles the how
3. **Optimistic UI**: Show expected results immediately, rollback on server error
4. **Type Safety**: Use GraphQL Codegen to generate TypeScript types from your schema

**Apollo Client's Data Flow:**

1. Component requests data via useQuery/useMutation
2. Apollo checks InMemoryCache first
3. If cache miss or stale, fetches from network
4. Response is normalized and stored in cache
5. All components watching that data re-render

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup and Configuration

Configure ApolloClient with InMemoryCache and appropriate type policies for cache normalization.

#### Constants

```typescript
const GRAPHQL_ENDPOINT =
  process.env.NEXT_PUBLIC_GRAPHQL_URL || "http://localhost:4000/graphql";
const DEFAULT_POLL_INTERVAL_MS = 30 * 1000;
```

#### Implementation

```typescript
// lib/apollo-client.ts
import { ApolloClient, InMemoryCache, HttpLink, from } from "@apollo/client";
import { onError } from "@apollo/client/link/error";

const GRAPHQL_ENDPOINT = process.env.NEXT_PUBLIC_GRAPHQL_URL || "";

// Error handling link
const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path }) => {
      console.error(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
      );
    });
  }
  if (networkError) {
    console.error(`[Network error]: ${networkError}`);
  }
});

// HTTP link
const httpLink = new HttpLink({
  uri: GRAPHQL_ENDPOINT,
  credentials: "include",
});

// Cache with type policies
const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        // Merge paginated results
        users: {
          keyArgs: ["filter"],
          merge(existing = [], incoming) {
            return [...existing, ...incoming];
          },
        },
      },
    },
    User: {
      // Identify users by their ID
      keyFields: ["id"],
    },
    Product: {
      // Identify products by SKU (not default id)
      keyFields: ["sku"],
    },
  },
});

const apolloClient = new ApolloClient({
  link: from([errorLink, httpLink]),
  cache,
  defaultOptions: {
    watchQuery: {
      fetchPolicy: "cache-and-network",
      errorPolicy: "all",
    },
    query: {
      fetchPolicy: "cache-first",
      errorPolicy: "all",
    },
    mutate: {
      errorPolicy: "all",
    },
  },
});

export { apolloClient };
```

**Why good:** Environment variables enable different GraphQL endpoints per environment, type policies ensure proper cache normalization, error link provides centralized error handling, named exports enable tree-shaking

---

### Pattern 2: useQuery for Data Fetching

Use useQuery to fetch data declaratively with loading, error, and data states.

#### Implementation

```typescript
// components/user-list.tsx
import { useQuery, gql } from "@apollo/client";
import type { GetUsersQuery, GetUsersQueryVariables } from "@/generated/graphql";

const GET_USERS = gql`
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

function UserList() {
  const { data, loading, error, refetch } = useQuery<GetUsersQuery, GetUsersQueryVariables>(
    GET_USERS,
    {
      variables: {
        limit: DEFAULT_PAGE_SIZE,
        offset: INITIAL_OFFSET,
      },
      // Control fetch behavior
      fetchPolicy: "cache-and-network",
      // Notify on network status changes
      notifyOnNetworkStatusChange: true,
    }
  );

  if (loading && !data) {
    return <Skeleton />;
  }

  if (error) {
    return <Error message={error.message} onRetry={() => refetch()} />;
  }

  if (!data?.users?.length) {
    return <EmptyState message="No users found" />;
  }

  return (
    <ul>
      {data.users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

export { UserList };
```

**Why good:** TypeScript generics provide full type safety, named constants make pagination configurable, refetch enables user-triggered refresh, cache-and-network shows cached data while fetching fresh

---

### Pattern 3: useMutation with Optimistic Updates

Use useMutation for data modifications with optimistic UI for instant feedback.

#### Implementation

```typescript
// components/add-comment.tsx
import { useState } from "react";
import type { FormEvent } from "react";
import { useMutation, gql } from "@apollo/client";
import type { AddCommentMutation, AddCommentMutationVariables } from "@/generated/graphql";

const ADD_COMMENT = gql`
  mutation AddComment($postId: ID!, $content: String!) {
    addComment(postId: $postId, content: $content) {
      id
      content
      author {
        id
        name
      }
      createdAt
    }
  }
`;

const GET_POST_COMMENTS = gql`
  query GetPostComments($postId: ID!) {
    post(id: $postId) {
      id
      comments {
        id
        content
        author {
          id
          name
        }
        createdAt
      }
    }
  }
`;

interface AddCommentFormProps {
  postId: string;
  currentUser: { id: string; name: string };
}

function AddCommentForm({ postId, currentUser }: AddCommentFormProps) {
  const [content, setContent] = useState("");

  const [addComment, { loading }] = useMutation<AddCommentMutation, AddCommentMutationVariables>(
    ADD_COMMENT,
    {
      // Optimistic response for instant UI update
      optimisticResponse: {
        addComment: {
          __typename: "Comment",
          id: `temp-${Date.now()}`,
          content,
          author: {
            __typename: "User",
            id: currentUser.id,
            name: currentUser.name,
          },
          createdAt: new Date().toISOString(),
        },
      },
      // Update cache after mutation
      update(cache, { data }) {
        if (!data?.addComment) return;

        // Read existing comments
        const existing = cache.readQuery({
          query: GET_POST_COMMENTS,
          variables: { postId },
        });

        // Write new comment to cache
        cache.writeQuery({
          query: GET_POST_COMMENTS,
          variables: { postId },
          data: {
            post: {
              ...existing?.post,
              comments: [...(existing?.post?.comments || []), data.addComment],
            },
          },
        });
      },
      onError(error) {
        console.error("Failed to add comment:", error);
        toast.error("Failed to add comment. Please try again.");
      },
    }
  );

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;

    await addComment({ variables: { postId, content } });
    setContent("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Write a comment..."
        disabled={loading}
      />
      <button type="submit" disabled={loading || !content.trim()}>
        {loading ? "Posting..." : "Post Comment"}
      </button>
    </form>
  );
}

export { AddCommentForm };
```

**Why good:** Optimistic response includes `__typename` and `id` for proper cache normalization, update callback manually updates related queries, onError provides user feedback on failure, UI remains responsive during network request

---

### Pattern 4: Cache Type Policies

Configure type policies for proper cache normalization and custom field behaviors.

#### Implementation

```typescript
// lib/apollo-cache.ts
import { InMemoryCache, Reference, makeVar } from "@apollo/client";
import { relayStylePagination } from "@apollo/client/utilities";

// Reactive variable for local state
const isLoggedInVar = makeVar<boolean>(false);
const cartItemsVar = makeVar<string[]>([]);

const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        // Relay-style pagination for connections
        usersConnection: relayStylePagination(["filter", "sortBy"]),

        // Custom read for local state
        isLoggedIn: {
          read() {
            return isLoggedInVar();
          },
        },

        // Singleton pattern (no keyArgs needed)
        currentUser: {
          merge(existing, incoming) {
            return incoming;
          },
        },
      },
    },

    User: {
      // Default cache key is id, this is explicit
      keyFields: ["id"],
      fields: {
        // Computed field
        fullName: {
          read(_, { readField }) {
            const firstName = readField<string>("firstName");
            const lastName = readField<string>("lastName");
            return `${firstName} ${lastName}`;
          },
        },
      },
    },

    Product: {
      // Use SKU instead of id for cache key
      keyFields: ["sku"],
    },

    CartItem: {
      // Don't normalize (embed in parent)
      keyFields: false,
    },

    // Interface-level policy (applies to all implementing types)
    Node: {
      keyFields: ["id"],
    },
  },
});

export { cache, isLoggedInVar, cartItemsVar };
```

**Why good:** relayStylePagination handles cursor-based pagination automatically, keyFields configure proper cache identification, read functions enable computed and local state fields, keyFields: false prevents unnecessary normalization for embedded types

---

### Pattern 5: Pagination with fetchMore

Implement cursor-based pagination using fetchMore and type policies.

#### Implementation

```typescript
// components/paginated-users.tsx
import { useQuery, gql } from "@apollo/client";

const GET_USERS_CONNECTION = gql`
  query GetUsersConnection($first: Int!, $after: String) {
    usersConnection(first: $first, after: $after) {
      edges {
        cursor
        node {
          id
          name
          email
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
`;

const PAGE_SIZE = 20;

function PaginatedUserList() {
  const { data, loading, error, fetchMore } = useQuery(GET_USERS_CONNECTION, {
    variables: { first: PAGE_SIZE },
    notifyOnNetworkStatusChange: true,
  });

  const loadMore = () => {
    if (!data?.usersConnection?.pageInfo?.hasNextPage) return;

    fetchMore({
      variables: {
        after: data.usersConnection.pageInfo.endCursor,
      },
      // Type policy handles merging automatically with relayStylePagination
    });
  };

  if (loading && !data) {
    return <Skeleton />;
  }

  if (error) {
    return <Error message={error.message} />;
  }

  const users = data?.usersConnection?.edges?.map((edge) => edge.node) || [];
  const hasNextPage = data?.usersConnection?.pageInfo?.hasNextPage || false;

  return (
    <div>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
      {hasNextPage && (
        <button onClick={loadMore} disabled={loading}>
          {loading ? "Loading..." : "Load More"}
        </button>
      )}
    </div>
  );
}

export { PaginatedUserList };
```

**Why good:** fetchMore appends new data to existing cache, relayStylePagination type policy handles merge automatically, hasNextPage prevents unnecessary requests, loading state during fetch prevents double-clicks

---

### Pattern 6: Fragment Colocation

Colocate data requirements with components using fragments.

#### Implementation

```typescript
// components/user-card.tsx
import { gql } from "@apollo/client";
import type { UserCardFragment } from "@/generated/graphql";

// Colocated fragment - defines component's data needs
const USER_CARD_FRAGMENT = gql`
  fragment UserCard on User {
    id
    name
    email
    avatar
    role
  }
`;

interface UserCardProps {
  user: UserCardFragment;
}

function UserCard({ user }: UserCardProps) {
  return (
    <div className="user-card">
      <img src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      <span>{user.role}</span>
    </div>
  );
}

// Attach fragment to component for parent queries
UserCard.fragments = {
  user: USER_CARD_FRAGMENT,
};

export { UserCard };
```

```typescript
// components/user-list.tsx
import { useQuery, gql } from "@apollo/client";
import { UserCard } from "./user-card";

// Parent query includes child fragment
const GET_USERS = gql`
  query GetUsers {
    users {
      ...UserCard
    }
  }
  ${UserCard.fragments.user}
`;

function UserListPage() {
  const { data, loading, error } = useQuery(GET_USERS);

  if (loading) return <Skeleton />;
  if (error) return <Error message={error.message} />;

  return (
    <div>
      {data?.users?.map((user) => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}

export { UserListPage };
```

**Why good:** Fragment colocation keeps data requirements close to components, parent queries automatically include child data needs, TypeScript types generated for fragments ensure type safety, component changes don't require updating parent queries

---

### Pattern 7: useSubscription for Real-Time Data

Set up WebSocket subscriptions for real-time updates.

#### Link Configuration

```typescript
// lib/apollo-client.ts
import { ApolloClient, InMemoryCache, HttpLink, split } from "@apollo/client";
import { GraphQLWsLink } from "@apollo/client/link/subscriptions";
import { createClient } from "graphql-ws";
import { getMainDefinition } from "@apollo/client/utilities";

const GRAPHQL_HTTP_URL = process.env.NEXT_PUBLIC_GRAPHQL_URL || "";
const GRAPHQL_WS_URL = process.env.NEXT_PUBLIC_GRAPHQL_WS_URL || "";

const httpLink = new HttpLink({
  uri: GRAPHQL_HTTP_URL,
});

const wsLink = new GraphQLWsLink(
  createClient({
    url: GRAPHQL_WS_URL,
    connectionParams: () => ({
      // Add auth token if needed
      authToken: localStorage.getItem("token"),
    }),
  }),
);

// Split traffic between WebSocket (subscriptions) and HTTP (queries/mutations)
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    );
  },
  wsLink,
  httpLink,
);

const apolloClient = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache(),
});

export { apolloClient };
```

#### Subscription Usage

```typescript
// components/live-comments.tsx
import { useSubscription, gql } from "@apollo/client";

const COMMENT_ADDED = gql`
  subscription OnCommentAdded($postId: ID!) {
    commentAdded(postId: $postId) {
      id
      content
      author {
        id
        name
      }
      createdAt
    }
  }
`;

interface LiveCommentsProps {
  postId: string;
}

function LiveComments({ postId }: LiveCommentsProps) {
  const { data, loading, error } = useSubscription(COMMENT_ADDED, {
    variables: { postId },
    onData({ data }) {
      // Handle new comment (e.g., play sound, show notification)
      console.log("New comment received:", data.data?.commentAdded);
    },
    onError(error) {
      console.error("Subscription error:", error);
    },
  });

  if (error) {
    return <div>Subscription error: {error.message}</div>;
  }

  return (
    <div>
      {loading && <span>Listening for new comments...</span>}
      {data?.commentAdded && (
        <div className="new-comment">
          <strong>{data.commentAdded.author.name}:</strong>
          <p>{data.commentAdded.content}</p>
        </div>
      )}
    </div>
  );
}

export { LiveComments };
```

**Why good:** Link splitting routes subscriptions to WebSocket and queries/mutations to HTTP, connectionParams enables authenticated subscriptions, onData callback handles side effects for new data

---

### Pattern 8: Local State with Reactive Variables

Use reactive variables for client-side state that needs to integrate with Apollo queries.

#### Implementation

```typescript
// lib/local-state.ts
import { makeVar } from "@apollo/client";

// Theme preference
const themeVar = makeVar<"light" | "dark">("light");

// Shopping cart items
const cartItemsVar = makeVar<string[]>([]);

// Auth state
const isAuthenticatedVar = makeVar<boolean>(false);

// Helpers for cart operations
const addToCart = (productId: string) => {
  const current = cartItemsVar();
  if (!current.includes(productId)) {
    cartItemsVar([...current, productId]);
  }
};

const removeFromCart = (productId: string) => {
  const current = cartItemsVar();
  cartItemsVar(current.filter((id) => id !== productId));
};

const clearCart = () => {
  cartItemsVar([]);
};

export {
  themeVar,
  cartItemsVar,
  isAuthenticatedVar,
  addToCart,
  removeFromCart,
  clearCart,
};
```

```typescript
// components/cart-badge.tsx
import { useReactiveVar } from "@apollo/client";
import { cartItemsVar } from "@/lib/local-state";

function CartBadge() {
  // Re-renders automatically when cartItemsVar changes
  const cartItems = useReactiveVar(cartItemsVar);

  return (
    <div className="cart-badge">
      <span>Cart</span>
      {cartItems.length > 0 && (
        <span className="badge">{cartItems.length}</span>
      )}
    </div>
  );
}

export { CartBadge };
```

**Why good:** Reactive variables provide simple local state without Redux complexity, useReactiveVar hook triggers re-renders on changes, can be queried via type policies if needed, helper functions encapsulate state mutations

---

### Pattern 9: Suspense with useSuspenseQuery (v3.9+)

Use `useSuspenseQuery` for Suspense-enabled data fetching that integrates with React's concurrent features.

See [examples/suspense.md](examples/suspense.md) for complete implementation patterns including:

- `useSuspenseQuery` for component-level Suspense
- `useLoadableQuery` for user-interaction triggered loading
- `useBackgroundQuery` + `useReadQuery` for background loading
- `createQueryPreloader` for preloading outside React (router integration)

---

### Pattern 10: useFragment for Data Masking (v3.8+)

Use `useFragment` to read fragment data directly from the cache with automatic updates.

```typescript
// components/user-card.tsx
import { useFragment, gql } from "@apollo/client";
import type { FragmentType, useFragment as useFragmentType } from "@/generated/graphql";

const USER_CARD_FRAGMENT = gql`
  fragment UserCardFragment on User {
    id
    name
    avatar
    email
  }
`;

interface UserCardProps {
  userRef: FragmentType<typeof USER_CARD_FRAGMENT>;
}

function UserCard({ userRef }: UserCardProps) {
  // Reads fragment data from cache, updates automatically
  const { data: user, complete } = useFragment({
    fragment: USER_CARD_FRAGMENT,
    from: userRef,
  });

  if (!complete) {
    return <UserCardSkeleton />;
  }

  return (
    <div className="user-card">
      <img src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}

export { UserCard, USER_CARD_FRAGMENT };
```

**Why good:** useFragment reads directly from cache without additional queries, `complete` flag indicates if all fragment fields are available, automatic re-render when fragment data updates in cache

</patterns>

---

<integration>

## Integration Guide

**Works with:**

- **GraphQL Codegen**: Generate TypeScript types from GraphQL schema and operations for full type safety
- **React**: useQuery, useMutation, useSubscription hooks integrate with React component lifecycle
- **WebSocket libraries (graphql-ws)**: Enable real-time subscriptions via WebSocket transport
- **Error tracking solutions**: onError link integrates with error reporting services

**Domain boundaries:**

- **Server-side GraphQL schema**: Defer to backend skills for schema design, resolvers, and server setup
- **REST APIs**: Use your REST data fetching solution instead - Apollo Client is for GraphQL only
- **Global client state**: Use your client state management solution for complex non-GraphQL state; reactive variables work for simple cases

</integration>

---

<version_migration>

## Apollo Client v4 Migration Notes

**Apollo Client v4** (released September 2025) introduces significant breaking changes. If upgrading from v3, review:

### Import Path Changes (CRITICAL)

```typescript
// v3 imports (DEPRECATED in v4)
import { useQuery, useMutation, ApolloProvider } from "@apollo/client";

// v4 imports (REQUIRED)
import { ApolloClient, InMemoryCache } from "@apollo/client";
import { useQuery, useMutation, ApolloProvider } from "@apollo/client/react";
```

### New `dataState` Property (v4)

```typescript
// v4: Use dataState for TypeScript-safe state checking
const { data, dataState } = useQuery(GET_USER);

// dataState values: "empty" | "partial" | "streaming" | "complete"
if (dataState === "complete") {
  // TypeScript knows data is fully populated
  return <UserCard user={data.user} />;
}
```

### Error Handling Changes (v4)

```typescript
// v3: Single ApolloError class
import { ApolloError } from "@apollo/client";
if (error instanceof ApolloError) { ... }

// v4: Specific error classes
import { CombinedGraphQLErrors, ServerError, ServerParseError } from "@apollo/client";
if (CombinedGraphQLErrors.is(error)) { ... }
if (ServerError.is(error)) { ... }
```

### RxJS Dependency (v4)

```bash
# v4 requires rxjs as peer dependency
npm install rxjs
```

### Client Initialization (v4)

```typescript
// v3: uri option on ApolloClient (DEPRECATED)
const client = new ApolloClient({
  uri: "https://api.example.com/graphql",
  name: "my-app",
  version: "1.0.0",
  cache: new InMemoryCache(),
});

// v4: Explicit HttpLink + clientAwareness (REQUIRED)
import { HttpLink } from "@apollo/client/link/http";
const client = new ApolloClient({
  link: new HttpLink({ uri: "https://api.example.com/graphql" }),
  cache: new InMemoryCache(),
  clientAwareness: {
    name: "my-app",
    version: "1.0.0",
  },
});
```

### notifyOnNetworkStatusChange Default (v4)

```typescript
// v3: Defaults to false
useQuery(GET_USER); // notifyOnNetworkStatusChange: false

// v4: Defaults to true (BREAKING CHANGE)
useQuery(GET_USER); // notifyOnNetworkStatusChange: true

// Explicitly set to false in v4 if you want v3 behavior
useQuery(GET_USER, { notifyOnNetworkStatusChange: false });
```

**Codemod available:** `npx @apollo/client-codemod-migrate-3-to-4`

See [Apollo Client 4 Migration Guide](https://www.apollographql.com/docs/react/migrating/apollo-client-4-migration) for complete details.

</version_migration>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST use GraphQL Codegen for type generation - NEVER write manual TypeScript types for GraphQL)**

**(You MUST include `__typename` and `id` in all optimistic responses for cache normalization)**

**(You MUST configure type policies with appropriate `keyFields` for cache identification)**

**(You MUST use named constants for ALL timeout, retry, and polling values - NO magic numbers)**

**(You MUST use named exports only - NO default exports)**

**(For v4: You MUST import React hooks from `@apollo/client/react` - NOT from `@apollo/client`)**

**Failure to follow these rules will cause cache inconsistencies, type drift, and production bugs.**

</critical_reminders>
