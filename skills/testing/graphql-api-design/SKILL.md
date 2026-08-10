---
name: graphql-api-design
description: Design GraphQL APIs with well-structured schemas, efficient resolvers, pagination, and performance patterns like DataLoader and federation. Use when the user requests graphql api design or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# GraphQL API Design

This skill enables an AI agent to design complete GraphQL APIs from specifications, schemas, or natural language descriptions. The agent produces type definitions, queries, mutations, subscriptions, input types, enums, and resolver implementations. It applies performance patterns including DataLoader for N+1 prevention, cursor-based pagination via the Relay connection spec, query depth limiting, and schema federation for microservice architectures.

## Workflow

1. **Model the domain as types:** Analyze the application domain and define GraphQL object types, input types, enums, interfaces, and unions. Each type should represent a real entity with fields that match the data consumers actually need. Use non-nullable (`!`) annotations deliberately—fields that can genuinely be absent should be nullable. Prefer specific scalar types (e.g., `DateTime`, `URL`) over raw `String` for self-documenting schemas.

2. **Design queries and mutations:** Define Query fields for read operations and Mutation fields for write operations. Queries should be noun-based (`user`, `posts`) while mutations should be verb-based (`createPost`, `updateUser`). Each mutation should accept a single input type argument and return a payload type that includes the modified object plus any user-facing errors. This pattern keeps mutations consistent and extensible.

3. **Implement pagination with connections:** For any list field that could return many items, use the Relay connection specification with `edges`, `node`, `cursor`, and `pageInfo`. This provides cursor-based pagination that is stable under insertions and deletions, unlike offset-based pagination. Define reusable connection types per entity rather than returning raw arrays.

4. **Write resolvers with DataLoader:** Implement resolvers that use DataLoader to batch and cache database lookups within a single request. Without DataLoader, a query that fetches 50 posts and their authors would make 50 separate author queries (the N+1 problem). DataLoader collapses these into a single batched query. Create a new DataLoader instance per request to avoid leaking data between users.

5. **Add subscriptions for real-time data:** Define Subscription fields for events clients need to react to in real-time (e.g., new messages, status changes). Use a pub/sub backend (Redis, Kafka, or in-memory for development) to publish events. Keep subscription payloads lean—clients can use the subscription trigger to refetch full data if needed.

6. **Secure and optimize the schema:** Add query depth limiting (max 10-15 levels) and query complexity analysis to prevent abusive queries. Implement field-level authorization in resolvers. Use persisted queries in production to reduce bandwidth and prevent arbitrary query execution. Consider schema federation if the API spans multiple services.

## Supported Technologies

- **Servers:** Apollo Server, GraphQL Yoga, Mercurius (Fastify), Strawberry (Python), graphql-java
- **Schema tools:** SDL-first (typeDefs), code-first (TypeGraphQL, Nexus, Pothos)
- **Performance:** DataLoader, @defer/@stream directives, persisted queries, automatic persisted queries (APQ)
- **Federation:** Apollo Federation, GraphQL Mesh, Schema Stitching
- **Testing:** GraphQL Playground, Apollo Studio, graphql-test (jest), Insomnia

## Usage

Provide the agent with a description of the data entities, their relationships, and the operations needed. The agent will produce a complete SDL schema, resolver implementations, and DataLoader setup. Specify whether you want SDL-first or code-first output, and which server framework to target.

## Examples

### Example 1: Blog Platform Schema with Resolvers

```graphql
# schema.graphql — Complete blog platform schema

scalar DateTime

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

type User {
  id: ID!
  username: String!
  email: String!
  bio: String
  avatarUrl: String
  posts(first: Int, after: String): PostConnection!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  slug: String!
  content: String!
  excerpt: String
  status: PostStatus!
  author: User!
  tags: [Tag!]!
  comments(first: Int, after: String): CommentConnection!
  publishedAt: DateTime
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Comment {
  id: ID!
  body: String!
  author: User!
  post: Post!
  createdAt: DateTime!
}

type Tag {
  id: ID!
  name: String!
  slug: String!
  posts(first: Int, after: String): PostConnection!
}

# Relay connection types for cursor-based pagination
type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  cursor: String!
  node: Post!
}

type CommentConnection {
  edges: [CommentEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type CommentEdge {
  cursor: String!
  node: Comment!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Queries
type Query {
  post(id: ID, slug: String): Post
  posts(
    first: Int = 10
    after: String
    status: PostStatus
    tagSlug: String
  ): PostConnection!
  user(id: ID!): User
  me: User
  tags: [Tag!]!
}

# Mutations with input types and payload types
input CreatePostInput {
  title: String!
  content: String!
  tagIds: [ID!]
  status: PostStatus = DRAFT
}

type CreatePostPayload {
  post: Post
  errors: [MutationError!]!
}

input UpdatePostInput {
  title: String
  content: String
  status: PostStatus
  tagIds: [ID!]
}

type UpdatePostPayload {
  post: Post
  errors: [MutationError!]!
}

type MutationError {
  field: String
  message: String!
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
  updatePost(id: ID!, input: UpdatePostInput!): UpdatePostPayload!
  deletePost(id: ID!): Boolean!
  addComment(postId: ID!, body: String!): Comment!
}

# Subscriptions
type Subscription {
  commentAdded(postId: ID!): Comment!
  postPublished: Post!
}
```

```javascript
// resolvers.js — Resolvers with DataLoader for N+1 prevention
const DataLoader = require("dataloader");

// Create loaders per request (called from context factory)
function createLoaders(db) {
  return {
    userLoader: new DataLoader(async (userIds) => {
      const users = await db.users.findByIds(userIds);
      const userMap = new Map(users.map((u) => [u.id, u]));
      return userIds.map((id) => userMap.get(id) || null);
    }),
    postLoader: new DataLoader(async (postIds) => {
      const posts = await db.posts.findByIds(postIds);
      const postMap = new Map(posts.map((p) => [p.id, p]));
      return postIds.map((id) => postMap.get(id) || null);
    }),
  };
}

const resolvers = {
  Query: {
    post: (_, { id, slug }, { db }) => {
      if (id) return db.posts.findById(id);
      if (slug) return db.posts.findBySlug(slug);
      return null;
    },
    posts: async (_, { first = 10, after, status, tagSlug }, { db }) => {
      const cursor = after ? decodeCursor(after) : null;
      const { rows, totalCount } = await db.posts.findPaginated({
        limit: first + 1,
        cursor,
        status,
        tagSlug,
      });
      const hasNextPage = rows.length > first;
      const edges = rows.slice(0, first).map((post) => ({
        cursor: encodeCursor(post.id),
        node: post,
      }));
      return {
        edges,
        totalCount,
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!after,
          startCursor: edges[0]?.cursor || null,
          endCursor: edges[edges.length - 1]?.cursor || null,
        },
      };
    },
    me: (_, __, { currentUser }) => currentUser,
  },
  Post: {
    author: (post, _, { loaders }) => loaders.userLoader.load(post.authorId),
    tags: (post, _, { db }) => db.tags.findByPostId(post.id),
  },
  Comment: {
    author: (comment, _, { loaders }) => loaders.userLoader.load(comment.authorId),
  },
  Mutation: {
    createPost: async (_, { input }, { currentUser, db }) => {
      if (!currentUser) return { post: null, errors: [{ message: "Not authenticated" }] };
      if (!input.title.trim()) {
        return { post: null, errors: [{ field: "title", message: "Title cannot be empty" }] };
      }
      const post = await db.posts.create({ ...input, authorId: currentUser.id });
      return { post, errors: [] };
    },
  },
};

function encodeCursor(id) { return Buffer.from(`cursor:${id}`).toString("base64"); }
function decodeCursor(cursor) { return Buffer.from(cursor, "base64").toString().replace("cursor:", ""); }
```

### Example 2: Cursor-Based Pagination Implementation

```javascript
// pagination.js — Reusable cursor-based pagination for any entity

/**
 * Generic paginated query builder for SQL databases.
 * Works with any table that has an auto-incrementing or sortable ID.
 */
async function paginatedQuery(db, { table, first = 10, after, where = {} }) {
  const limit = Math.min(first, 100); // Cap at 100 per page
  const conditions = [];
  const params = [];

  // Apply cursor (decode to original ID)
  if (after) {
    const cursorId = Buffer.from(after, "base64").toString().split(":")[1];
    conditions.push(`id < $${params.length + 1}`);
    params.push(cursorId);
  }

  // Apply additional filters
  for (const [key, value] of Object.entries(where)) {
    if (value !== undefined) {
      conditions.push(`${key} = $${params.length + 1}`);
      params.push(value);
    }
  }

  const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";

  // Fetch one extra row to determine hasNextPage
  const query = `SELECT * FROM ${table} ${whereClause} ORDER BY id DESC LIMIT ${limit + 1}`;
  const rows = await db.query(query, params);

  // Count total matching rows
  const countQuery = `SELECT COUNT(*) as total FROM ${table} ${whereClause}`;
  const [{ total: totalCount }] = await db.query(countQuery, params);

  const hasNextPage = rows.length > limit;
  const nodes = rows.slice(0, limit);

  const edges = nodes.map((node) => ({
    cursor: Buffer.from(`cursor:${node.id}`).toString("base64"),
    node,
  }));

  return {
    edges,
    totalCount,
    pageInfo: {
      hasNextPage,
      hasPreviousPage: !!after,
      startCursor: edges[0]?.cursor || null,
      endCursor: edges[edges.length - 1]?.cursor || null,
    },
  };
}

// Usage in resolver
const resolvers = {
  Query: {
    posts: (_, args, { db }) =>
      paginatedQuery(db, {
        table: "posts",
        first: args.first,
        after: args.after,
        where: { status: args.status },
      }),
  },
};
```

## Best Practices

- **Keep mutations consistent** by always using a single `input` argument and returning a payload type with both the result and a list of user-facing errors. This makes client code predictable.
- **Solve N+1 with DataLoader** on every relationship resolver. Create DataLoader instances per-request (in the context factory) to avoid leaking cached data between users or requests.
- **Limit query depth and complexity** to prevent denial-of-service attacks. Set max depth to 10-15 and assign complexity costs to fields (especially connections and nested relationships).
- **Use nullable return types for single-entity queries** (`post(id: ID!): Post` returns `null` if not found) and non-nullable arrays for list queries (`tags: [Tag!]!` always returns an array, possibly empty).
- **Version via schema evolution, not URL versioning.** Add new fields freely (non-breaking), deprecate old fields with `@deprecated(reason: "Use newField instead")`, and remove them after clients have migrated.
- **Use input types for all mutation arguments** rather than passing individual scalar arguments. This makes it easy to add optional fields later without breaking existing clients.

## Edge Cases

- **Circular references:** Types like `User -> Posts -> Author -> Posts` create circular schemas. This is valid in GraphQL but requires depth limiting to prevent infinite queries. DataLoader prevents infinite resolution loops.
- **Null propagation:** If a non-nullable field resolver throws an error, the null propagates upward to the nearest nullable parent. Design nullable boundaries carefully to prevent one field error from nullifying an entire response.
- **Empty connections:** Return `{ edges: [], pageInfo: { hasNextPage: false, hasPreviousPage: false }, totalCount: 0 }` for empty result sets, not `null`.
- **Cursor stability:** Cursors should be opaque and stable across insertions. Using row IDs as cursor values (base64 encoded) is stable; using offsets is not and breaks when items are inserted or deleted.
- **File uploads:** GraphQL doesn't natively support file uploads. Use the multipart request spec (`graphql-upload`) or handle uploads via a separate REST endpoint and pass the resulting URL to a mutation.
- **Subscription connection drops:** Clients can lose WebSocket connections. Design subscriptions so clients can recover state by re-querying on reconnect rather than relying solely on the subscription stream.
