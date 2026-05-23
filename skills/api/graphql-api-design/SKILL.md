---
name: graphql-api-design
description: Auto-activates when user mentions GraphQL, schema design, resolvers, queries, mutations, or Apollo. Expert in designing scalable GraphQL APIs with best practices.
category: backend
---

# GraphQL API Design

Designs clean, scalable GraphQL APIs with type-safe schemas, efficient resolvers, and best practices.

## When This Activates

- User says: "create GraphQL API", "design GraphQL schema", "add GraphQL endpoint"
- User mentions: "GraphQL", "Apollo", "resolvers", "queries", "mutations", "subscriptions"
- Files: schema.graphql, resolvers.ts, typeDefs being created/edited
- API design involving GraphQL

## GraphQL Schema Design

### Type Definitions

```graphql
# schema.graphql

# Object Types
type User {
  id: ID!
  email: String!
  name: String!
  posts: [Post!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  published: Boolean!
  author: User!
  comments: [Comment!]!
  tags: [String!]!
  createdAt: DateTime!
}

type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
  createdAt: DateTime!
}

# Input Types
input CreateUserInput {
  email: String!
  name: String!
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
  tags: [String!]
}

# Custom Scalars
scalar DateTime
scalar JSON
scalar Upload

# Enums
enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

enum SortOrder {
  ASC
  DESC
}

# Pagination
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

# Root Types
type Query {
  # User queries
  me: User
  user(id: ID!): User
  users(
    first: Int
    after: String
    orderBy: String
    order: SortOrder
  ): UserConnection!
  
  # Post queries
  post(id: ID!): Post
  posts(
    first: Int = 20
    after: String
    status: PostStatus
    authorId: ID
  ): PostConnection!
  
  # Search
  search(query: String!, type: SearchType!): SearchResult!
}

type Mutation {
  # User mutations
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
  
  # Post mutations
  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, input: UpdatePostInput!): Post!
  deletePost(id: ID!): Boolean!
  publishPost(id: ID!): Post!
  
  # Comment mutations
  createComment(postId: ID!, content: String!): Comment!
  deleteComment(id: ID!): Boolean!
}

type Subscription {
  postCreated: Post!
  postUpdated(id: ID!): Post!
  commentAdded(postId: ID!): Comment!
}

# Union Types
union SearchResult = User | Post | Comment

# Interfaces
interface Node {
  id: ID!
  createdAt: DateTime!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}
```

## Apollo Server Implementation

### Server Setup

```typescript
// server.ts
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { readFileSync } from 'fs';
import { resolvers } from './resolvers';
import { context } from './context';

const typeDefs = readFileSync('./schema.graphql', 'utf-8');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
  formatError: (error) => {
    console.error('GraphQL Error:', error);
    return {
      message: error.message,
      code: error.extensions?.code,
      path: error.path,
    };
  },
});

const { url } = await startStandaloneServer(server, {
  context,
  listen: { port: 4000 },
});

console.log(`🚀 Server ready at ${url}`);
```

### Resolvers

```typescript
// resolvers.ts
import { GraphQLError } from 'graphql';
import type { Context } from './context';

export const resolvers = {
  Query: {
    me: async (_parent, _args, context: Context) => {
      if (!context.user) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' },
        });
      }
      return context.db.user.findUnique({
        where: { id: context.user.id },
      });
    },

    user: async (_parent, { id }, context: Context) => {
      const user = await context.db.user.findUnique({
        where: { id },
      });
      
      if (!user) {
        throw new GraphQLError('User not found', {
          extensions: { code: 'NOT_FOUND' },
        });
      }
      
      return user;
    },

    posts: async (_parent, { first = 20, after, status, authorId }, context: Context) => {
      const where = {
        ...(status && { status }),
        ...(authorId && { authorId }),
      };

      const posts = await context.db.post.findMany({
        where,
        take: first + 1,
        ...(after && { cursor: { id: after }, skip: 1 }),
        orderBy: { createdAt: 'desc' },
      });

      const hasNextPage = posts.length > first;
      const edges = posts.slice(0, first).map(post => ({
        node: post,
        cursor: post.id,
      }));

      return {
        edges,
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!after,
          startCursor: edges[0]?.cursor,
          endCursor: edges[edges.length - 1]?.cursor,
        },
        totalCount: await context.db.post.count({ where }),
      };
    },
  },

  Mutation: {
    createUser: async (_parent, { input }, context: Context) => {
      const { email, name, password } = input;

      const existingUser = await context.db.user.findUnique({
        where: { email },
      });

      if (existingUser) {
        throw new GraphQLError('Email already exists', {
          extensions: { code: 'BAD_USER_INPUT' },
        });
      }

      const hashedPassword = await context.hashPassword(password);

      return context.db.user.create({
        data: { email, name, password: hashedPassword },
      });
    },

    createPost: async (_parent, { input }, context: Context) => {
      if (!context.user) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' },
        });
      }

      return context.db.post.create({
        data: {
          ...input,
          authorId: context.user.id,
        },
      });
    },

    deletePost: async (_parent, { id }, context: Context) => {
      if (!context.user) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' },
        });
      }

      const post = await context.db.post.findUnique({
        where: { id },
      });

      if (!post) {
        throw new GraphQLError('Post not found', {
          extensions: { code: 'NOT_FOUND' },
        });
      }

      if (post.authorId !== context.user.id) {
        throw new GraphQLError('Not authorized', {
          extensions: { code: 'FORBIDDEN' },
        });
      }

      await context.db.post.delete({ where: { id } });
      return true;
    },
  },

  // Field Resolvers
  User: {
    posts: async (parent, _args, context: Context) => {
      return context.db.post.findMany({
        where: { authorId: parent.id },
      });
    },
  },

  Post: {
    author: async (parent, _args, context: Context) => {
      return context.db.user.findUnique({
        where: { id: parent.authorId },
      });
    },
    comments: async (parent, _args, context: Context) => {
      return context.db.comment.findMany({
        where: { postId: parent.id },
      });
    },
  },

  // Subscription Resolvers
  Subscription: {
    postCreated: {
      subscribe: (_parent, _args, context: Context) => {
        return context.pubsub.asyncIterator(['POST_CREATED']);
      },
    },
    commentAdded: {
      subscribe: (_parent, { postId }, context: Context) => {
        return context.pubsub.asyncIterator([`COMMENT_ADDED_${postId}`]);
      },
    },
  },
};
```

### Context

```typescript
// context.ts
import { PrismaClient } from '@prisma/client';
import { PubSub } from 'graphql-subscriptions';
import { verifyToken } from './auth';

const db = new PrismaClient();
const pubsub = new PubSub();

export interface Context {
  db: PrismaClient;
  pubsub: PubSub;
  user: { id: string; email: string } | null;
  hashPassword: (password: string) => Promise<string>;
}

export async function context({ req }): Promise<Context> {
  const token = req.headers.authorization?.replace('Bearer ', '');
  const user = token ? await verifyToken(token) : null;

  return {
    db,
    pubsub,
    user,
    hashPassword: async (password) => {
      const bcrypt = await import('bcrypt');
      return bcrypt.hash(password, 10);
    },
  };
}
```

## Best Practices

### 1. N+1 Query Problem

```typescript
// ❌ BAD: Causes N+1 queries
const posts = await db.post.findMany();
for (const post of posts) {
  post.author = await db.user.findUnique({ where: { id: post.authorId } });
}

// ✅ GOOD: Use DataLoader
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (ids: string[]) => {
  const users = await db.user.findMany({
    where: { id: { in: ids } },
  });
  return ids.map(id => users.find(u => u.id === id));
});

// In resolver
Post: {
  author: (parent, _args, context) => {
    return context.loaders.user.load(parent.authorId);
  }
}
```

### 2. Input Validation

```typescript
import { GraphQLError } from 'graphql';
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(50),
  password: z.string().min(8),
});

createUser: async (_parent, { input }, context) => {
  const result = createUserSchema.safeParse(input);
  
  if (!result.success) {
    throw new GraphQLError('Invalid input', {
      extensions: {
        code: 'BAD_USER_INPUT',
        errors: result.error.flatten(),
      },
    });
  }
  
  // ... create user
}
```

### 3. Cursor-Based Pagination

```typescript
// Better than offset pagination for large datasets
posts: async (_parent, { first = 20, after }, context) => {
  const posts = await context.db.post.findMany({
    take: first + 1,
    ...(after && { cursor: { id: after }, skip: 1 }),
    orderBy: { createdAt: 'desc' },
  });

  const hasNextPage = posts.length > first;
  const edges = posts.slice(0, first);

  return {
    edges: edges.map(post => ({ node: post, cursor: post.id })),
    pageInfo: {
      hasNextPage,
      endCursor: edges[edges.length - 1]?.id,
    },
  };
}
```

### 4. Error Handling

```typescript
export class AuthenticationError extends GraphQLError {
  constructor(message: string) {
    super(message, {
      extensions: { code: 'UNAUTHENTICATED' },
    });
  }
}

export class ForbiddenError extends GraphQLError {
  constructor(message: string) {
    super(message, {
      extensions: { code: 'FORBIDDEN' },
    });
  }
}

export class NotFoundError extends GraphQLError {
  constructor(resource: string) {
    super(`${resource} not found`, {
      extensions: { code: 'NOT_FOUND' },
    });
  }
}
```

## Client Usage

```typescript
// queries.ts
import { gql } from '@apollo/client';

export const GET_POSTS = gql`
  query GetPosts($first: Int, $after: String) {
    posts(first: $first, after: $after) {
      edges {
        node {
          id
          title
          content
          author {
            id
            name
          }
        }
        cursor
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
`;

export const CREATE_POST = gql`
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
      id
      title
      content
    }
  }
`;

// Component
import { useQuery, useMutation } from '@apollo/client';

function Posts() {
  const { data, loading, fetchMore } = useQuery(GET_POSTS, {
    variables: { first: 20 },
  });

  const [createPost] = useMutation(CREATE_POST, {
    refetchQueries: [{ query: GET_POSTS }],
  });

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {data.posts.edges.map(({ node }) => (
        <div key={node.id}>{node.title}</div>
      ))}
      {data.posts.pageInfo.hasNextPage && (
        <button onClick={() => fetchMore({
          variables: { after: data.posts.pageInfo.endCursor },
        })}>
          Load More
        </button>
      )}
    </div>
  );
}
```

## Schema Design Checklist

- [ ] Use clear, descriptive type names
- [ ] Non-nullable fields for required data (!)
- [ ] Input types for mutations
- [ ] Cursor-based pagination for lists
- [ ] Custom scalars for Date, JSON, etc.
- [ ] Enums for fixed sets of values
- [ ] Error codes in extensions
- [ ] DataLoader for N+1 prevention
- [ ] Field-level authorization
- [ ] Validation before database operations
- [ ] Proper error handling
- [ ] Subscriptions for real-time features

**Design schema, implement resolvers, present complete GraphQL API structure.**
