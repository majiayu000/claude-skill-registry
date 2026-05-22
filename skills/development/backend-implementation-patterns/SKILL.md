---
name: backend-implementation-patterns
description: Production-ready backend API implementation patterns including REST, GraphQL, authentication, error handling, and data validation
license: MIT
metadata:
  adapted-by: ai-skills
  category: backend-development
---

# Backend Implementation Patterns

Production-ready patterns for building robust, scalable backend APIs.

## API Design Patterns

### RESTful Endpoints

```typescript
// Resource-based routing
app.get('/api/users', getUsers);           // List
app.get('/api/users/:id', getUserById);    // Get
app.post('/api/users', createUser);        // Create
app.put('/api/users/:id', updateUser);     // Update
app.delete('/api/users/:id', deleteUser);  // Delete

// Nested resources
app.get('/api/users/:id/posts', getUserPosts);
app.post('/api/users/:id/posts', createUserPost);
```

### Request/Response Pattern

```typescript
interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
  };
}

async function handleRequest<T>(
  handler: () => Promise<T>
): Promise<APIResponse<T>> {
  try {
    const data = await handler();
    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      error: {
        code: error.code || 'INTERNAL_ERROR',
        message: error.message,
      }
    };
  }
}
```

### Validation Layer

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().min(18).optional(),
});

app.post('/api/users', async (req, res) => {
  const validation = CreateUserSchema.safeParse(req.body);
  
  if (!validation.success) {
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid request data',
        details: validation.error.errors
      }
    });
  }
  
  const user = await userService.create(validation.data);
  res.status(201).json({ success: true, data: user });
});
```

## Authentication Patterns

### JWT Authentication

```typescript
import jwt from 'jsonwebtoken';

// Generate token
function generateToken(userId: string) {
  return jwt.sign(
    { userId },
    process.env.JWT_SECRET!, // allow-secret
    { expiresIn: '7d' }
  );
}

// Middleware
async function authenticateToken(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];  // allow-secret
  
  if (!token) {
    return res.status(401).json({
      success: false,
      error: { code: 'UNAUTHORIZED', message: 'Missing token' }
    });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!); // allow-secret
    req.userId = decoded.userId;
    next();
  } catch (error) {
    return res.status(401).json({
      success: false,
      error: { code: 'INVALID_TOKEN', message: 'Invalid or expired token' }
    });
  }
}
```

## Error Handling

### Custom Error Classes

```typescript
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, 'NOT_FOUND', `${resource} not found`);
  }
}

class ValidationError extends AppError {
  constructor(details: any) {
    super(400, 'VALIDATION_ERROR', 'Validation failed', details);
  }
}
```

### Error Handling Middleware

```typescript
app.use((error, req, res, next) => {
  console.error('Error:', error);
  
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      success: false,
      error: {
        code: error.code,
        message: error.message,
        details: error.details
      }
    });
  }
  
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  });
});
```

## Data Access Layer

### Repository Pattern

```typescript
interface Repository<T> {
  find Find(filters: any): Promise<T[]>;
  findById(id: string): Promise<T | null>;
  create(data: Partial<T>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

class UserRepository implements Repository<User> {
  async findById(id: string): Promise<User | null> {
    return db.user.findUnique({ where: { id } });
  }
  
  async create(data: Partial<User>): Promise<User> {
    return db.user.create({ data });
  }
  
  // ... other methods
}
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: { success: false, error: { code: 'RATE_LIMIT', message: 'Too many requests' }}
});

app.use('/api/', limiter);
```

## Integration Points

Complements:
- **api-design-patterns**: For API structure
- **postgres-advanced-patterns**: For data layer
- **security-implementation-guide**: For security
- **tdd-workflow**: For testing

---

## Related Skills

### Complementary Skills (Use Together)
- **[api-design-patterns](../api-design-patterns/)** - Design your API structure before implementing
- **[postgres-advanced-patterns](../postgres-advanced-patterns/)** - Advanced database patterns for the data layer
- **[testing-patterns](../testing-patterns/)** - Write tests for your API endpoints
- **[deployment-cicd](../deployment-cicd/)** - Deploy your backend services

### Alternative Skills (Similar Purpose)
- **[nextjs-fullstack-patterns](../nextjs-fullstack-patterns/)** - If building with Next.js App Router

### Prerequisite Skills (Learn First)
- **[api-design-patterns](../api-design-patterns/)** - Understanding API design helps structure implementations
