---
name: urql
description: >-
  You are an expert in urql, the highly customizable and lightweight GraphQL
  client for React, Vue, Svelte, and vanilla JavaScript. You help developers
  fetch GraphQL data with minimal bundle size, document caching, normalized
  caching via Graphcache, exchanges (middleware pipeline), subscriptions, and
  offline support — providing a leaner alternative to Apollo Client with
  better extensibility.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Frontend Development
  tags:
    - graphql
    - react
    - client
    - lightweight
    - cache
    - exchange
    - typescript
---

# urql — Lightweight GraphQL Client

You are an expert in urql, the highly customizable and lightweight GraphQL client for React, Vue, Svelte, and vanilla JavaScript. You help developers fetch GraphQL data with minimal bundle size, document caching, normalized caching via Graphcache, exchanges (middleware pipeline), subscriptions, and offline support — providing a leaner alternative to Apollo Client with better extensibility.

## Core Capabilities

### Setup and Queries

```tsx
import { Client, Provider, cacheExchange, fetchExchange, gql, useQuery, useMutation } from "urql";

const client = new Client({
  url: "https://api.example.com/graphql",
  exchanges: [cacheExchange, fetchExchange],
  fetchOptions: () => ({
    headers: { Authorization: `Bearer ${getToken()}` },
  }),
});

function App() {
  return <Provider value={client}><Dashboard /></Provider>;
}

const POSTS_QUERY = gql`
  query Posts($limit: Int!) {
    posts(limit: $limit) { id title author { name } createdAt }
  }
`;

function PostList() {
  const [result, reexecute] = useQuery({
    query: POSTS_QUERY,
    variables: { limit: 10 },
  });

  const { data, fetching, error } = result;
  if (fetching) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return (
    <div>
      {data.posts.map(p => <PostCard key={p.id} post={p} />)}
      <button onClick={() => reexecute({ requestPolicy: "network-only" })}>Refresh</button>
    </div>
  );
}
```

### Mutations

```tsx
const CREATE_POST = gql`
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) { id title createdAt }
  }
`;

function CreatePostForm() {
  const [result, createPost] = useMutation(CREATE_POST);

  const handleSubmit = (data: any) => {
    createPost({ input: data }).then(result => {
      if (result.error) console.error(result.error);
    });
  };

  return <Form onSubmit={handleSubmit} loading={result.fetching} />;
}
```

### Graphcache (Normalized Cache)

```typescript
import { cacheExchange } from "@urql/exchange-graphcache";

const cache = cacheExchange({
  keys: { Post: (data) => data.id as string },
  resolvers: {
    Query: {
      post: (_, args) => ({ __typename: "Post", id: args.id }),
    },
  },
  updates: {
    Mutation: {
      createPost(result, _args, cache) {
        cache.updateQuery({ query: POSTS_QUERY, variables: { limit: 10 } }, (data) => {
          if (data) data.posts.unshift(result.createPost);
          return data;
        });
      },
    },
  },
});
```

## Installation

```bash
npm install urql graphql
npm install @urql/exchange-graphcache     # Optional normalized cache
```

## Best Practices

1. **Document cache** — Default cache deduplicates by query+variables; sufficient for most apps
2. **Graphcache for complex** — Use normalized cache only when you need cache updates across queries
3. **Exchanges** — urql's middleware pipeline; add auth, retry, persist, logging as composable exchanges
4. **Request policies** — Use `cache-first` (default), `network-only` for refresh, `cache-and-network` for stale-while-revalidate
5. **Bundle size** — urql core is ~5KB gzipped (vs Apollo ~30KB); ideal for performance-sensitive apps
6. **SSR support** — Use `ssrExchange` for server-side rendering; hydrates cache on client
7. **Subscriptions** — Add `subscriptionExchange` for WebSocket/SSE subscriptions; plug and play
8. **Framework agnostic** — Works with React, Vue, Svelte, and vanilla JS; same core, different bindings
