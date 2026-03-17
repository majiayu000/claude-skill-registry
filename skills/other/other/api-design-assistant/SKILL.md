---
name: api-design-assistant
description: Design and review APIs with suggestions for endpoints, parameters, return types, and best practices. Use when designing new APIs from requirements, reviewing existing API designs, generating API documentation, or getting implementation guidance. Supports REST APIs with focus on endpoint structure, request/response schemas, authentication, pagination, filtering, versioning, and OpenAPI specifications. Triggers when users ask to design, review, document, or improve APIs.
---

# API Design Assistant

## Overview

Assist with designing well-structured, RESTful APIs by suggesting endpoints, parameters, return types, and best practices. Generate OpenAPI specifications and provide implementation guidance.

## Workflow

### 1. Understand Requirements

When designing a new API or reviewing an existing one, first understand:

**For new API design:**
- What is the domain/purpose of the API?
- What resources need to be exposed? (users, products, orders, etc.)
- What operations are needed? (create, read, update, delete, custom actions)
- Who are the consumers? (web app, mobile app, third-party integrations)
- Are there specific requirements? (authentication, rate limiting, versioning)

**For API review:**
- What are the existing endpoints?
- What issues or improvements are needed?
- Are there consistency problems?
- Are best practices being followed?

### 2. Design or Review API Structure

Follow these steps based on the use case:

#### Designing New APIs

**Step 1: Identify Resources**

Map domain concepts to API resources:
- User management → `/users`
- Product catalog → `/products`
- Order processing → `/orders`
- User's orders → `/users/{userId}/orders`

**Step 2: Define Endpoints**

For each resource, determine needed operations:

```
# Users resource
GET    /users              # List users
POST   /users              # Create user
GET    /users/{id}         # Get specific user
PUT    /users/{id}         # Replace user
PATCH  /users/{id}         # Update user
DELETE /users/{id}         # Delete user

# Nested resources
GET    /users/{id}/orders  # Get user's orders
POST   /users/{id}/orders  # Create order for user

# Actions
POST   /users/{id}/activate      # Activate user
POST   /orders/{id}/cancel       # Cancel order
```

**Step 3: Design Request/Response Schemas**

Define what data each endpoint expects and returns. See [best-practices.md](references/best-practices.md) for detailed examples.

**Step 4: Add Supporting Features**

- Authentication (Bearer tokens, API keys)
- Pagination (page-based, cursor-based)
- Filtering and sorting
- Error handling
- Versioning strategy

**Step 5: Generate OpenAPI Specification**

Create formal API documentation. See [openapi-template.md](references/openapi-template.md) for complete templates.

#### Reviewing Existing APIs

**Step 1: Analyze Consistency**

Check for:
- Consistent naming conventions
- Consistent use of HTTP methods
- Consistent response formats
- Consistent error handling

**Step 2: Identify Issues**

Common problems:
- Verbs in URLs (e.g., `/getUsers` instead of `GET /users`)
- Wrong HTTP methods (e.g., GET for mutations)
- Inconsistent naming (e.g., `/user` vs `/users`)
- Missing pagination on collections
- Inadequate error responses
- No versioning strategy

**Step 3: Suggest Improvements**

Provide specific recommendations:
- "Change `/getUsers` to `GET /users`"
- "Add pagination to `GET /users` endpoint"
- "Standardize error response format across all endpoints"
- "Use PATCH instead of PUT for partial updates"

**Step 4: Propose Migration Path**

If breaking changes are needed:
- Version the API (`/v2/users`)
- Provide deprecation timeline
- Suggest backward compatibility approaches

### 3. Apply Best Practices

Consult [best-practices.md](references/best-practices.md) for detailed guidance on:

- **Resource naming**: Plural nouns, lowercase, hyphens
- **HTTP methods**: Correct usage of GET, POST, PUT, PATCH, DELETE
- **Status codes**: When to use 200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500
- **Authentication**: Bearer tokens, API keys, OAuth2
- **Pagination**: Offset, page-based, cursor-based
- **Filtering & sorting**: Query parameter patterns
- **Versioning**: URL, header, or query parameter approaches
- **Error handling**: Consistent error response formats
- **Rate limiting**: Header-based communication

### 4. Generate Documentation

Depending on user needs, provide:

#### Markdown Documentation

```markdown
## POST /users

Create a new user account.

### Request

**Headers:**
- `Content-Type: application/json`
- `Authorization: Bearer <token>`

**Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user"
}
```

### Response

**Success (201 Created):**
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error (400 Bad Request):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ]
  }
}
```
```

#### OpenAPI 3.0 Specification

Generate formal OpenAPI specs using templates from [openapi-template.md](references/openapi-template.md).

#### Implementation Hints

Provide language/framework-specific guidance when requested:

**Example for Express.js:**
```javascript
// POST /users
app.post('/users', async (req, res) => {
  try {
    const { name, email, role } = req.body;

    // Validation
    if (!name || !email) {
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Name and email are required'
        }
      });
    }

    // Create user
    const user = await User.create({ name, email, role });

    res.status(201)
      .location(`/users/${user.id}`)
      .json(user);
  } catch (error) {
    res.status(500).json({
      error: {
        code: 'INTERNAL_ERROR',
        message: 'Failed to create user'
      }
    });
  }
});
```

### 5. Handle Common Scenarios

#### Pagination

Recommend appropriate pagination strategy:
- **Small datasets**: Offset or page-based
- **Large datasets**: Cursor-based
- **Real-time data**: Cursor-based with timestamps

#### Authentication

Suggest authentication approach:
- **Public API**: API keys
- **Web/mobile apps**: JWT tokens
- **Third-party integrations**: OAuth2
- **Internal services**: mTLS or service tokens

#### Versioning

Recommend when to version:
- Breaking changes to existing endpoints
- Removing fields from responses
- Changing data types
- Changing endpoint URLs

Don't version for:
- Adding new endpoints
- Adding optional fields to responses
- Adding optional parameters

#### Filtering Complex Data

Design filtering for different data types:

**Exact match:**
```
GET /users?status=active&role=admin
```

**Range queries:**
```
GET /products?price_min=10&price_max=100
GET /events?start_date=2024-01-01&end_date=2024-12-31
```

**Pattern matching:**
```
GET /users?name_contains=john
GET /products?search=laptop
```

**Multiple values:**
```
GET /users?status=active,pending
GET /products?category=electronics,computers
```

## Example Workflows

### Example 1: Design API from Requirements

**User request:**
> "Design an API for a blog platform. Users should be able to create posts, comment on posts, and like posts."

**Response approach:**

1. **Identify resources:** Users, Posts, Comments, Likes
2. **Design endpoints:**
   ```
   # Posts
   GET    /posts
   POST   /posts
   GET    /posts/{postId}
   PUT    /posts/{postId}
   DELETE /posts/{postId}

   # Comments on posts
   GET    /posts/{postId}/comments
   POST   /posts/{postId}/comments
   DELETE /posts/{postId}/comments/{commentId}

   # Likes on posts
   POST   /posts/{postId}/likes
   DELETE /posts/{postId}/likes
   GET    /posts/{postId}/likes
   ```

3. **Define schemas:**
   ```json
   // Post
   {
     "id": 123,
     "title": "My Post",
     "content": "Post content...",
     "author_id": 456,
     "created_at": "2024-01-15T10:30:00Z",
     "likes_count": 10,
     "comments_count": 5
   }
   ```

4. **Add features:** Pagination for posts/comments, filtering by author, sorting by date/popularity

5. **Generate OpenAPI spec** if requested

### Example 2: Review Existing API

**User request:**
> "Review this API design: `GET /getUserById?id=123`, `POST /createUser`, `POST /updateUser`"

**Response approach:**

1. **Identify issues:**
   - Using verbs in URLs
   - Using GET with query param instead of path param
   - Not using proper HTTP methods for updates

2. **Suggest improvements:**
   ```
   # Before
   GET  /getUserById?id=123
   POST /createUser
   POST /updateUser

   # After
   GET   /users/{id}
   POST  /users
   PUT   /users/{id}    # Full replacement
   PATCH /users/{id}    # Partial update
   ```

3. **Explain benefits:**
   - RESTful resource naming
   - Proper HTTP method semantics
   - Cleaner, more intuitive URLs
   - Better caching support

### Example 3: Generate Documentation

**User request:**
> "Generate OpenAPI documentation for a user management API"

**Response approach:**

1. Use templates from [openapi-template.md](references/openapi-template.md)
2. Define info, servers, paths, schemas
3. Include authentication schemes
4. Add examples for requests/responses
5. Output complete YAML specification

## Tips for Effective API Design

**Start with resources, not actions:**
- Think "What resources exist?" not "What actions can be performed?"
- Resources are nouns (users, products), actions are HTTP methods

**Be consistent:**
- Use same naming conventions throughout
- Use same error format for all endpoints
- Use same pagination approach across collections

**Think about the consumer:**
- What data do they need? Don't over-fetch or under-fetch
- What queries will be common? Support them with filters
- What's the expected load? Design pagination accordingly

**Plan for evolution:**
- Add versioning from the start
- Make fields optional when possible
- Don't break existing clients unnecessarily

**Document early:**
- Generate OpenAPI specs during design
- Keep documentation in sync with implementation
- Provide clear examples

**Validate thoroughly:**
- Check all inputs
- Return meaningful error messages
- Use appropriate status codes

## References

For detailed information, consult these references:

- **[best-practices.md](references/best-practices.md)**: Comprehensive REST API best practices including naming, HTTP methods, status codes, authentication, pagination, filtering, and common mistakes
- **[openapi-template.md](references/openapi-template.md)**: Complete OpenAPI 3.0 specification templates with examples for all common patterns
