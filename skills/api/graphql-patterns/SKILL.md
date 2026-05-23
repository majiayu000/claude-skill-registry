---
name: graphql-patterns
description: Schema design, resolver patterns, DataLoader, N+1 prevention, and subscription patterns for GraphQL APIs.
---

# GraphQL Patterns

Production-grade GraphQL API design with performance and type safety.

## Schema Design Principles

```graphql
# Use interfaces for shared fields
interface Node {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type User implements Node {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  email: String!
  displayName: String!
  posts(first: Int, after: String): PostConnection!
}

# Relay-style pagination (cursor-based)
type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Input types for mutations
input CreatePostInput {
  title: String!
  body: String!
  tags: [String!]
}

# Union for mutation results (error handling without exceptions)
type CreatePostSuccess {
  post: Post!
}

type ValidationError {
  field: String!
  message: String!
}

union CreatePostResult = CreatePostSuccess | ValidationError
```

## DataLoader - N+1 Prevention

```typescript
import DataLoader from 'dataloader'

// Batch function: receives array of keys, returns array of results in same order
function createUserLoader(db: Database) {
  return new DataLoader<string, User | null>(async (userIds) => {
    const users = await db.user.findMany({
      where: { id: { in: [...userIds] } }
    })
    const userMap = new Map(users.map(u => [u.id, u]))
    // MUST return in same order as input keys
    return userIds.map(id => userMap.get(id) ?? null)
  })
}

// Create per-request context (loaders are NOT shared across requests)
function createContext(req: Request) {
  const db = getDatabase()
  return {
    db,
    loaders: {
      user: createUserLoader(db),
      post: createPostLoader(db),
      comment: createCommentLoader(db),
    }
  }
}

// Resolver uses loader instead of direct DB query
const resolvers = {
  Post: {
    author: (post: Post, _args: unknown, ctx: Context) => {
      return ctx.loaders.user.load(post.authorId)  // batched automatically
    }
  }
}
```

## Resolver Pattern with Validation

```typescript
import { z } from 'zod'

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  body: z.string().min(10).max(50000),
  tags: z.array(z.string()).max(10).optional()
})

const resolvers = {
  Mutation: {
    createPost: async (_parent: unknown, args: { input: unknown }, ctx: Context) => {
      // Auth guard
      if (!ctx.currentUser) {
        throw new AuthenticationError('Login required')
      }

      // Input validation
      const parsed = CreatePostSchema.safeParse(args.input)
      if (!parsed.success) {
        return {
          __typename: 'ValidationError',
          field: parsed.error.issues[0].path.join('.'),
          message: parsed.error.issues[0].message
        }
      }

      const post = await ctx.db.post.create({
        data: { ...parsed.data, authorId: ctx.currentUser.id }
      })

      return { __typename: 'CreatePostSuccess', post }
    }
  }
}
```

## Subscription Patterns

```typescript
import { PubSub, withFilter } from 'graphql-subscriptions'

const pubsub = new PubSub()  // Use RedisPubSub in production

const EVENTS = {
  POST_CREATED: 'POST_CREATED',
  COMMENT_ADDED: 'COMMENT_ADDED',
} as const

const resolvers = {
  Subscription: {
    commentAdded: {
      // Filter: only deliver to subscribers watching this post
      subscribe: withFilter(
        () => pubsub.asyncIterableIterator(EVENTS.COMMENT_ADDED),
        (payload, variables) => payload.commentAdded.postId === variables.postId
      )
    }
  },
  Mutation: {
    addComment: async (_p: unknown, args: { postId: string; body: string }, ctx: Context) => {
      const comment = await ctx.db.comment.create({
        data: { postId: args.postId, body: args.body, authorId: ctx.currentUser!.id }
      })
      await pubsub.publish(EVENTS.COMMENT_ADDED, { commentAdded: comment })
      return comment
    }
  }
}
```

## Query Depth & Complexity Limiting

```typescript
import depthLimit from 'graphql-depth-limit'
import { createComplexityLimitRule } from 'graphql-validation-complexity'

const server = new ApolloServer({
  schema,
  validationRules: [
    depthLimit(7),                          // Max 7 levels deep
    createComplexityLimitRule(1000, {        // Max 1000 complexity points
      scalarCost: 1,
      objectCost: 2,
      listFactor: 10,
    })
  ]
})
```

## Checklist

- [ ] Cursor-based pagination (not offset-based) for all list fields
- [ ] DataLoader for every relationship resolver (one loader per entity per request)
- [ ] Input validation with zod/joi before DB operations
- [ ] Query depth limit (7-10) and complexity limit
- [ ] Auth checks in resolvers, not middleware (field-level control)
- [ ] Union types for mutation results instead of throwing errors
- [ ] Persisted queries in production (disable arbitrary queries)
- [ ] Schema versioned via interfaces, not breaking changes

## Anti-Patterns

- Exposing database IDs directly (use opaque/global IDs)
- Resolver doing N+1 queries without DataLoader
- Sharing DataLoader instances across requests (stale data, auth leak)
- Offset pagination on large datasets (performance cliff)
- God queries: single resolver fetching entire object graph
- Putting business logic in resolvers (keep resolvers thin, use service layer)
