---
name: graphql-schema-design
description: Use when designing GraphQL schemas with type system, SDL patterns, field design, pagination, directives, and versioning strategies for maintainable and scalable APIs.
allowed-tools: []
---

# GraphQL Schema Design

Apply GraphQL schema design principles to create well-structured,
maintainable, and scalable GraphQL APIs. This skill covers the type
system, Schema Definition Language (SDL), field design patterns,
pagination strategies, directives, and schema evolution techniques.

## Core Type System

### Object Types

Object types are the fundamental building blocks of GraphQL schemas.
Each object type represents a kind of object you can fetch from your
service, and what fields it has.

```graphql
type User {
  id: ID!
  username: String!
  email: String!
  createdAt: DateTime!
  posts: [Post!]!
  profile: Profile
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  publishedAt: DateTime
  tags: [String!]!
}
```

### Interface Types

Interfaces define abstract types that multiple object types can
implement. Use interfaces when multiple types share common fields.

```graphql
interface Node {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Article implements Node & Timestamped {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  title: String!
  content: String!
  author: User!
}

type Comment implements Node & Timestamped {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  text: String!
  author: User!
  post: Post!
}
```

### Union Types

Union types represent values that could be one of several object types.
Use unions when a field can return different types without shared
fields.

```graphql
union SearchResult = Article | User | Tag | Comment

type Query {
  search(query: String!): [SearchResult!]!
}

# Query example
query {
  search(query: "graphql") {
    __typename
    ... on Article {
      title
      content
    }
    ... on User {
      username
      email
    }
    ... on Tag {
      name
      count
    }
  }
}
```

### Enum Types

Enums define a specific set of allowed values for a field. Use enums
for fields with a fixed set of options to ensure type safety.

```graphql
enum UserRole {
  ADMIN
  MODERATOR
  USER
  GUEST
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
  DELETED
}

enum SortOrder {
  ASC
  DESC
}

type User {
  id: ID!
  role: UserRole!
  status: AccountStatus!
}

enum AccountStatus {
  ACTIVE
  SUSPENDED
  DEACTIVATED
}
```

### Input Types

Input types are used for complex arguments in queries and mutations.
They allow you to pass structured data as a single argument.

```graphql
input CreateUserInput {
  username: String!
  email: String!
  password: String!
  profile: UserProfileInput
}

input UserProfileInput {
  firstName: String
  lastName: String
  bio: String
  avatarUrl: String
}

input UpdatePostInput {
  title: String
  content: String
  status: PostStatus
  tags: [String!]
}

input PostFilterInput {
  status: PostStatus
  authorId: ID
  tags: [String!]
  createdAfter: DateTime
  createdBefore: DateTime
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updatePost(id: ID!, input: UpdatePostInput!): Post!
}

type Query {
  posts(filter: PostFilterInput, limit: Int): [Post!]!
}
```

## Custom Scalars

Custom scalars extend the built-in scalar types (String, Int, Float,
Boolean, ID) with domain-specific types.

```graphql
scalar DateTime
scalar EmailAddress
scalar URL
scalar JSON
scalar UUID
scalar PositiveInt
scalar Currency

type User {
  id: UUID!
  email: EmailAddress!
  website: URL
  createdAt: DateTime!
  metadata: JSON
  age: PositiveInt
}

type Product {
  id: ID!
  price: Currency!
  images: [URL!]!
}
```

## Directives

Directives provide a way to modify execution behavior or add metadata
to your schema.

```graphql
# Built-in directives
type Query {
  # Skip field if condition is true
  user(id: ID!): User @skip(if: $skipUser)

  # Include field only if condition is true
  posts: [Post!]! @include(if: $includePosts)
}

type Post {
  id: ID!
  title: String!
  # Mark field as deprecated with migration hint
  oldTitle: String @deprecated(reason: "Use 'title' instead")
}

# Custom directives
directive @auth(requires: UserRole!) on FIELD_DEFINITION
directive @rateLimit(max: Int!, window: Int!) on FIELD_DEFINITION
directive @cacheControl(
  maxAge: Int!
  scope: CacheScope = PUBLIC
) on FIELD_DEFINITION | OBJECT

enum CacheScope {
  PUBLIC
  PRIVATE
}

type Query {
  me: User @auth(requires: USER)
  adminPanel: AdminData @auth(requires: ADMIN)

  publicPosts: [Post!]!
    @cacheControl(maxAge: 300)
    @rateLimit(max: 100, window: 60)
}
```

## Nullable vs Non-Null Design

Carefully consider nullability in your schema design. Non-null fields
provide stronger guarantees but reduce flexibility.

```graphql
type User {
  # Required fields - will never be null
  id: ID!
  username: String!
  email: String!

  # Optional fields - may be null
  bio: String
  website: URL

  # Non-null list with nullable items
  # List itself will never be null, but items can be
  favoriteColors: [String]!

  # Nullable list with non-null items
  # List can be null, but if present, items won't be
  phoneNumbers: [String!]

  # Non-null list with non-null items
  # Neither list nor items will be null
  roles: [UserRole!]!

  # Optional relationship
  profile: Profile

  # Required relationship
  account: Account!
}
```

## Pagination Patterns

### Offset-Based Pagination

Simple pagination using limit and offset. Easy to implement but has
performance issues with large offsets.

```graphql
type Query {
  posts(limit: Int = 10, offset: Int = 0): PostsResult!
}

type PostsResult {
  posts: [Post!]!
  total: Int!
  hasMore: Boolean!
}

# Query example
query {
  posts(limit: 20, offset: 40) {
    posts {
      id
      title
    }
    total
    hasMore
  }
}
```

### Cursor-Based Pagination (Connections)

More efficient for large datasets and supports bidirectional
pagination. Based on Relay Connection specification.

```graphql
type Query {
  posts(
    first: Int
    after: String
    last: Int
    before: String
  ): PostConnection!
}

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

# Query example
query {
  posts(first: 10, after: "Y3Vyc29yOjEw") {
    edges {
      cursor
      node {
        id
        title
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

## Mutation Design Patterns

### Input Object Pattern

Use input objects for mutations to allow for easier evolution and
better organization of arguments.

```graphql
type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
  updatePost(input: UpdatePostInput!): UpdatePostPayload!
  deletePost(input: DeletePostInput!): DeletePostPayload!
}

input CreatePostInput {
  title: String!
  content: String!
  authorId: ID!
  tags: [String!]
  publishedAt: DateTime
}

type CreatePostPayload {
  post: Post
  errors: [UserError!]
  success: Boolean!
}

type UserError {
  message: String!
  field: String
  code: String!
}

input UpdatePostInput {
  id: ID!
  title: String
  content: String
  status: PostStatus
}

type UpdatePostPayload {
  post: Post
  errors: [UserError!]
  success: Boolean!
}
```

## Error Handling in Schema

Design your schema to support both field-level and mutation-level
error handling.

```graphql
type Mutation {
  # Option 1: Union return type
  login(email: String!, password: String!): LoginResult!
}

union LoginResult = LoginSuccess | LoginError

type LoginSuccess {
  user: User!
  token: String!
  expiresAt: DateTime!
}

type LoginError {
  message: String!
  code: LoginErrorCode!
}

enum LoginErrorCode {
  INVALID_CREDENTIALS
  ACCOUNT_LOCKED
  EMAIL_NOT_VERIFIED
}

# Option 2: Payload with errors array
type Mutation {
  updateUser(input: UpdateUserInput!): UpdateUserPayload!
}

type UpdateUserPayload {
  user: User
  errors: [UserError!]
  success: Boolean!
}
```

## Schema Stitching and Federation Basics

### Schema Federation

Design schemas for federation by defining entities and extending types
across services.

```graphql
# User service
type User @key(fields: "id") {
  id: ID!
  username: String!
  email: String!
}

# Posts service
extend type User @key(fields: "id") {
  id: ID! @external
  posts: [Post!]!
}

type Post @key(fields: "id") {
  id: ID!
  title: String!
  content: String!
  author: User!
}

# Reviews service
extend type Post @key(fields: "id") {
  id: ID! @external
  reviews: [Review!]!
}

type Review {
  id: ID!
  rating: Int!
  comment: String
  post: Post!
}
```

## Versioning Strategies

### Field Deprecation

Mark fields as deprecated while maintaining backward compatibility.

```graphql
type User {
  id: ID!
  name: String! @deprecated(
    reason: "Use 'firstName' and 'lastName' instead"
  )
  firstName: String!
  lastName: String!

  email: String! @deprecated(
    reason: "Use 'primaryEmail' from ContactInfo"
  )
  contactInfo: ContactInfo!
}

type ContactInfo {
  primaryEmail: String!
  secondaryEmails: [String!]!
}
```

### Additive Changes

Add new fields and types without breaking existing queries.

```graphql
# Version 1
type Post {
  id: ID!
  title: String!
  content: String!
}

# Version 2 - Additive changes
type Post {
  id: ID!
  title: String!
  content: String!
  # New fields added
  summary: String
  readingTime: Int
  tags: [Tag!]!
}

# New type added
type Tag {
  id: ID!
  name: String!
  color: String
}
```

## Best Practices

1. **Use meaningful names**: Choose clear, descriptive names for types,
   fields, and arguments that reflect their purpose and domain
2. **Design for nullable fields**: Make fields nullable by default
   unless you can guarantee the value will always be present
3. **Prefer input objects**: Use input types for complex arguments in
   mutations to allow for easier evolution
4. **Implement pagination**: Always paginate list fields that could
   grow unbounded using cursor-based or offset-based patterns
5. **Use enums for fixed sets**: Define enums for fields with a
   limited set of possible values to ensure type safety
6. **Document your schema**: Add descriptions to types, fields, and
   arguments using GraphQL description syntax
7. **Version through deprecation**: Use @deprecated directive rather
   than removing fields to maintain backward compatibility
8. **Design mutations carefully**: Return payload types that include
   both the result and potential errors
9. **Keep schema flat**: Avoid deeply nested types that could lead to
   complex queries and N+1 problems
10. **Use interfaces wisely**: Define interfaces for shared fields
    across multiple types to enable polymorphic queries

## Common Pitfalls

1. **Over-fetching in schema design**: Creating fields that return
   entire objects when only specific data is needed
2. **Under-fetching**: Not providing enough related data, forcing
   clients to make multiple requests
3. **Circular dependencies**: Creating circular references between
   types without careful resolver design
4. **Breaking changes**: Removing or renaming fields without
   deprecation period, breaking existing clients
5. **No pagination**: Returning unbounded lists that can cause
   performance issues as data grows
6. **Inconsistent naming**: Using different conventions for similar
   fields across types
7. **Over-use of non-null**: Making too many fields non-null, reducing
   schema flexibility and resilience
8. **Missing error handling**: Not designing proper error handling in
   mutation payloads
9. **Ignoring N+1 problems**: Creating schema designs that inherently
   lead to N+1 query problems
10. **Poor input validation**: Not defining constraints on input types,
    leading to runtime validation issues

## When to Use This Skill

Use GraphQL schema design skills when:

- Designing a new GraphQL API from scratch
- Refactoring an existing GraphQL schema for better structure
- Adding new features to an existing schema
- Migrating from REST to GraphQL
- Implementing schema federation across microservices
- Optimizing schema for performance and maintainability
- Establishing schema design standards for a team
- Reviewing and improving schema design patterns
- Designing for long-term API evolution and versioning
- Creating reusable schema patterns and conventions

## Resources

- [GraphQL Specification](https://spec.graphql.org/) - Official
  GraphQL specification
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/) -
  Official best practices guide
- [Apollo Schema Design Guide](https://www.apollographql.com/docs/apollo-server/schema/schema/)
  Schema design patterns
- [Relay Connection Specification](https://relay.dev/graphql/connections.htm) -
  Cursor-based pagination standard
- [GraphQL Schema Design Book](https://book.graphql.guide/) - In-depth
  schema design resource
