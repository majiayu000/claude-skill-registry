---
name: api-patterns
description: |
  REST API and GraphQL design patterns, authentication, error handling, and best practices.
  Use when building APIs, designing endpoints, or implementing backend services.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# API Design Patterns & Best Practices

## REST API Principles

### 1. Resource-Based URLs
```
# GOOD: Resource-oriented
GET    /users           # List users
GET    /users/123       # Get specific user
POST   /users           # Create user
PUT    /users/123       # Update user (full)
PATCH  /users/123       # Update user (partial)
DELETE /users/123       # Delete user

# BAD: Action-oriented
GET    /getUsers
POST   /createUser
POST   /updateUser/123
```

### 2. Use Proper HTTP Methods
- **GET**: Read (idempotent, cacheable)
- **POST**: Create (not idempotent)
- **PUT**: Replace (idempotent)
- **PATCH**: Partial update (not idempotent)
- **DELETE**: Remove (idempotent)

### 3. Use Proper HTTP Status Codes
```typescript
// Success
200 OK           // General success
201 Created      // Resource created (POST)
204 No Content   // Success with no body (DELETE)

// Client Errors
400 Bad Request  // Invalid input
401 Unauthorized // No/invalid auth
403 Forbidden    // Auth valid but not allowed
404 Not Found    // Resource doesn't exist
409 Conflict     // Resource state conflict
422 Unprocessable // Validation failed

// Server Errors
500 Internal     // Unexpected error
503 Unavailable  // Service temporarily down
```

## Response Format

### Standard Response Structure

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: {
    code: string
    message: string
    details?: Record<string, string[]>
  }
  meta?: {
    total: number
    page: number
    limit: number
    hasMore: boolean
  }
}

// Success response
{
  "success": true,
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  }
}

// List response with pagination
{
  "success": true,
  "data": [
    { "id": "1", "name": "User 1" },
    { "id": "2", "name": "User 2" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "hasMore": true
  }
}

// Error response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["Invalid email format"],
      "age": ["Must be at least 18"]
    }
  }
}
```

## Request Validation

### Zod Schema Validation

```typescript
import { z } from 'zod'

const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(18).max(150).optional(),
  role: z.enum(['user', 'admin']).default('user')
})

type CreateUserInput = z.infer<typeof CreateUserSchema>

// Usage in endpoint
export async function POST(request: Request) {
  try {
    const body = await request.json()
    const data = CreateUserSchema.parse(body)
    
    const user = await createUser(data)
    return Response.json({ success: true, data: user }, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return Response.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input',
          details: formatZodErrors(error)
        }
      }, { status: 422 })
    }
    throw error
  }
}
```

## Error Handling

### Custom Error Classes

```typescript
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR'
  ) {
    super(message)
    this.name = 'AppError'
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, 'NOT_FOUND')
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED')
  }
}

export class ValidationError extends AppError {
  constructor(
    message: string,
    public details?: Record<string, string[]>
  ) {
    super(message, 422, 'VALIDATION_ERROR')
  }
}

// Usage
throw new NotFoundError('User')
throw new UnauthorizedError('Invalid token')
throw new ValidationError('Invalid input', { email: ['Required'] })
```

### Global Error Handler

```typescript
// Express middleware
export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  console.error('Error:', error)

  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      success: false,
      error: {
        code: error.code,
        message: error.message,
        details: error instanceof ValidationError ? error.details : undefined
      }
    })
  }

  // Don't leak internal errors
  return res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  })
}
```

## Authentication Patterns

### JWT Authentication

```typescript
import jwt from 'jsonwebtoken'

const JWT_SECRET = process.env.JWT_SECRET!
const JWT_EXPIRES_IN = '7d'

export function generateToken(user: User): string {
  return jwt.sign(
    { userId: user.id, role: user.role },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRES_IN }
  )
}

export function verifyToken(token: string): JwtPayload {
  try {
    return jwt.verify(token, JWT_SECRET) as JwtPayload
  } catch {
    throw new UnauthorizedError('Invalid token')
  }
}

// Auth middleware
export async function authMiddleware(req: Request) {
  const authHeader = req.headers.get('authorization')
  
  if (!authHeader?.startsWith('Bearer ')) {
    throw new UnauthorizedError('Missing token')
  }

  const token = authHeader.slice(7)
  const payload = verifyToken(token)
  
  return payload
}
```

### API Key Authentication

```typescript
export async function apiKeyAuth(req: Request) {
  const apiKey = req.headers.get('x-api-key')
  
  if (!apiKey) {
    throw new UnauthorizedError('Missing API key')
  }

  const hashedKey = hashApiKey(apiKey)
  const keyRecord = await db.apiKeys.findUnique({
    where: { hashedKey }
  })

  if (!keyRecord || keyRecord.revokedAt) {
    throw new UnauthorizedError('Invalid API key')
  }

  // Update last used
  await db.apiKeys.update({
    where: { id: keyRecord.id },
    data: { lastUsedAt: new Date() }
  })

  return keyRecord
}
```

## Rate Limiting

### Token Bucket Implementation

```typescript
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(100, '1 m'), // 100 requests per minute
  analytics: true
})

export async function rateLimitMiddleware(req: Request) {
  const ip = req.headers.get('x-forwarded-for') ?? 'anonymous'
  const { success, limit, remaining, reset } = await ratelimit.limit(ip)

  if (!success) {
    return Response.json(
      {
        success: false,
        error: {
          code: 'RATE_LIMITED',
          message: 'Too many requests'
        }
      },
      {
        status: 429,
        headers: {
          'X-RateLimit-Limit': limit.toString(),
          'X-RateLimit-Remaining': remaining.toString(),
          'X-RateLimit-Reset': reset.toString()
        }
      }
    )
  }
}
```

## Pagination

### Cursor-Based (Recommended)

```typescript
interface PaginationParams {
  cursor?: string
  limit?: number
}

async function getUsers(params: PaginationParams) {
  const limit = Math.min(params.limit ?? 20, 100)
  
  const users = await db.users.findMany({
    take: limit + 1, // Fetch one extra to check hasMore
    cursor: params.cursor ? { id: params.cursor } : undefined,
    orderBy: { createdAt: 'desc' }
  })

  const hasMore = users.length > limit
  const data = hasMore ? users.slice(0, -1) : users
  const nextCursor = hasMore ? data[data.length - 1].id : null

  return {
    data,
    meta: {
      hasMore,
      nextCursor
    }
  }
}
```

### Offset-Based

```typescript
async function getUsers(page: number = 1, limit: number = 20) {
  const offset = (page - 1) * limit
  
  const [users, total] = await Promise.all([
    db.users.findMany({ skip: offset, take: limit }),
    db.users.count()
  ])

  return {
    data: users,
    meta: {
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit),
      hasMore: offset + users.length < total
    }
  }
}
```

## Versioning

### URL Versioning (Recommended)

```
/api/v1/users
/api/v2/users
```

### Header Versioning

```typescript
const version = req.headers.get('api-version') ?? 'v1'

switch (version) {
  case 'v1':
    return handleV1(req)
  case 'v2':
    return handleV2(req)
  default:
    throw new AppError('Unsupported API version', 400)
}
```

## CORS Configuration

```typescript
const corsHeaders = {
  'Access-Control-Allow-Origin': process.env.ALLOWED_ORIGINS ?? '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key',
  'Access-Control-Max-Age': '86400' // 24 hours
}

// Handle preflight
export function OPTIONS() {
  return new Response(null, { headers: corsHeaders })
}

// Add to responses
export function withCors(response: Response) {
  Object.entries(corsHeaders).forEach(([key, value]) => {
    response.headers.set(key, value)
  })
  return response
}
```

## Security Headers

```typescript
const securityHeaders = {
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'X-XSS-Protection': '1; mode=block',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
  'Content-Security-Policy': "default-src 'self'",
  'Referrer-Policy': 'strict-origin-when-cross-origin'
}
```

## OpenAPI Documentation

```typescript
/**
 * @openapi
 * /api/users:
 *   get:
 *     summary: List users
 *     tags: [Users]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *         description: Page number
 *     responses:
 *       200:
 *         description: List of users
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/UsersResponse'
 */
```

## GraphQL Patterns

### Schema Design

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

input CreateUserInput {
  name: String!
  email: String!
}
```

### Resolver Pattern

```typescript
const resolvers = {
  Query: {
    user: async (_, { id }, context) => {
      return context.dataSources.users.findById(id)
    },
    users: async (_, { first, after }, context) => {
      return context.dataSources.users.findMany({ first, after })
    }
  },
  User: {
    posts: async (user, _, context) => {
      return context.dataSources.posts.findByUserId(user.id)
    }
  }
}
```

## Checklist

- [ ] RESTful resource naming
- [ ] Proper HTTP methods and status codes
- [ ] Consistent response format
- [ ] Input validation (Zod)
- [ ] Error handling (custom errors)
- [ ] Authentication (JWT/API key)
- [ ] Rate limiting
- [ ] Pagination (cursor-based)
- [ ] CORS configured
- [ ] Security headers set
- [ ] API documentation (OpenAPI)
