---
name: graphql
description: Builds APIs with GraphQL including schemas, queries, mutations, resolvers, and client integration. Use when designing flexible APIs, fetching related data, or implementing real-time subscriptions.
---

# GraphQL

Query language for APIs with type system and efficient data fetching.

## Quick Start

**Install (Apollo Server):**
```bash
npm install @apollo/server graphql
```

**Install (Client):**
```bash
npm install @apollo/client graphql
```

## Schema Definition

### Basic Types

```graphql
# schema.graphql
type User {
  id: ID!
  email: String!
  name: String
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  published: Boolean!
  author: User!
  comments: [Comment!]!
  createdAt: DateTime!
}

type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
}

scalar DateTime
```

### Input Types

```graphql
input CreateUserInput {
  email: String!
  name: String
  password: String!
}

input UpdateUserInput {
  email: String
  name: String
}

input CreatePostInput {
  title: String!
  content: String!
  published: Boolean = false
}
```

### Enums

```graphql
enum Role {
  USER
  ADMIN
  MODERATOR
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

type User {
  id: ID!
  role: Role!
}
```

### Interfaces

```graphql
interface Node {
  id: ID!
}

type User implements Node {
  id: ID!
  name: String!
}

type Post implements Node {
  id: ID!
  title: String!
}
```

### Unions

```graphql
union SearchResult = User | Post | Comment

type Query {
  search(term: String!): [SearchResult!]!
}
```

## Queries

### Root Query

```graphql
type Query {
  # Single item
  user(id: ID!): User
  post(id: ID!): Post

  # Lists
  users: [User!]!
  posts(published: Boolean): [Post!]!

  # Pagination
  paginatedPosts(
    first: Int
    after: String
    last: Int
    before: String
  ): PostConnection!

  # Search
  search(term: String!): [SearchResult!]!

  # Current user
  me: User
}
```

### Client Queries

```graphql
# Simple query
query GetUser {
  user(id: "1") {
    id
    name
    email
  }
}

# With variables
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
    posts {
      id
      title
    }
  }
}

# Multiple queries
query Dashboard {
  me {
    id
    name
  }
  recentPosts: posts(first: 5) {
    id
    title
  }
}

# Fragments
fragment UserFields on User {
  id
  name
  email
}

query GetUsers {
  users {
    ...UserFields
    posts {
      id
      title
    }
  }
}
```

## Mutations

### Root Mutation

```graphql
type Mutation {
  # Create
  createUser(input: CreateUserInput!): User!
  createPost(input: CreatePostInput!): Post!

  # Update
  updateUser(id: ID!, input: UpdateUserInput!): User!
  updatePost(id: ID!, input: UpdatePostInput!): Post!

  # Delete
  deleteUser(id: ID!): Boolean!
  deletePost(id: ID!): Boolean!

  # Actions
  login(email: String!, password: String!): AuthPayload!
  publishPost(id: ID!): Post!
}

type AuthPayload {
  token: String!
  user: User!
}
```

### Client Mutations

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}

mutation Login($email: String!, $password: String!) {
  login(email: $email, password: $password) {
    token
    user {
      id
      name
    }
  }
}
```

## Subscriptions

### Schema

```graphql
type Subscription {
  postCreated: Post!
  commentAdded(postId: ID!): Comment!
  userStatusChanged: User!
}
```

### Server Setup

```typescript
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import express from 'express';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();

const resolvers = {
  Subscription: {
    postCreated: {
      subscribe: () => pubsub.asyncIterator(['POST_CREATED']),
    },
  },
  Mutation: {
    createPost: async (_, { input }, ctx) => {
      const post = await ctx.prisma.post.create({ data: input });
      pubsub.publish('POST_CREATED', { postCreated: post });
      return post;
    },
  },
};
```

## Apollo Server

### Basic Setup

```typescript
// server.ts
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { readFileSync } from 'fs';

const typeDefs = readFileSync('./schema.graphql', 'utf-8');

const resolvers = {
  Query: {
    users: async (_, __, { prisma }) => {
      return prisma.user.findMany();
    },
    user: async (_, { id }, { prisma }) => {
      return prisma.user.findUnique({ where: { id } });
    },
  },
  Mutation: {
    createUser: async (_, { input }, { prisma }) => {
      return prisma.user.create({ data: input });
    },
  },
  User: {
    posts: async (parent, _, { prisma }) => {
      return prisma.post.findMany({
        where: { authorId: parent.id },
      });
    },
  },
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

const { url } = await startStandaloneServer(server, {
  context: async ({ req }) => ({
    prisma,
    user: await getUser(req),
  }),
  listen: { port: 4000 },
});

console.log(`Server ready at ${url}`);
```

### Next.js API Route

```typescript
// app/api/graphql/route.ts
import { ApolloServer } from '@apollo/server';
import { startServerAndCreateNextHandler } from '@as-integrations/next';
import { NextRequest } from 'next/server';

const typeDefs = `#graphql
  type Query {
    hello: String
  }
`;

const resolvers = {
  Query: {
    hello: () => 'Hello, World!',
  },
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

const handler = startServerAndCreateNextHandler<NextRequest>(server, {
  context: async (req) => ({
    req,
  }),
});

export { handler as GET, handler as POST };
```

## Apollo Client

### Setup

```typescript
// lib/apollo-client.ts
import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';

const httpLink = new HttpLink({
  uri: '/api/graphql',
});

export const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
});
```

### Provider

```tsx
// app/providers.tsx
'use client';

import { ApolloProvider } from '@apollo/client';
import { client } from '@/lib/apollo-client';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ApolloProvider client={client}>
      {children}
    </ApolloProvider>
  );
}
```

### useQuery

```tsx
import { gql, useQuery } from '@apollo/client';

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      email
    }
  }
`;

function UserList() {
  const { loading, error, data, refetch } = useQuery(GET_USERS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <ul>
      {data.users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### useMutation

```tsx
import { gql, useMutation } from '@apollo/client';

const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      id
      name
      email
    }
  }
`;

function CreateUserForm() {
  const [createUser, { loading, error }] = useMutation(CREATE_USER, {
    refetchQueries: ['GetUsers'],
    onCompleted: (data) => {
      console.log('User created:', data.createUser);
    },
  });

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    await createUser({
      variables: {
        input: {
          name: formData.get('name'),
          email: formData.get('email'),
        },
      },
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" placeholder="Name" />
      <input name="email" placeholder="Email" />
      <button disabled={loading}>
        {loading ? 'Creating...' : 'Create User'}
      </button>
      {error && <p>{error.message}</p>}
    </form>
  );
}
```

### useSubscription

```tsx
import { gql, useSubscription } from '@apollo/client';

const POST_CREATED = gql`
  subscription OnPostCreated {
    postCreated {
      id
      title
    }
  }
`;

function NewPosts() {
  const { data, loading } = useSubscription(POST_CREATED);

  if (loading) return null;

  return <p>New post: {data?.postCreated.title}</p>;
}
```

## Pagination

### Cursor-Based

```graphql
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type PostEdge {
  cursor: String!
  node: Post!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type Query {
  posts(first: Int, after: String): PostConnection!
}
```

```typescript
// Resolver
posts: async (_, { first = 10, after }, { prisma }) => {
  const posts = await prisma.post.findMany({
    take: first + 1,
    cursor: after ? { id: after } : undefined,
    skip: after ? 1 : 0,
    orderBy: { createdAt: 'desc' },
  });

  const hasNextPage = posts.length > first;
  const edges = hasNextPage ? posts.slice(0, -1) : posts;

  return {
    edges: edges.map((post) => ({
      cursor: post.id,
      node: post,
    })),
    pageInfo: {
      hasNextPage,
      endCursor: edges[edges.length - 1]?.id,
    },
  };
},
```

## Error Handling

### Custom Errors

```typescript
import { GraphQLError } from 'graphql';

const resolvers = {
  Mutation: {
    createPost: async (_, { input }, { prisma, user }) => {
      if (!user) {
        throw new GraphQLError('Not authenticated', {
          extensions: {
            code: 'UNAUTHENTICATED',
          },
        });
      }

      if (!user.canCreatePosts) {
        throw new GraphQLError('Not authorized', {
          extensions: {
            code: 'FORBIDDEN',
          },
        });
      }

      return prisma.post.create({ data: input });
    },
  },
};
```

## Best Practices

1. **Use fragments** - Reuse field selections
2. **Implement pagination** - For lists
3. **Use DataLoader** - Prevent N+1 queries
4. **Validate inputs** - Use custom scalars
5. **Document schema** - Add descriptions

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| N+1 queries | Use DataLoader |
| Over-fetching | Query only needed fields |
| No error handling | Return proper errors |
| Missing types | Add Input types |
| No caching | Configure cache policies |

## Reference Files

- [references/schema.md](references/schema.md) - Schema design
- [references/resolvers.md](references/resolvers.md) - Resolver patterns
- [references/caching.md](references/caching.md) - Cache strategies
