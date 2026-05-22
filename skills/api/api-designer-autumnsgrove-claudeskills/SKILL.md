---
name: api-designer
description: "Design and document RESTful and GraphQL APIs with OpenAPI/Swagger specifications, authentication patterns, versioning strategies, and best practices. Use for: (1) Creating API specifications, (2) Designing REST endpoints, (3) GraphQL schema design, (4) API authentication and authorization, (5) API versioning strategies, (6) Documentation generation"
---

# API Designer

## Overview

This skill provides comprehensive guidance for designing, documenting, and implementing modern APIs. It covers both REST and GraphQL paradigms, with emphasis on industry best practices, clear documentation, and maintainable architecture. Use this skill to create production-ready API designs that are scalable, secure, and developer-friendly.

## Core Capabilities

### REST API Design
- Resource-oriented endpoint design with proper URL structure
- HTTP method semantics and status code usage
- Request/response payload design with consistent naming
- Pagination, filtering, and sorting strategies
- Error handling and validation patterns

### GraphQL API Design
- Schema definition with type system and relationships
- Query and mutation design with proper input types
- Resolver patterns and performance optimization
- Fragment usage and directive implementation
- N+1 problem prevention strategies

### API Documentation
- OpenAPI 3.0 specification generation
- Interactive documentation with Swagger UI
- Authentication and authorization documentation
- Example requests/responses with multiple scenarios
- Code generation from specifications

### Authentication & Authorization
- OAuth 2.0 flows (authorization code, client credentials, PKCE)
- JWT token design, validation, and rotation
- API key management and rotation strategies
- Role-based access control (RBAC) implementation
- Rate limiting and throttling patterns

### API Versioning
- URL versioning and header-based versioning strategies
- Semantic versioning for API releases
- Deprecation planning and communication
- Backward compatibility maintenance
- Migration path design

## When to Use This Skill

Use this skill when:
- Designing a new API from scratch or refactoring existing endpoints
- Creating OpenAPI/Swagger specifications for documentation
- Implementing authentication and authorization flows
- Planning API versioning and deprecation strategies
- Designing GraphQL schemas and resolvers
- Establishing API governance and best practices

## REST API Design Workflow

### Step 1: Identify Resources

Identify core resources (nouns) your API will expose:

```
Resources: Users, Posts, Comments

Collections:
- GET    /users              (List all users)
- POST   /users              (Create new user)

Individual Resources:
- GET    /users/{id}         (Get specific user)
- PUT    /users/{id}         (Replace user - full update)
- PATCH  /users/{id}         (Update user - partial)
- DELETE /users/{id}         (Delete user)

Nested Resources:
- GET    /users/{id}/posts   (Get user's posts)
- POST   /users/{id}/posts   (Create post for user)
```

### Step 2: Design URL Structure

Follow RESTful naming conventions:

**Best Practices**:
- Use plural nouns: `/users`, `/posts` (not `/user`, `/post`)
- Use hyphens for multi-word: `/blog-posts` (not `/blogPosts` or `/blog_posts`)
- Keep URLs lowercase
- Limit nesting to 2 levels maximum
- Use query parameters for filtering: `/posts?status=published&author=123`

**Quick Examples**:
```
✅ Good:
GET /users
GET /users/123/posts
GET /posts?published=true&limit=10

❌ Bad:
GET /getUsers
GET /users/123/posts/comments/likes  (too deep nesting)
GET /posts/published  (use query param instead)
```

### Step 3: Choose HTTP Methods

Map operations to standard HTTP methods:

- **GET**: Retrieve resource(s) - Safe, idempotent, cacheable
- **POST**: Create new resource - Returns 201 Created with Location header
- **PUT**: Replace entire resource - Idempotent, full replacement
- **PATCH**: Partial update - Update specific fields only
- **DELETE**: Remove resource - Idempotent, returns 204 or 200

### Step 4: Design Request/Response Payloads

Structure JSON payloads consistently:

**Naming Conventions**:
- Use camelCase for JSON field names
- Use ISO 8601 for timestamps (UTC)
- Use consistent ID formats with prefixes: `usr_`, `post_`
- Include metadata: `createdAt`, `updatedAt`

**Example Response**:
```json
{
  "id": "usr_1234567890",
  "username": "johndoe",
  "email": "john@example.com",
  "profile": {
    "firstName": "John",
    "lastName": "Doe"
  },
  "createdAt": "2025-10-25T10:30:00Z",
  "updatedAt": "2025-10-25T10:30:00Z"
}
```

### Step 5: Implement Error Handling

Design comprehensive error responses:

**Error Response Format**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ],
    "requestId": "req_abc123xyz",
    "timestamp": "2025-10-25T10:30:00Z"
  }
}
```

**Key Status Codes**:
- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing/invalid authentication
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource doesn't exist
- `422 Unprocessable Entity`: Validation errors
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Step 6: Add Pagination and Filtering

**Cursor-Based Pagination** (recommended for large datasets):
```
GET /posts?limit=20&cursor=eyJpZCI6MTIzfQ

Response:
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ",
    "hasMore": true
  }
}
```

**Offset-Based Pagination** (simpler for small datasets):
```
GET /posts?limit=20&offset=40&sort=-createdAt

Response:
{
  "data": [...],
  "pagination": {
    "total": 500,
    "limit": 20,
    "offset": 40
  }
}
```

For detailed pagination strategies and filtering patterns, see `references/rest_best_practices.md`.

## GraphQL API Design Workflow

### Step 1: Define Schema Types

Create type definitions for your domain:

```graphql
type User {
  id: ID!
  username: String!
  email: String!
  profile: Profile
  posts(limit: Int = 10): [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  published: Boolean!
  author: User!
  tags: [String!]!
  createdAt: DateTime!
}
```

### Step 2: Design Queries

Define read operations with filtering:

```graphql
type Query {
  user(id: ID!): User
  post(id: ID!): Post

  users(
    limit: Int = 10
    offset: Int = 0
    search: String
  ): UserConnection!

  posts(
    limit: Int = 10
    published: Boolean
    authorId: ID
    tags: [String!]
  ): PostConnection!
}
```

### Step 3: Design Mutations

Define write operations with input types and error handling:

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  createPost(input: CreatePostInput!): CreatePostPayload!
}

input CreateUserInput {
  username: String!
  email: String!
  password: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}
```

For complete GraphQL schema examples, see `examples/graphql_schema.graphql`.

## Authentication Patterns

### OAuth 2.0 Quick Reference

**Authorization Code Flow** (web apps with backend):
```
1. Redirect to /oauth/authorize with client_id, redirect_uri, scope
2. User authenticates and grants permission
3. Receive authorization code via redirect
4. Exchange code for access token at /oauth/token
5. Use access token in Authorization header
```

**Client Credentials Flow** (service-to-service):
```
POST /oauth/token
{
  "grant_type": "client_credentials",
  "client_id": "CLIENT_ID",
  "client_secret": "SECRET"
}
```

**PKCE Flow** (mobile/SPA - most secure for public clients):
```
1. Generate code_verifier and code_challenge
2. Request authorization with code_challenge
3. Exchange code for token with code_verifier (no client_secret needed)
```

### JWT Token Design

**Token Structure**:
```json
{
  "header": { "alg": "RS256", "typ": "JWT" },
  "payload": {
    "sub": "usr_1234567890",
    "iat": 1698336000,
    "exp": 1698339600,
    "scope": ["read:posts", "write:posts"],
    "roles": ["user", "editor"]
  }
}
```

**Usage**:
```http
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### API Key Authentication

```http
X-API-Key: sk_live_abcdef1234567890
```

**Best Practices**:
- Different keys for different environments (dev, staging, prod)
- Support multiple keys per account for rotation
- Implement key expiration and usage logging
- Never expose keys in client-side code

For comprehensive authentication patterns including refresh tokens, MFA, and security best practices, see `references/authentication.md`.

## API Versioning Strategies

### URL Versioning (Recommended)

```
/v1/users
/v2/users
```

**Pros**: Clear, explicit, easy to cache and route
**Cons**: URL proliferation, multiple codebases

### Header Versioning

```http
Accept: application/vnd.myapi.v2+json
API-Version: 2
```

**Pros**: Clean URLs, same endpoint
**Cons**: Less visible, harder to test in browser

### When to Version

**Create new version for**:
- Removing endpoints or fields
- Changing field types or names
- Modifying authentication methods
- Breaking existing client contracts

**Don't version for**:
- Adding new optional fields
- Adding new endpoints
- Bug fixes or performance improvements

For detailed versioning strategies, deprecation processes, and migration patterns, see `references/versioning-strategies.md`.

## OpenAPI Specification

### Basic Structure

```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
  description: API description

servers:
  - url: https://api.example.com/v1

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

components:
  schemas:
    User:
      type: object
      required:
        - username
        - email
      properties:
        id:
          type: string
        username:
          type: string
        email:
          type: string
          format: email
```

For complete OpenAPI specification examples, see `examples/openapi_spec.yaml`.

### Generating Documentation

Use the helper script to generate and validate specs:

```bash
# Generate OpenAPI spec from code
python scripts/api_helper.py generate --input api.py --output openapi.yaml

# Validate existing spec
python scripts/api_helper.py validate --spec openapi.yaml

# Generate documentation site
python scripts/api_helper.py docs --spec openapi.yaml --output docs/
```

## Best Practices Summary

### Consistency
- Use consistent naming conventions across all endpoints
- Standardize error response format
- Apply same authentication pattern everywhere
- Use uniform timestamp format (ISO 8601 with UTC)

### Security
- Always use HTTPS in production
- Validate all input data thoroughly
- Implement rate limiting per user/key/IP
- Use proper authentication for all endpoints
- Never expose sensitive data in URLs or logs
- Implement proper CORS configuration

### Performance
- Use pagination for large datasets
- Implement caching headers (ETag, Cache-Control)
- Support compression (gzip)
- Use cursor-based pagination for real-time data
- Implement field selection for sparse fieldsets

### Documentation
- Document all endpoints with OpenAPI
- Provide example requests and responses
- Document error codes and meanings
- Include authentication instructions
- Keep documentation in sync with code

### Maintainability
- Version APIs appropriately with clear deprecation timelines
- Provide deprecation warnings before removing features
- Write integration tests for all endpoints
- Monitor API usage, errors, and performance
- Maintain backward compatibility when possible

## Common Patterns

### Health Check
```http
GET /health
Response: { "status": "ok", "timestamp": "2025-10-25T10:30:00Z" }
```

### Batch Operations
```http
POST /users/batch
{
  "operations": [
    { "method": "POST", "path": "/users", "body": {...} },
    { "method": "PATCH", "path": "/users/123", "body": {...} }
  ]
}
```

### Webhooks
```http
POST /webhooks/configure
{
  "url": "https://your-app.com/webhook",
  "events": ["user.created", "post.published"],
  "secret": "webhook_secret_key"
}
```

For additional patterns including idempotency, long-running operations, file uploads, and soft deletes, see `references/common-patterns.md`.

## Quick Reference Checklists

### REST Endpoint Design
- [ ] Use plural nouns for collections
- [ ] Limit URL nesting to 2 levels
- [ ] Use appropriate HTTP methods
- [ ] Return correct status codes
- [ ] Implement consistent error format
- [ ] Add pagination for collections
- [ ] Include filtering and sorting
- [ ] Document with OpenAPI
- [ ] Implement authentication
- [ ] Add rate limiting

### GraphQL Schema Design
- [ ] Define clear type hierarchy
- [ ] Use nullable types appropriately
- [ ] Implement pagination (connections)
- [ ] Design mutations with input types
- [ ] Return errors in payload
- [ ] Document schema with descriptions
- [ ] Implement authentication/authorization
- [ ] Optimize for N+1 queries (DataLoader)

## Additional Resources

### Comprehensive References
- `references/rest_best_practices.md` - Complete REST API patterns, status codes, and implementation details
- `references/authentication.md` - OAuth 2.0, JWT, API keys, MFA, and security best practices
- `references/versioning-strategies.md` - Versioning approaches, deprecation, and migration strategies
- `references/common-patterns.md` - Health checks, webhooks, batch operations, and more

### Examples
- `examples/openapi_spec.yaml` - Complete OpenAPI 3.0 specification for a blog API
- `examples/graphql_schema.graphql` - Full GraphQL schema with queries, mutations, and subscriptions

### Tools
- `scripts/api_helper.py` - API specification generation, validation, and documentation utilities
