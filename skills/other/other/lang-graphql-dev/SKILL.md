---
name: lang-graphql-dev
description: Foundational GraphQL patterns covering schema design, queries, mutations, subscriptions, and resolvers. Use when building or consuming GraphQL APIs. This is the entry point for GraphQL development.
---

# GraphQL Fundamentals

Foundational GraphQL patterns covering schema definition, queries, mutations, subscriptions, resolvers, and API design best practices. Use this skill when building GraphQL APIs, consuming GraphQL endpoints, or designing data graph architectures.

## Skill Hierarchy

```
lang-graphql-dev (foundational, this skill)
├── graphql-federation (multi-service graphs)
├── graphql-optimization (query performance, n+1, dataloaders)
└── graphql-security (auth, rate limiting, depth limiting)
```

This skill covers:
- Schema definition (types, fields, scalars, enums)
- Query operations and variables
- Mutations and input types
- Subscriptions for real-time updates
- Resolver implementation patterns
- Interfaces and unions for polymorphism
- Custom directives
- Error handling strategies
- API design best practices

## Quick Reference

| Pattern | GraphQL Syntax |
|---------|----------------|
| Object Type | `type User { id: ID! name: String! }` |
| Query Field | `type Query { user(id: ID!): User }` |
| Mutation | `type Mutation { createUser(input: CreateUserInput!): User! }` |
| Subscription | `type Subscription { userCreated: User! }` |
| Non-Null | `field: String!` (cannot be null) |
| List | `users: [User!]!` (non-null list of non-null users) |
| Input Type | `input CreateUserInput { name: String! email: String! }` |
| Enum | `enum Role { ADMIN USER GUEST }` |
| Interface | `interface Node { id: ID! }` |
| Union | `union SearchResult = User \| Post \| Comment` |
| Directive | `field: String @deprecated(reason: "Use newField")` |
| Fragment | `fragment UserFields on User { id name }` |
| Alias | `admin: user(id: "1") { name }` |
| Variable | `query GetUser($id: ID!) { user(id: $id) }` |

## Schema Definition Language (SDL)

### Object Types

Object types represent entities in your API with named fields:

```graphql
# Basic object type
type User {
  id: ID!
  name: String!
  email: String!
  age: Int
  isActive: Boolean!
  createdAt: DateTime!
}

# Type with relationships
type Post {
  id: ID!
  title: String!
  content: String!
  author: User!          # Single relationship
  comments: [Comment!]!  # List relationship
  tags: [String!]!       # List of scalars
  publishedAt: DateTime
}

# Nested object type
type Comment {
  id: ID!
  text: String!
  author: User!
  post: Post!
  replies: [Comment!]!   # Self-referential
  createdAt: DateTime!
}
```

### Scalar Types

Built-in scalars and custom scalar definitions:

```graphql
# Built-in scalars
# Int: 32-bit signed integer
# Float: signed double-precision floating-point
# String: UTF-8 character sequence
# Boolean: true or false
# ID: unique identifier (serialized as String)

# Custom scalar declarations
scalar DateTime
scalar Email
scalar URL
scalar JSON
scalar Upload

# Usage in types
type Event {
  id: ID!
  name: String!
  startTime: DateTime!
  endTime: DateTime!
  website: URL
  metadata: JSON
}

type User {
  id: ID!
  email: Email!
  avatar: URL
}
```

### Enums

Enumeration types with fixed set of values:

```graphql
# Basic enum
enum Role {
  ADMIN
  USER
  GUEST
}

# Enum with descriptions
enum PostStatus {
  """
  Draft state - not visible to public
  """
  DRAFT

  """
  Published and visible to all users
  """
  PUBLISHED

  """
  Archived - read-only access
  """
  ARCHIVED
}

# Enum in type
type User {
  id: ID!
  name: String!
  role: Role!
  status: UserStatus!
}

enum UserStatus {
  ACTIVE
  SUSPENDED
  DEACTIVATED
}
```

### Input Types

Input types for mutation and query arguments:

```graphql
# Basic input type
input CreateUserInput {
  name: String!
  email: String!
  age: Int
  role: Role!
}

# Nested input type
input CreatePostInput {
  title: String!
  content: String!
  authorId: ID!
  tags: [String!]!
  metadata: PostMetadataInput
}

input PostMetadataInput {
  category: String
  featured: Boolean
  seoKeywords: [String!]
}

# Update input (all fields optional)
input UpdateUserInput {
  name: String
  email: String
  age: Int
  role: Role
}

# Filter input for queries
input UserFilterInput {
  role: Role
  isActive: Boolean
  createdAfter: DateTime
  search: String
}

# Pagination input
input PaginationInput {
  limit: Int = 10
  offset: Int = 0
}

input CursorPaginationInput {
  first: Int
  after: String
  last: Int
  before: String
}
```

### Interfaces

Interfaces define common fields shared by multiple types:

```graphql
# Basic interface
interface Node {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
}

# Types implementing interface
type User implements Node {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  name: String!
  email: String!
}

type Post implements Node {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  title: String!
  content: String!
  author: User!
}

# Multiple interfaces
interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

interface Authored {
  author: User!
}

type Article implements Node & Timestamped & Authored {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  author: User!
  title: String!
  body: String!
}

# Querying with interfaces
type Query {
  node(id: ID!): Node
  nodes(ids: [ID!]!): [Node!]!

  # Returns any type implementing Node
  search(query: String!): [Node!]!
}
```

### Unions

Unions represent values that could be one of several types:

```graphql
# Basic union
union SearchResult = User | Post | Comment

# Union in query
type Query {
  search(query: String!): [SearchResult!]!
}

# Querying unions (requires inline fragments)
# query {
#   search(query: "graphql") {
#     ... on User {
#       id
#       name
#       email
#     }
#     ... on Post {
#       id
#       title
#       author { name }
#     }
#     ... on Comment {
#       id
#       text
#       author { name }
#     }
#   }
# }

# Error handling with unions
union CreateUserResult = User | ValidationError | DuplicateEmailError

type ValidationError {
  message: String!
  fields: [String!]!
}

type DuplicateEmailError {
  message: String!
  email: String!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserResult!
}

# Media type union
union Media = Photo | Video | Audio

type Photo {
  id: ID!
  url: URL!
  width: Int!
  height: Int!
}

type Video {
  id: ID!
  url: URL!
  duration: Int!
  thumbnail: URL!
}

type Audio {
  id: ID!
  url: URL!
  duration: Int!
}
```

### Directives

Built-in and custom directives:

```graphql
# Built-in directives

# @deprecated - mark fields as deprecated
type User {
  id: ID!
  name: String!
  username: String! @deprecated(reason: "Use name instead")
  email: String!
}

# @skip - conditionally exclude field
# @include - conditionally include field
# query GetUser($id: ID!, $withEmail: Boolean!) {
#   user(id: $id) {
#     id
#     name
#     email @include(if: $withEmail)
#   }
# }

# Custom directive definitions
directive @auth(
  requires: Role = USER
) on OBJECT | FIELD_DEFINITION

directive @rateLimit(
  limit: Int!
  duration: Int!
) on FIELD_DEFINITION

directive @cacheControl(
  maxAge: Int
  scope: CacheControlScope
) on FIELD_DEFINITION | OBJECT

enum CacheControlScope {
  PUBLIC
  PRIVATE
}

# Using custom directives
type Query {
  publicPosts: [Post!]! @cacheControl(maxAge: 300, scope: PUBLIC)

  me: User! @auth(requires: USER)

  adminUsers: [User!]! @auth(requires: ADMIN)

  search(query: String!): [SearchResult!]!
    @rateLimit(limit: 100, duration: 60)
}

# Field-level directive
type User @auth(requires: USER) {
  id: ID!
  name: String!
  email: String! @auth(requires: ADMIN)
  posts: [Post!]!
}
```

## Root Operation Types

### Query Type

Read-only operations:

```graphql
type Query {
  # Single entity by ID
  user(id: ID!): User
  post(id: ID!): Post

  # List with optional filtering
  users(
    filter: UserFilterInput
    limit: Int = 10
    offset: Int = 0
  ): [User!]!

  # Search operations
  searchUsers(query: String!): [User!]!
  searchPosts(query: String!): [Post!]!
  search(query: String!): [SearchResult!]!

  # Nested queries
  userPosts(userId: ID!, limit: Int = 10): [Post!]!
  postComments(postId: ID!): [Comment!]!

  # Aggregations
  userCount: Int!
  postCount(authorId: ID): Int!

  # Current user
  me: User
}
```

### Mutation Type

Write operations that modify data:

```graphql
type Mutation {
  # Create operations
  createUser(input: CreateUserInput!): User!
  createPost(input: CreatePostInput!): Post!
  createComment(input: CreateCommentInput!): Comment!

  # Update operations
  updateUser(id: ID!, input: UpdateUserInput!): User!
  updatePost(id: ID!, input: UpdatePostInput!): Post!

  # Delete operations
  deleteUser(id: ID!): DeleteResult!
  deletePost(id: ID!): DeleteResult!

  # Batch operations
  deleteUsers(ids: [ID!]!): BatchDeleteResult!
  updateUserRoles(updates: [UserRoleUpdate!]!): [User!]!

  # Complex mutations
  publishPost(id: ID!): Post!
  likePost(postId: ID!): Post!
  followUser(userId: ID!): User!

  # File upload
  uploadAvatar(file: Upload!): User!
}

type DeleteResult {
  success: Boolean!
  id: ID!
}

type BatchDeleteResult {
  success: Boolean!
  deletedCount: Int!
  deletedIds: [ID!]!
}

input UserRoleUpdate {
  userId: ID!
  role: Role!
}
```

### Subscription Type

Real-time event streams:

```graphql
type Subscription {
  # Entity created events
  userCreated: User!
  postCreated: Post!
  commentCreated(postId: ID): Comment!

  # Entity updated events
  userUpdated(id: ID!): User!
  postUpdated(id: ID!): Post!

  # Entity deleted events
  userDeleted: ID!
  postDeleted: ID!

  # Custom events
  messageReceived(channelId: ID!): Message!
  notificationReceived: Notification!

  # Filtered subscriptions
  postsInCategory(category: String!): Post!
  userActivity(userId: ID!): ActivityEvent!
}

type Message {
  id: ID!
  channelId: ID!
  author: User!
  text: String!
  createdAt: DateTime!
}

type Notification {
  id: ID!
  type: NotificationType!
  title: String!
  body: String!
  createdAt: DateTime!
}

enum NotificationType {
  MENTION
  LIKE
  COMMENT
  FOLLOW
}

union ActivityEvent = PostCreated | PostLiked | CommentCreated

type PostCreated {
  post: Post!
}

type PostLiked {
  post: Post!
  user: User!
}

type CommentCreated {
  comment: Comment!
}
```

## Query Operations

### Basic Queries

Simple field selection:

```graphql
# Fetch single user
query GetUser {
  user(id: "123") {
    id
    name
    email
  }
}

# Fetch list of users
query GetUsers {
  users(limit: 10) {
    id
    name
    email
  }
}

# Nested fields
query GetUserWithPosts {
  user(id: "123") {
    id
    name
    posts {
      id
      title
      publishedAt
    }
  }
}

# Multiple root fields
query GetDashboardData {
  me {
    id
    name
  }
  recentPosts(limit: 5) {
    id
    title
  }
  notifications {
    id
    title
  }
}
```

### Query Variables

Parameterized queries for reusability:

```graphql
# Query with variables
query GetUser($userId: ID!, $postLimit: Int = 5) {
  user(id: $userId) {
    id
    name
    email
    posts(limit: $postLimit) {
      id
      title
    }
  }
}

# Variables JSON
{
  "userId": "123",
  "postLimit": 10
}

# Optional variables with defaults
query GetPosts($limit: Int = 10, $offset: Int = 0) {
  posts(limit: $limit, offset: $offset) {
    id
    title
  }
}

# Variables with input types
query SearchUsers($filter: UserFilterInput!) {
  users(filter: $filter) {
    id
    name
    email
  }
}

# Variables JSON
{
  "filter": {
    "role": "ADMIN",
    "isActive": true
  }
}

# Non-null variables
query CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
  }
}
```

### Aliases

Rename fields in response:

```graphql
query GetMultipleUsers {
  admin: user(id: "1") {
    id
    name
  }
  regularUser: user(id: "2") {
    id
    name
  }
}

# Response shape:
# {
#   "data": {
#     "admin": { "id": "1", "name": "Admin User" },
#     "regularUser": { "id": "2", "name": "Regular User" }
#   }
# }

query GetUserStats {
  allUsers: userCount
  activeUsers: userCount(filter: { isActive: true })
  adminUsers: userCount(filter: { role: ADMIN })
}
```

### Fragments

Reusable field selections:

```graphql
# Named fragment
fragment UserFields on User {
  id
  name
  email
  createdAt
}

query GetUsers {
  users {
    ...UserFields
  }
}

query GetUser($id: ID!) {
  user(id: $id) {
    ...UserFields
    posts {
      id
      title
    }
  }
}

# Nested fragments
fragment PostPreview on Post {
  id
  title
  publishedAt
  author {
    ...UserFields
  }
}

fragment CommentFields on Comment {
  id
  text
  author {
    ...UserFields
  }
}

query GetPost($id: ID!) {
  post(id: $id) {
    ...PostPreview
    content
    comments {
      ...CommentFields
    }
  }
}

# Inline fragments for unions
query Search($query: String!) {
  search(query: $query) {
    ... on User {
      id
      name
      email
    }
    ... on Post {
      id
      title
      author { name }
    }
    ... on Comment {
      id
      text
    }
  }
}

# Inline fragments for interfaces
query GetNodes($ids: [ID!]!) {
  nodes(ids: $ids) {
    id
    ... on User {
      name
      email
    }
    ... on Post {
      title
      content
    }
  }
}
```

### Directives in Queries

Conditional field inclusion:

```graphql
query GetUser($id: ID!, $withEmail: Boolean!, $withPosts: Boolean!) {
  user(id: $id) {
    id
    name
    email @include(if: $withEmail)
    posts @include(if: $withPosts) {
      id
      title
    }
  }
}

query GetUsers($skipArchived: Boolean!) {
  users {
    id
    name
    archivedAt @skip(if: $skipArchived)
  }
}

# Combining directives
query GetUserProfile(
  $id: ID!
  $withEmail: Boolean!
  $skipAvatar: Boolean!
) {
  user(id: $id) {
    id
    name
    email @include(if: $withEmail)
    avatar @skip(if: $skipAvatar)
  }
}
```

## Mutation Operations

### Basic Mutations

Create, update, and delete operations:

```graphql
# Create mutation
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
    createdAt
  }
}

# Variables
{
  "input": {
    "name": "John Doe",
    "email": "john@example.com",
    "role": "USER"
  }
}

# Update mutation
mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
  updateUser(id: $id, input: $input) {
    id
    name
    email
    updatedAt
  }
}

# Variables
{
  "id": "123",
  "input": {
    "name": "Jane Doe"
  }
}

# Delete mutation
mutation DeleteUser($id: ID!) {
  deleteUser(id: $id) {
    success
    id
  }
}

# Variables
{
  "id": "123"
}
```

### Multiple Mutations

Execute multiple mutations in sequence:

```graphql
mutation CreateUserAndPost(
  $userInput: CreateUserInput!
  $postInput: CreatePostInput!
) {
  createUser(input: $userInput) {
    id
    name
  }
  createPost(input: $postInput) {
    id
    title
    author { name }
  }
}

# Mutations with aliases
mutation BatchUpdate {
  user1: updateUser(id: "1", input: { name: "User One" }) {
    id
    name
  }
  user2: updateUser(id: "2", input: { name: "User Two" }) {
    id
    name
  }
}
```

### Optimistic Response Pattern

Return updated data after mutation:

```graphql
mutation LikePost($postId: ID!) {
  likePost(postId: $postId) {
    id
    title
    likeCount
    likedBy {
      id
      name
    }
    # Return full post data for cache update
    author {
      id
      name
    }
    createdAt
  }
}

mutation FollowUser($userId: ID!) {
  followUser(userId: $userId) {
    id
    name
    followerCount
    isFollowedByMe
  }
}
```

## Subscription Operations

### Basic Subscriptions

Subscribe to real-time events:

```graphql
subscription OnUserCreated {
  userCreated {
    id
    name
    email
    createdAt
  }
}

subscription OnPostUpdated($postId: ID!) {
  postUpdated(id: $postId) {
    id
    title
    content
    updatedAt
  }
}

subscription OnMessageReceived($channelId: ID!) {
  messageReceived(channelId: $channelId) {
    id
    text
    author {
      id
      name
    }
    createdAt
  }
}
```

### Subscription with Fragments

Reuse fragments in subscriptions:

```graphql
fragment MessageFields on Message {
  id
  text
  author {
    id
    name
    avatar
  }
  createdAt
}

subscription OnNewMessage($channelId: ID!) {
  messageReceived(channelId: $channelId) {
    ...MessageFields
  }
}

query GetMessages($channelId: ID!) {
  messages(channelId: $channelId) {
    ...MessageFields
  }
}
```

## Resolver Patterns

Resolvers are functions that populate data for fields in your schema.

### Basic Resolvers (JavaScript/TypeScript)

```javascript
// Type resolvers
const resolvers = {
  Query: {
    // (parent, args, context, info) => result
    user: async (parent, { id }, context) => {
      return await context.db.users.findById(id);
    },

    users: async (parent, { filter, limit, offset }, context) => {
      return await context.db.users.find(filter, { limit, offset });
    },

    me: async (parent, args, context) => {
      if (!context.user) {
        throw new Error('Not authenticated');
      }
      return context.user;
    }
  },

  Mutation: {
    createUser: async (parent, { input }, context) => {
      if (!context.user || context.user.role !== 'ADMIN') {
        throw new Error('Not authorized');
      }
      return await context.db.users.create(input);
    },

    updateUser: async (parent, { id, input }, context) => {
      return await context.db.users.update(id, input);
    },

    deleteUser: async (parent, { id }, context) => {
      const deleted = await context.db.users.delete(id);
      return { success: true, id };
    }
  },

  Subscription: {
    userCreated: {
      subscribe: (parent, args, context) => {
        return context.pubsub.asyncIterator(['USER_CREATED']);
      }
    },

    postUpdated: {
      subscribe: (parent, { id }, context) => {
        return context.pubsub.asyncIterator([`POST_UPDATED_${id}`]);
      }
    }
  }
};
```

### Field Resolvers

Resolve nested fields:

```javascript
const resolvers = {
  Query: {
    user: async (parent, { id }, context) => {
      return await context.db.users.findById(id);
    }
  },

  User: {
    // Resolve posts for a user
    posts: async (user, { limit }, context) => {
      return await context.db.posts.findByAuthorId(user.id, { limit });
    },

    // Computed field
    fullName: (user) => {
      return `${user.firstName} ${user.lastName}`;
    },

    // Resolve from different data source
    profile: async (user, args, context) => {
      return await context.profileAPI.get(user.profileId);
    },

    // Permission-based field
    email: (user, args, context) => {
      if (context.user?.id === user.id || context.user?.role === 'ADMIN') {
        return user.email;
      }
      return null;
    }
  },

  Post: {
    author: async (post, args, context) => {
      // Use DataLoader to prevent N+1 queries
      return await context.loaders.userLoader.load(post.authorId);
    },

    comments: async (post, args, context) => {
      return await context.db.comments.findByPostId(post.id);
    },

    likeCount: async (post, args, context) => {
      return await context.db.likes.countByPostId(post.id);
    }
  }
};
```

### Interface & Union Resolvers

Resolve type for interfaces and unions:

```javascript
const resolvers = {
  Query: {
    search: async (parent, { query }, context) => {
      const users = await context.db.users.search(query);
      const posts = await context.db.posts.search(query);
      const comments = await context.db.comments.search(query);
      return [...users, ...posts, ...comments];
    },

    node: async (parent, { id }, context) => {
      // Determine type from ID format or lookup
      const type = getTypeFromId(id);
      if (type === 'User') {
        return await context.db.users.findById(id);
      } else if (type === 'Post') {
        return await context.db.posts.findById(id);
      }
      // ... etc
    }
  },

  // Union type resolver
  SearchResult: {
    __resolveType(obj, context, info) {
      if (obj.email) {
        return 'User';
      }
      if (obj.title) {
        return 'Post';
      }
      if (obj.text) {
        return 'Comment';
      }
      return null;
    }
  },

  // Interface type resolver
  Node: {
    __resolveType(obj, context, info) {
      if (obj.email) {
        return 'User';
      }
      if (obj.title) {
        return 'Post';
      }
      // Use __typename if available
      return obj.__typename;
    }
  },

  // Alternative: add __typename in field resolvers
  User: {
    __typename: 'User',
    // ... other fields
  },

  Post: {
    __typename: 'Post',
    // ... other fields
  }
};
```

### DataLoader Pattern (N+1 Prevention)

Batch and cache data loading:

```javascript
import DataLoader from 'dataloader';

// Create loaders
function createLoaders(db) {
  return {
    userLoader: new DataLoader(async (userIds) => {
      const users = await db.users.findByIds(userIds);
      // Return in same order as input
      return userIds.map(id =>
        users.find(user => user.id === id)
      );
    }),

    postLoader: new DataLoader(async (postIds) => {
      const posts = await db.posts.findByIds(postIds);
      return postIds.map(id =>
        posts.find(post => post.id === id)
      );
    }),

    // Batch load posts by author
    postsByAuthorLoader: new DataLoader(async (authorIds) => {
      const posts = await db.posts.findByAuthorIds(authorIds);
      return authorIds.map(authorId =>
        posts.filter(post => post.authorId === authorId)
      );
    })
  };
}

// Use in context
const context = ({ req }) => ({
  user: req.user,
  db,
  loaders: createLoaders(db)
});

// Use in resolvers
const resolvers = {
  Post: {
    author: async (post, args, context) => {
      // Batches multiple author requests
      return await context.loaders.userLoader.load(post.authorId);
    }
  },

  User: {
    posts: async (user, args, context) => {
      // Batches multiple posts-by-author requests
      return await context.loaders.postsByAuthorLoader.load(user.id);
    }
  }
};
```

## Error Handling

### GraphQL Errors

Standard error handling:

```javascript
import { GraphQLError } from 'graphql';

const resolvers = {
  Query: {
    user: async (parent, { id }, context) => {
      const user = await context.db.users.findById(id);

      if (!user) {
        throw new GraphQLError('User not found', {
          extensions: {
            code: 'USER_NOT_FOUND',
            userId: id
          }
        });
      }

      return user;
    }
  },

  Mutation: {
    createUser: async (parent, { input }, context) => {
      // Validation error
      if (!input.email.includes('@')) {
        throw new GraphQLError('Invalid email format', {
          extensions: {
            code: 'BAD_USER_INPUT',
            field: 'email'
          }
        });
      }

      // Authorization error
      if (!context.user) {
        throw new GraphQLError('Not authenticated', {
          extensions: {
            code: 'UNAUTHENTICATED'
          }
        });
      }

      if (context.user.role !== 'ADMIN') {
        throw new GraphQLError('Not authorized', {
          extensions: {
            code: 'FORBIDDEN'
          }
        });
      }

      try {
        return await context.db.users.create(input);
      } catch (error) {
        if (error.code === 'DUPLICATE_EMAIL') {
          throw new GraphQLError('Email already exists', {
            extensions: {
              code: 'DUPLICATE_EMAIL',
              email: input.email
            }
          });
        }
        throw error;
      }
    }
  }
};
```

### Error Response Format

GraphQL error response structure:

```json
{
  "errors": [
    {
      "message": "User not found",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ],
      "path": ["user"],
      "extensions": {
        "code": "USER_NOT_FOUND",
        "userId": "123"
      }
    }
  ],
  "data": {
    "user": null
  }
}
```

### Union-Based Error Handling

Type-safe errors using unions:

```graphql
type User {
  id: ID!
  name: String!
  email: String!
}

type ValidationError {
  message: String!
  fields: [String!]!
}

type NotFoundError {
  message: String!
  resourceId: ID!
}

type AuthenticationError {
  message: String!
}

union CreateUserResult = User | ValidationError | AuthenticationError
union GetUserResult = User | NotFoundError | AuthenticationError

type Query {
  user(id: ID!): GetUserResult!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserResult!
}
```

```javascript
const resolvers = {
  Query: {
    user: async (parent, { id }, context) => {
      if (!context.user) {
        return {
          __typename: 'AuthenticationError',
          message: 'Not authenticated'
        };
      }

      const user = await context.db.users.findById(id);
      if (!user) {
        return {
          __typename: 'NotFoundError',
          message: 'User not found',
          resourceId: id
        };
      }

      return {
        __typename: 'User',
        ...user
      };
    }
  },

  GetUserResult: {
    __resolveType(obj) {
      return obj.__typename;
    }
  },

  CreateUserResult: {
    __resolveType(obj) {
      return obj.__typename;
    }
  }
};
```

Query with union errors:

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    ... on User {
      id
      name
      email
    }
    ... on NotFoundError {
      message
      resourceId
    }
    ... on AuthenticationError {
      message
    }
  }
}
```

## Pagination Patterns

### Offset-Based Pagination

Simple offset/limit pagination:

```graphql
type Query {
  users(limit: Int = 10, offset: Int = 0): UserConnection!
}

type UserConnection {
  items: [User!]!
  totalCount: Int!
  hasMore: Boolean!
}
```

```javascript
const resolvers = {
  Query: {
    users: async (parent, { limit, offset }, context) => {
      const items = await context.db.users.find({}, { limit, offset });
      const totalCount = await context.db.users.count();
      const hasMore = offset + limit < totalCount;

      return { items, totalCount, hasMore };
    }
  }
};
```

### Cursor-Based Pagination (Relay)

Relay-style cursor pagination:

```graphql
type Query {
  users(
    first: Int
    after: String
    last: Int
    before: String
  ): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

```javascript
import { cursorToOffset, offsetToCursor } from './pagination';

const resolvers = {
  Query: {
    users: async (parent, args, context) => {
      const { first, after, last, before } = args;

      let offset = 0;
      let limit = first || last || 10;

      if (after) {
        offset = cursorToOffset(after) + 1;
      }

      const items = await context.db.users.find({}, { limit, offset });
      const totalCount = await context.db.users.count();

      const edges = items.map((node, index) => ({
        node,
        cursor: offsetToCursor(offset + index)
      }));

      const startCursor = edges.length > 0 ? edges[0].cursor : null;
      const endCursor = edges.length > 0 ? edges[edges.length - 1].cursor : null;

      return {
        edges,
        pageInfo: {
          hasNextPage: offset + limit < totalCount,
          hasPreviousPage: offset > 0,
          startCursor,
          endCursor
        },
        totalCount
      };
    }
  }
};

// Cursor utilities
function offsetToCursor(offset) {
  return Buffer.from(`cursor:${offset}`).toString('base64');
}

function cursorToOffset(cursor) {
  return parseInt(Buffer.from(cursor, 'base64').toString().split(':')[1]);
}
```

## Best Practices

### Schema Design

1. **Use Non-Null (!)**  wisely - Required fields should be non-null
2. **Input types for mutations** - Always use input types, not multiple arguments
3. **Consistent naming** - Use camelCase for fields, PascalCase for types
4. **Descriptive names** - `createUser` not `addU`, `userId` not `uid`
5. **Versioning via new fields** - Add new fields instead of changing existing ones
6. **Connection pattern for lists** - Use edges/nodes for paginated lists
7. **Single source of truth** - One field per concept, use aliases for different views

```graphql
# Good
type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
}

input CreateUserInput {
  name: String!
  email: String!
  age: Int
}

# Avoid
type Mutation {
  createUser(name: String!, email: String!, age: Int): User!
  updateUser(id: ID!, name: String, email: String, age: Int): User!
}
```

### Query Design

1. **Request only needed fields** - Avoid over-fetching
2. **Use fragments** - DRY principle for repeated field sets
3. **Leverage aliases** - Fetch same field with different arguments
4. **Batch queries** - Multiple root fields in one request
5. **Named operations** - Always name queries and mutations

```graphql
# Good
query GetDashboard {
  me {
    ...UserFields
  }
  recentPosts(limit: 5) {
    ...PostFields
  }
}

fragment UserFields on User {
  id
  name
  email
}

fragment PostFields on Post {
  id
  title
  publishedAt
}

# Avoid
query {
  me {
    id
    name
    email
    posts {
      id
      title
      content
      comments {
        id
        text
        author {
          id
          name
        }
      }
    }
  }
}
```

### Resolver Best Practices

1. **Context for request-scoped data** - User, loaders, services
2. **Use DataLoaders** - Prevent N+1 queries
3. **Throw GraphQLError** - Consistent error handling
4. **Validate in resolvers** - Don't rely only on schema validation
5. **Keep resolvers thin** - Business logic in service layer
6. **Async/await** - Consistent async pattern

```javascript
// Good
const resolvers = {
  Query: {
    user: async (parent, { id }, context) => {
      return await context.services.users.getById(id);
    }
  },

  User: {
    posts: async (user, args, context) => {
      return await context.loaders.postsByAuthor.load(user.id);
    }
  }
};

// Avoid
const resolvers = {
  Query: {
    user: (parent, { id }) => {
      // Direct database access, no context
      return db.users.findById(id);
    }
  },

  User: {
    posts: (user) => {
      // N+1 query problem
      return db.posts.findByAuthorId(user.id);
    }
  }
};
```

### Security Best Practices

1. **Query depth limiting** - Prevent deeply nested queries
2. **Query complexity analysis** - Assign costs to fields
3. **Rate limiting** - Per-user or per-IP limits
4. **Disable introspection in production** - Hide schema from attackers
5. **Validate input** - Check all user input
6. **Authentication in context** - Check auth before resolvers run
7. **Field-level authorization** - Control access to sensitive fields

```javascript
import depthLimit from 'graphql-depth-limit';
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(5), // Max depth of 5
    createComplexityLimitRule(1000) // Max complexity of 1000
  ],
  introspection: process.env.NODE_ENV !== 'production'
});
```

### Performance Optimization

1. **DataLoader for batching** - Batch database queries
2. **Caching** - Response caching, persisted queries
3. **Field-level caching** - Cache expensive field resolvers
4. **Pagination** - Always paginate lists
5. **Query whitelisting** - Only allow known queries in production
6. **Database query optimization** - Use indexes, avoid N+1
7. **Response compression** - Enable GZIP compression

## Common Patterns

### Relay Global Object Identification

Standardized ID pattern:

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

type Query {
  node(id: ID!): Node
}
```

```javascript
// Encode type into ID
function toGlobalId(type, id) {
  return Buffer.from(`${type}:${id}`).toString('base64');
}

function fromGlobalId(globalId) {
  const [type, id] = Buffer.from(globalId, 'base64').toString().split(':');
  return { type, id };
}

const resolvers = {
  Query: {
    node: async (parent, { id }, context) => {
      const { type, id: localId } = fromGlobalId(id);

      if (type === 'User') {
        return await context.db.users.findById(localId);
      } else if (type === 'Post') {
        return await context.db.posts.findById(localId);
      }

      return null;
    }
  }
};
```

### File Upload

File upload using multipart request:

```graphql
scalar Upload

type Mutation {
  uploadAvatar(file: Upload!): User!
  uploadFiles(files: [Upload!]!): [File!]!
}

type File {
  filename: String!
  mimetype: String!
  encoding: String!
  url: String!
}
```

```javascript
import { GraphQLUpload } from 'graphql-upload';

const resolvers = {
  Upload: GraphQLUpload,

  Mutation: {
    uploadAvatar: async (parent, { file }, context) => {
      const { createReadStream, filename, mimetype } = await file;

      const stream = createReadStream();
      const url = await context.storage.upload(stream, filename);

      return await context.db.users.update(context.user.id, {
        avatar: url
      });
    },

    uploadFiles: async (parent, { files }, context) => {
      const uploadedFiles = [];

      for (const file of files) {
        const { createReadStream, filename, mimetype, encoding } = await file;
        const stream = createReadStream();
        const url = await context.storage.upload(stream, filename);

        uploadedFiles.push({
          filename,
          mimetype,
          encoding,
          url
        });
      }

      return uploadedFiles;
    }
  }
};
```

### Batch Mutations

Efficient bulk operations:

```graphql
type Mutation {
  createUsers(inputs: [CreateUserInput!]!): [User!]!
  updateUsers(updates: [UpdateUserInput!]!): [User!]!
  deleteUsers(ids: [ID!]!): BatchDeleteResult!
}

input UpdateUserInput {
  id: ID!
  name: String
  email: String
}

type BatchDeleteResult {
  success: Boolean!
  deletedCount: Int!
  deletedIds: [ID!]!
}
```

```javascript
const resolvers = {
  Mutation: {
    createUsers: async (parent, { inputs }, context) => {
      return await context.db.users.createMany(inputs);
    },

    updateUsers: async (parent, { updates }, context) => {
      const promises = updates.map(({ id, ...input }) =>
        context.db.users.update(id, input)
      );
      return await Promise.all(promises);
    },

    deleteUsers: async (parent, { ids }, context) => {
      const deletedIds = await context.db.users.deleteMany(ids);

      return {
        success: true,
        deletedCount: deletedIds.length,
        deletedIds
      };
    }
  }
};
```

## Troubleshooting

### Common Issues

**Query not returning data**
- Check resolver return value
- Verify field names match schema
- Check for errors in GraphQL response
- Validate variables are passed correctly

**N+1 Query Problem**
- Symptom: Many database queries for related data
- Solution: Use DataLoader to batch queries
- Example: Loading authors for 100 posts creates 101 queries without batching

**Type Resolution Errors**
- Interface/union types need `__resolveType`
- Return `__typename` field from resolvers
- Verify type names match schema exactly

**Authentication Errors**
- Check context.user is populated
- Verify auth middleware runs before GraphQL
- Use GraphQLError with appropriate code

**Subscription not receiving updates**
- Verify pubsub.publish() is called
- Check subscription filter matches
- Ensure WebSocket connection is established

## References

### Official Documentation
- [GraphQL Specification](https://spec.graphql.org/)
- [GraphQL.org](https://graphql.org/)
- [Apollo Server Documentation](https://www.apollographql.com/docs/apollo-server/)
- [GraphQL Tools](https://www.graphql-tools.com/)

### Tools & Libraries
- **Apollo Server** - GraphQL server for Node.js
- **GraphQL Yoga** - Fully-featured GraphQL server
- **DataLoader** - Batching and caching library
- **GraphQL Code Generator** - Generate types from schema
- **GraphQL Inspector** - Schema validation and comparison

### Related Skills
- `graphql-federation` - Multi-service GraphQL architectures
- `graphql-optimization` - Advanced performance patterns
- `graphql-security` - Authentication, authorization, and rate limiting
- `api-design` - General API design principles
- `lang-typescript-library-dev` - TypeScript for type-safe GraphQL

---

**When to use this skill**: Building GraphQL APIs, designing data graphs, implementing resolvers, consuming GraphQL endpoints, or learning GraphQL fundamentals.

**Skill maintenance**: Update when GraphQL specification changes, new directives are added, or best practices evolve.
