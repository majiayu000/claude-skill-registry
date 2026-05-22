---
name: typescript-api
description: TypeScript/Node.js API development skills. REST API patterns, Express/Fastify handlers, TypeScript types, Zod validation, and async patterns.
---

# TypeScript API Development Skill

You are a TypeScript API development expert. You create type-safe, well-structured REST APIs following modern best practices.

## Core Principles

1. **Type Safety**: Leverage TypeScript's type system fully
2. **Validation**: Use Zod for runtime schema validation
3. **Error Handling**: Consistent error responses across all endpoints
4. **Async/Await**: Proper async patterns and error propagation
5. **Separation of Concerns**: Clear separation between routes, controllers, services, and models

## Project Structure

```
src/
  routes/           # Route definitions and middleware
  controllers/      # Request handlers
  services/         # Business logic
  models/           # Type definitions and schemas
  middleware/       # Custom middleware
  utils/            # Helper functions
  index.ts          # Application entry point
```

## Type Definitions

### Request/Response Types

```typescript
// types/api.ts
export interface CreateUserRequest {
  email: string;
  password: string;
  name: string;
}

export interface UserResponse {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
}
```

### Zod Validation Schemas

```typescript
// schemas/user.ts
import { z } from 'zod';

export const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  name: z.string().min(1, 'Name is required'),
});

export const updateUserSchema = createUserSchema.partial();

export const getUserParamsSchema = z.object({
  id: z.string().uuid('Invalid user ID format'),
});

export type CreateUserInput = z.infer<typeof createUserSchema>;
export type UpdateUserInput = z.infer<typeof updateUserSchema>;
export type GetUserParamsInput = z.infer<typeof getUserParamsSchema>;
```

## Route Handlers

### Express Handler Pattern

```typescript
// controllers/userController.ts
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { createUserSchema, getUserParamsSchema, updateUserSchema } from '../schemas/user';
import * as userService from '../services/userService';

export async function createUser(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    // Validate request body
    const input = createUserSchema.parse(req.body);

    // Call service layer
    const user = await userService.createUser(input);

    // Send response
    res.status(201).json({
      success: true,
      data: user,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid request data',
          details: error.errors,
        },
      });
      return;
    }
    next(error); // Pass to error handler
  }
}

export async function getUser(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const { id } = getUserParamsSchema.parse(req.params);
    const user = await userService.getUserById(id);

    if (!user) {
      res.status(404).json({
        success: false,
        error: {
          code: 'NOT_FOUND',
          message: 'User not found',
        },
      });
      return;
    }

    res.json({
      success: true,
      data: user,
    });
  } catch (error) {
    next(error);
  }
}

export async function updateUser(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const { id } = getUserParamsSchema.parse(req.params);
    const input = updateUserSchema.parse(req.body);
    const user = await userService.updateUser(id, input);

    if (!user) {
      res.status(404).json({
        success: false,
        error: {
          code: 'NOT_FOUND',
          message: 'User not found',
        },
      });
      return;
    }

    res.json({
      success: true,
      data: user,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid request data',
          details: error.errors,
        },
      });
      return;
    }
    next(error);
  }
}

export async function deleteUser(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const { id } = getUserParamsSchema.parse(req.params);
    const deleted = await userService.deleteUser(id);

    if (!deleted) {
      res.status(404).json({
        success: false,
        error: {
          code: 'NOT_FOUND',
          message: 'User not found',
        },
      });
      return;
    }

    res.status(204).send();
  } catch (error) {
    next(error);
  }
}
```

### Route Definition

```typescript
// routes/userRoutes.ts
import { Router } from 'express';
import * as userController from '../controllers/userController';
import { authenticate } from '../middleware/auth';

const router = Router();

router.post('/users', authenticate, userController.createUser);
router.get('/users/:id', authenticate, userController.getUser);
router.patch('/users/:id', authenticate, userController.updateUser);
router.delete('/users/:id', authenticate, userController.deleteUser);

export default router;
```

## Service Layer

```typescript
// services/userService.ts
import { db } from '../db';
import { CreateUserInput, UpdateUserInput, UserResponse } from '../types/api';
import { hashPassword } from '../utils/crypto';

export async function createUser(
  input: CreateUserInput
): Promise<UserResponse> {
  // Check if user exists
  const existing = await db.user.findUnique({
    where: { email: input.email },
  });

  if (existing) {
    throw new Error('USER_ALREADY_EXISTS');
  }

  // Hash password
  const hashedPassword = await hashPassword(input.password);

  // Create user
  const user = await db.user.create({
    data: {
      email: input.email,
      password: hashedPassword,
      name: input.name,
    },
  });

  // Return response (excluding password)
  return {
    id: user.id,
    email: user.email,
    name: user.name,
    createdAt: user.createdAt,
  };
}

export async function getUserById(id: string): Promise<UserResponse | null> {
  const user = await db.user.findUnique({
    where: { id },
  });

  if (!user) {
    return null;
  }

  return {
    id: user.id,
    email: user.email,
    name: user.name,
    createdAt: user.createdAt,
  };
}

export async function updateUser(
  id: string,
  input: UpdateUserInput
): Promise<UserResponse | null> {
  const user = await db.user.update({
    where: { id },
    data: input,
  });

  if (!user) {
    return null;
  }

  return {
    id: user.id,
    email: user.email,
    name: user.name,
    createdAt: user.createdAt,
  };
}

export async function deleteUser(id: string): Promise<boolean> {
  try {
    await db.user.delete({
      where: { id },
    });
    return true;
  } catch {
    return false;
  }
}
```

## Utility Functions

```typescript
// utils/crypto.ts
import bcrypt from 'bcrypt';

export async function hashPassword(password: string): Promise<string> {
  const salt = await bcrypt.genSalt(10);
  return bcrypt.hash(password, salt);
}

export async function comparePassword(
  password: string,
  hashedPassword: string
): Promise<boolean> {
  return bcrypt.compare(password, hashedPassword);
}
```

## Error Handling Middleware

```typescript
// middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';

// Custom error class for application errors
export class AppError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  console.error('Error:', err);

  // Handle Zod validation errors
  if (err instanceof ZodError) {
    res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid request data',
        details: err.errors,
      },
    });
    return;
  }

  // Handle custom application errors
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message,
      },
    });
    return;
  }

  // Generic error response
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_SERVER_ERROR',
      message: 'An unexpected error occurred',
    },
  });
}

// Usage example in services:
// throw new AppError('USER_NOT_FOUND', 'User not found', 404);
```

## Async Patterns

### Proper Async/Await

```typescript
// GOOD: Proper async error handling
async function fetchUserData(userId: string): Promise<User> {
  try {
    const user = await db.user.findUnique({ where: { id: userId } });
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  } catch (error) {
    // Log and rethrow with context
    console.error('Failed to fetch user:', userId, error);
    throw error;
  }
}

// BAD: Not awaiting promises
async function badExample() {
  db.user.create({ data: userData }); // Fire-and-forget!
}

// GOOD: Await all promises
async function goodExample() {
  await db.user.create({ data: userData });
}
```

### Parallel Operations

```typescript
// GOOD: Parallel independent operations
async function getUserWithPosts(userId: string) {
  const [user, posts] = await Promise.all([
    db.user.findUnique({ where: { id: userId } }),
    db.post.findMany({ where: { userId } }),
  ]);

  return { user, posts };
}

// GOOD: Parallel with error handling
async function fetchMultipleUsers(ids: string[]) {
  const results = await Promise.allSettled(
    ids.map(id => db.user.findUnique({ where: { id } }))
  );

  return results.map((result, index) => ({
    id: ids[index],
    success: result.status === 'fulfilled',
    data: result.status === 'fulfilled' ? result.value : null,
    error: result.status === 'rejected' ? result.reason : null,
  }));
}
```

## Testing

### Controller Tests

```typescript
import request from 'supertest';
import express from 'express';
import * as userController from './userController';

const app = express();
app.use(express.json());
app.post('/users', userController.createUser);

describe('POST /users', () => {
  it('should create a user', async () => {
    const response = await request(app)
      .post('/users')
      .send({
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
      });

    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data).toHaveProperty('id');
  });

  it('should return 400 for invalid email', async () => {
    const response = await request(app)
      .post('/users')
      .send({
        email: 'invalid-email',
        password: 'password123',
        name: 'Test User',
      });

    expect(response.status).toBe(400);
    expect(response.body.success).toBe(false);
  });
});
```

## Best Practices

1. **Always use strict mode**: Enable `strict: true` in tsconfig.json
2. **Validate all inputs**: Never trust request data
3. **Use enums for constants**: Instead of magic strings
4. **Document types**: Use JSDoc for complex types
5. **Handle all errors**: Never let errors propagate to the client
6. **Use environment variables**: For configuration (use dotenv)
7. **Keep routes thin**: Business logic belongs in services
8. **Return consistent responses**: Use ApiResponse wrapper

## Common Patterns

### Pagination

```typescript
interface PaginationParams {
  page: number;
  limit: number;
}

interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    limit: number;
    totalPages: number;
  };
}

async function getPaginatedUsers(
  params: PaginationParams
): Promise<PaginatedResponse<UserResponse>> {
  const skip = (params.page - 1) * params.limit;
  const [users, total] = await Promise.all([
    db.user.findMany({
      skip,
      take: params.limit,
    }),
    db.user.count(),
  ]);

  return {
    data: users,
    meta: {
      total,
      page: params.page,
      limit: params.limit,
      totalPages: Math.ceil(total / params.limit),
    },
  };
}
```

### Searching and Filtering

```typescript
interface UserFilters {
  email?: string;
  name?: string;
  createdAfter?: Date;
}

async function findUsers(filters: UserFilters): Promise<UserResponse[]> {
  const where = {
    ...(filters.email && { email: { contains: filters.email } }),
    ...(filters.name && { name: { contains: filters.name, mode: 'insensitive' as const } }),
    ...(filters.createdAfter && { createdAt: { gte: filters.createdAfter } }),
  };

  return db.user.findMany({ where });
}
```
