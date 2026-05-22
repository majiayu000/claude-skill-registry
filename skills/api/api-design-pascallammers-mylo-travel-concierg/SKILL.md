---
name: api-design
description: Design clean, scalable, and maintainable REST and GraphQL APIs following industry best practices. Use when designing public or internal APIs, planning endpoint structures, defining request/response contracts, establishing versioning strategies, implementing authentication patterns, designing data models, creating API documentation, ensuring consistent error handling, optimizing for performance, or establishing service contracts between microservices.
---

# API Design - Building Clean, Scalable REST & GraphQL APIs

## When to use this skill

- Designing new REST or GraphQL APIs from scratch
- Planning endpoint structures and URL patterns
- Defining request/response contracts and data schemas
- Establishing API versioning and deprecation strategies
- Implementing authentication and authorization patterns
- Creating API documentation (OpenAPI/Swagger)
- Designing error response formats and status codes
- Planning pagination, filtering, and sorting strategies
- Establishing rate limiting and throttling policies
- Designing webhooks or event-driven integrations
- Creating service contracts for microservices
- Optimizing API performance and caching strategies

## When to use this skill

- Designing public or internal APIs, planning endpoints, defining contracts between services.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Designing public or internal APIs, planning endpoints, defining contracts between services.

## Core Principles

1. **Consistency** - Predictable patterns across endpoints
2. **Simplicity** - Easy to understand and use
3. **Versioning** - Support evolution without breaking clients
4. **Security** - Authentication, authorization, rate limiting
5. **Documentation** - Clear, up-to-date API specs

## REST API Design

### 1. **Resource-Based URLs**

```
✅ Good - Nouns, not verbs
GET    /users              - List users
GET    /users/:id          - Get specific user
POST   /users              - Create user
PUT    /users/:id          - Update user (full replace)
PATCH  /users/:id          - Update user (partial)
DELETE /users/:id          - Delete user

GET    /users/:id/posts    - Get user's posts
POST   /users/:id/posts    - Create post for user

❌ Bad - Verbs in URLs
GET    /getUsers
POST   /createUser
POST   /users/delete/:id
```

### 2. **HTTP Methods & Status Codes**

```typescript
// ✅ Proper HTTP method usage
app.get('/users', async (req, res) => {
  const users = await db.users.findAll();
  res.json(users); // 200 OK
});

app.post('/users', async (req, res) => {
  const user = await db.users.create(req.body);
  res.status(201) // 201 Created
     .location(`/users/${user.id}`)
     .json(user);
});

app.put('/users/:id', async (req, res) => {
  const user = await db.users.update(req.params.id, req.body);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user); // 200 OK
});

app.delete('/users/:id', async (req, res) => {
  await db.users.delete(req.params.id);
  res.status(204).send(); // 204 No Content
});

// ✅ Common status codes
// 2xx Success
200 OK                  - Request succeeded
201 Created             - Resource created
204 No Content          - Succeeded, no response body

// 4xx Client Errors
400 Bad Request         - Invalid input
401 Unauthorized        - Not authenticated
403 Forbidden           - Authenticated but no permission
404 Not Found           - Resource doesn't exist
409 Conflict            - Duplicate or conflicting state
422 Unprocessable       - Validation failed
429 Too Many Requests   - Rate limited

// 5xx Server Errors
500 Internal Error      - Something broke on server
503 Service Unavailable - Temporarily down
```

### 3. **Request/Response Format**

```typescript
// ✅ Consistent response structure
interface ApiResponse<T> {
  data: T;
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
  };
  links?: {
    self: string;
    next?: string;
    prev?: string;
  };
}

// Success response
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  }
}

// List response with pagination
{
  "data": [
    { "id": "1", "name": "User 1" },
    { "id": "2", "name": "User 2" }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  },
  "links": {
    "self": "/users?page=1",
    "next": "/users?page=2"
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {
        "field": "email",
        "message": "Must be valid email"
      }
    ]
  }
}
```

### 4. **Filtering, Sorting, Pagination**

```typescript
// ✅ Query parameters for filtering
GET /users?status=active&role=admin
GET /posts?author=john&tags=tech,programming
GET /products?minPrice=10&maxPrice=100

app.get('/users', async (req, res) => {
  const { status, role, page = 1, limit = 20, sort = 'createdAt' } = req.query;
  
  const query = {};
  if (status) query.status = status;
  if (role) query.role = role;
  
  const users = await db.users.findMany({
    where: query,
    skip: (page - 1) * limit,
    take: limit,
    orderBy: { [sort]: 'desc' }
  });
  
  const total = await db.users.count({ where: query });
  
  res.json({
    data: users,
    meta: { page, limit, total },
    links: {
      self: `/users?page=${page}`,
      next: page * limit < total ? `/users?page=${page + 1}` : null
    }
  });
});

// ✅ Sorting
GET /users?sort=name           - Sort by name ascending
GET /users?sort=-createdAt     - Sort by createdAt descending
GET /users?sort=role,-createdAt - Multiple sort fields

// ✅ Field selection (sparse fieldsets)
GET /users?fields=id,name,email - Only return specified fields
```

### 5. **Versioning**

```typescript
// ✅ URL versioning (most common)
GET /api/v1/users
GET /api/v2/users

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// ✅ Header versioning
GET /api/users
Headers: { "Accept-Version": "v2" }

// ✅ Deprecation warnings
app.use('/api/v1', (req, res, next) => {
  res.set('X-API-Deprecation', 'v1 will be deprecated on 2024-12-31');
  res.set('X-API-Upgrade', 'See /api/v2 for latest version');
  next();
});
```

### 6. **Authentication & Authorization**

```typescript
// ✅ Bearer token authentication
GET /api/users
Headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }

function authenticate(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
}

// ✅ Rate limiting
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100
});

app.use('/api/', limiter);

// ✅ API keys for service-to-service
GET /api/users
Headers: { "X-API-Key": "sk_live_abc123..." }

function requireApiKey(req, res, next) {
  const apiKey = req.get('X-API-Key');
  
  if (!isValidApiKey(apiKey)) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  
  next();
}
```

### 7. **HATEOAS (Hypermedia)**

```typescript
// ✅ Include related resource links
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "links": {
    "self": "/users/123",
    "posts": "/users/123/posts",
    "followers": "/users/123/followers"
  }
}

// ✅ Action links for state transitions
{
  "data": {
    "id": "456",
    "status": "pending",
    "amount": 100
  },
  "actions": {
    "approve": {
      "method": "POST",
      "href": "/orders/456/approve"
    },
    "cancel": {
      "method": "DELETE",
      "href": "/orders/456"
    }
  }
}
```

## GraphQL API Design

### 1. **Schema Definition**

```graphql
# ✅ Clear, typed schema
type User {
  id: ID!
  name: String!
  email: String!
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
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
  posts(authorId: ID, published: Boolean): [Post!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
  
  createPost(input: CreatePostInput!): Post!
  publishPost(id: ID!): Post!
}

input CreateUserInput {
  name: String!
  email: String!
}

input UpdateUserInput {
  name: String
  email: String
}

input CreatePostInput {
  title: String!
  content: String!
  authorId: ID!
}
```

### 2. **Resolvers**

```typescript
// ✅ Efficient resolvers with DataLoader
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (ids) => {
  const users = await db.users.findMany({
    where: { id: { in: ids } }
  });
  
  // Return in same order as input IDs
  return ids.map(id => users.find(u => u.id === id));
});

const resolvers = {
  Query: {
    user: async (_, { id }) => {
      return await userLoader.load(id);
    },
    
    users: async (_, { limit = 20, offset = 0 }) => {
      return await db.users.findMany({
        take: limit,
        skip: offset
      });
    }
  },
  
  Mutation: {
    createUser: async (_, { input }) => {
      return await db.users.create(input);
    },
    
    updateUser: async (_, { id, input }) => {
      return await db.users.update(id, input);
    }
  },
  
  User: {
    // Resolver for User.posts field
    posts: async (user) => {
      return await db.posts.findMany({
        where: { authorId: user.id }
      });
    }
  }
};
```

### 3. **Error Handling**

```typescript
// ✅ GraphQL error handling
import { GraphQLError } from 'graphql';

const resolvers = {
  Query: {
    user: async (_, { id }) => {
      const user = await db.users.findById(id);
      
      if (!user) {
        throw new GraphQLError('User not found', {
          extensions: {
            code: 'USER_NOT_FOUND',
            id
          }
        });
      }
      
      return user;
    }
  },
  
  Mutation: {
    createUser: async (_, { input }) => {
      try {
        return await db.users.create(input);
      } catch (error) {
        if (error.code === 'P2002') { // Unique constraint
          throw new GraphQLError('Email already exists', {
            extensions: {
              code: 'DUPLICATE_EMAIL',
              field: 'email'
            }
          });
        }
        throw error;
      }
    }
  }
};
```

## API Documentation

### 1. **OpenAPI/Swagger (REST)**

```typescript
// ✅ OpenAPI specification
/**
 * @swagger
 * /users:
 *   get:
 *     summary: List all users
 *     tags: [Users]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *         description: Page number
 *     responses:
 *       200:
 *         description: Success
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/User'
 */
app.get('/users', async (req, res) => {
  // Implementation
});

// components/schemas/User
/**
 * @swagger
 * components:
 *   schemas:
 *     User:
 *       type: object
 *       required:
 *         - id
 *         - email
 *       properties:
 *         id:
 *           type: string
 *           example: "123"
 *         name:
 *           type: string
 *           example: "John Doe"
 *         email:
 *           type: string
 *           format: email
 *           example: "john@example.com"
 */
```

### 2. **GraphQL Documentation**

```graphql
# ✅ Descriptions in schema (auto-documented)
"""
Represents a user in the system
"""
type User {
  """Unique identifier"""
  id: ID!
  
  """User's full name"""
  name: String!
  
  """User's email address"""
  email: String!
  
  """Posts authored by this user"""
  posts: [Post!]!
}

"""
Create a new user
"""
createUser(
  """User details"""
  input: CreateUserInput!
): User!
```

## API Best Practices

### 1. **Idempotency**

```typescript
// ✅ Idempotent operations (safe to retry)
app.put('/users/:id', async (req, res) => {
  // PUT is idempotent - same result on repeat
  const user = await db.users.upsert({
    where: { id: req.params.id },
    create: req.body,
    update: req.body
  });
  res.json(user);
});

// ✅ Idempotency keys for POST
app.post('/payments', async (req, res) => {
  const idempotencyKey = req.get('Idempotency-Key');
  
  if (!idempotencyKey) {
    return res.status(400).json({ error: 'Idempotency-Key required' });
  }
  
  // Check if already processed
  const existing = await cache.get(`payment:${idempotencyKey}`);
  if (existing) {
    return res.json(existing); // Return cached result
  }
  
  const payment = await processPayment(req.body);
  await cache.set(`payment:${idempotencyKey}`, payment, 24 * 60 * 60);
  
  res.status(201).json(payment);
});
```

### 2. **Caching**

```typescript
// ✅ HTTP caching headers
app.get('/products/:id', async (req, res) => {
  const product = await db.products.findById(req.params.id);
  
  // Generate ETag from content
  const etag = generateETag(product);
  
  // Check if client has current version
  if (req.get('If-None-Match') === etag) {
    return res.status(304).send(); // Not Modified
  }
  
  res.set({
    'ETag': etag,
    'Cache-Control': 'public, max-age=300', // 5 minutes
    'Last-Modified': product.updatedAt.toUTCString()
  });
  
  res.json(product);
});
```

### 3. **Webhooks**

```typescript
// ✅ Webhook system for async events
interface WebhookPayload {
  event: string;
  data: any;
  timestamp: string;
  signature: string; // HMAC for verification
}

async function sendWebhook(url: string, event: string, data: any) {
  const payload = {
    event,
    data,
    timestamp: new Date().toISOString()
  };
  
  // Sign payload
  const signature = crypto
    .createHmac('sha256', process.env.WEBHOOK_SECRET)
    .update(JSON.stringify(payload))
    .digest('hex');
  
  await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Webhook-Signature': signature
    },
    body: JSON.stringify({ ...payload, signature })
  });
}

// Trigger webhooks on events
app.post('/users', async (req, res) => {
  const user = await db.users.create(req.body);
  
  // Send webhook asynchronously
  sendWebhook(
    'https://customer.com/webhooks',
    'user.created',
    user
  ).catch(console.error);
  
  res.status(201).json(user);
});
```

## API Design Checklist

```
REST:
□ Resource-based URLs (nouns, not verbs)
□ Proper HTTP methods and status codes
□ Consistent response format
□ Pagination for lists
□ Filtering, sorting, field selection
□ API versioning strategy
□ Authentication (Bearer tokens, API keys)
□ Rate limiting configured
□ CORS properly configured
□ Error responses standardized

GraphQL:
□ Clear, typed schema
□ Efficient resolvers (DataLoader)
□ Pagination implemented (cursor or offset)
□ Error handling with codes
□ Authentication & authorization
□ Query complexity limits
□ Depth limiting
□ Introspection disabled in production

Documentation:
□ OpenAPI/GraphQL schema published
□ Example requests/responses
□ Authentication docs
□ Error codes documented
□ Changelog maintained
□ Migration guides for breaking changes

Performance:
□ Database queries optimized
□ N+1 queries eliminated
□ Response caching
□ Compression enabled (gzip)
□ CDN for static responses

Security:
□ Input validation on all endpoints
□ SQL injection prevention
□ Rate limiting per endpoint
□ API key rotation supported
□ Audit logging for sensitive operations
```

## Resources

- [REST API Tutorial](https://restfulapi.net/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [API Design Patterns](https://cloud.google.com/apis/design)

---

**Remember**: Great APIs are predictable, well-documented, and easy to use. Design for your API consumers, not just your implementation.
