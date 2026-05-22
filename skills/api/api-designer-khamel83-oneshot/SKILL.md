---
name: api-designer
description: "Design RESTful or GraphQL APIs with proper conventions. Creates endpoint specifications, request/response schemas, and documentation. Use when user says 'design API', 'endpoints', 'REST', 'GraphQL', or 'API spec'."
allowed-tools: Read, Write, Edit
---

# API Designer

You are an expert at designing clean REST and GraphQL APIs.

## When To Use

- User says "Design the API", "What endpoints do we need?"
- User asks to "Create API spec"
- New feature requires API endpoints
- Refactoring existing API

## Inputs

- Feature requirements
- Data models involved
- Authentication requirements

## Outputs

- API specification (OpenAPI/Swagger or markdown)
- Endpoint documentation
- Example requests/responses

## REST Conventions

| Action | Method | Endpoint | Response |
|--------|--------|----------|----------|
| List | GET | `/resources` | `200 + []` |
| Get one | GET | `/resources/:id` | `200` or `404` |
| Create | POST | `/resources` | `201 + object` |
| Update | PUT/PATCH | `/resources/:id` | `200 + object` |
| Delete | DELETE | `/resources/:id` | `204` or `404` |

## Workflow

### 1. Identify Resources

What entities does this feature involve?

### 2. Define Operations

CRUD? Custom actions?

### 3. Design URLs

- Use nouns, not verbs
- Nest appropriately
- Plural for collections

### 4. Define Request/Response

- Fields, types
- Required vs optional
- Pagination for lists

### 5. Error Handling

Standard error format, appropriate status codes.

### 6. Document

OpenAPI spec or markdown.

## URL Design

### Good

```
GET    /users
GET    /users/123
POST   /users
PUT    /users/123
DELETE /users/123

GET    /users/123/posts
POST   /users/123/posts
```

### Bad

```
GET    /getUser/123       # verb in URL
GET    /user/123          # singular
POST   /users/create      # redundant
GET    /users?action=delete  # wrong method
```

## Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ]
  }
}
```

## Status Codes

| Code | When |
|------|------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (deleted) |
| 400 | Bad Request (validation) |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (no permission) |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Server Error |

## Pagination

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

Or cursor-based:
```json
{
  "data": [...],
  "next_cursor": "abc123",
  "has_more": true
}
```

## OpenAPI Spec Template

```yaml
openapi: 3.0.0
info:
  title: API Name
  version: 1.0.0

paths:
  /resources:
    get:
      summary: List resources
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Resource'

components:
  schemas:
    Resource:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
```

---

## GraphQL

### When to Use GraphQL vs REST

| Use GraphQL | Use REST |
|-------------|----------|
| Complex data relationships | Simple CRUD |
| Mobile apps (reduce over-fetching) | Caching critical |
| Multiple clients need different data | Simpler tooling |
| Nested data in single request | File uploads |

### Schema Design

```graphql
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
  author: User!
  published: Boolean!
}

type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
  post(id: ID!): Post
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

input CreateUserInput {
  email: String!
  name: String
}

input UpdateUserInput {
  email: String
  name: String
}
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Types | PascalCase | `User`, `BlogPost` |
| Fields | camelCase | `createdAt`, `firstName` |
| Queries | camelCase, noun | `user`, `users`, `post` |
| Mutations | camelCase, verb+noun | `createUser`, `updatePost` |
| Inputs | PascalCase + Input | `CreateUserInput` |

### Pagination (Relay-style)

```graphql
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

# Query
query {
  users(first: 10, after: "cursor123") {
    edges {
      node { id name }
      cursor
    }
    pageInfo { hasNextPage endCursor }
  }
}
```

### Error Handling

```graphql
type MutationResult {
  success: Boolean!
  message: String
  errors: [FieldError!]
}

type FieldError {
  field: String!
  message: String!
}

# Or use union types
union CreateUserResult = User | ValidationError | AuthError
```

### Resolvers (Code-first with Python)

```python
from ariadne import QueryType, MutationType

query = QueryType()
mutation = MutationType()

@query.field("user")
def resolve_user(_, info, id):
    return db.get_user(id)

@query.field("users")
def resolve_users(_, info, first=10, after=None):
    return db.paginate_users(first, after)

@mutation.field("createUser")
def resolve_create_user(_, info, input):
    return db.create_user(**input)
```

### N+1 Problem (Use DataLoaders)

```python
from ariadne import load_schema_from_path
from graphql import GraphQLResolveInfo

# BAD: N+1 queries
@query.field("users")
def resolve_users(_, info):
    users = db.get_users()
    for user in users:
        user.posts = db.get_posts_for_user(user.id)  # N queries!
    return users

# GOOD: DataLoader
from aiodataloader import DataLoader

async def batch_load_posts(user_ids):
    posts = await db.get_posts_for_users(user_ids)
    return [posts.get(uid, []) for uid in user_ids]

posts_loader = DataLoader(batch_load_posts)

@query.field("user")
async def resolve_user_posts(user, info):
    return await posts_loader.load(user.id)
```

### GraphQL Anti-Patterns

- Deeply nested queries without limits
- No query complexity limits (DoS risk)
- Exposing database IDs directly
- Not using input types for mutations
- Returning null for errors instead of error types

---

## REST vs GraphQL Decision

| Factor | REST | GraphQL |
|--------|------|---------|
| Learning curve | Lower | Higher |
| Caching | Built-in HTTP | Manual |
| Over-fetching | Common | Solved |
| Under-fetching | Common | Solved |
| File uploads | Native | Needs workaround |
| Real-time | WebSocket separate | Subscriptions built-in |

**Default to REST** unless you have specific GraphQL needs.

---

## Anti-Patterns

- Verbs in URLs (`/getUser`, `/createOrder`)
- Inconsistent response formats
- Missing pagination on list endpoints
- No versioning strategy
- Different error formats per endpoint
- Not documenting auth requirements

## Keywords

API, REST, endpoints, design API, OpenAPI, Swagger, routes, GraphQL, schema, query, mutation
