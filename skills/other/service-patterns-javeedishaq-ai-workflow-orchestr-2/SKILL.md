# Service Patterns

Service layer patterns for clean architecture with proper error handling, logging, and type safety.

> **Template Usage:** Customize for your ORM (Prisma, Drizzle, TypeORM, etc.) and logging solution.

## Result Type Pattern

Never throw exceptions from services. Always return a Result type.

```typescript
// lib/result.ts
export type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

export function ok<T>(data: T): Result<T, never> {
  return { success: true, data };
}

export function err<E>(error: E): Result<never, E> {
  return { success: false, error };
}
```

## Base Service Pattern

```typescript
// lib/base-service.ts
import { Logger } from './logger';

export abstract class BaseService {
  protected logger: Logger;

  constructor(serviceName: string) {
    this.logger = new Logger(serviceName);
  }

  protected handleError<T>(
    operation: string,
    error: unknown,
    context?: Record<string, unknown>
  ): Result<T, ServiceError> {
    this.logger.error(`${operation} failed`, { error, ...context });

    if (error instanceof ServiceError) {
      return err(error);
    }

    return err(new ServiceError(
      error instanceof Error ? error.message : 'Unknown error',
      'INTERNAL_ERROR'
    ));
  }
}

export class ServiceError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
  }
}
```

## Service Implementation

```typescript
// services/user.service.ts
import { BaseService, ServiceError } from '@/lib/base-service';
import { ok, err, Result } from '@/lib/result';
import { db } from '@/lib/db';
import { User, CreateUserInput, UpdateUserInput } from '@/types';

export class UserService extends BaseService {
  constructor() {
    super('UserService');
  }

  async findById(id: string): Promise<Result<User | null, ServiceError>> {
    try {
      const user = await db.user.findUnique({ where: { id } });
      return ok(user);
    } catch (error) {
      return this.handleError('findById', error, { id });
    }
  }

  async create(input: CreateUserInput): Promise<Result<User, ServiceError>> {
    try {
      // Validate business rules
      const existing = await db.user.findUnique({
        where: { email: input.email }
      });

      if (existing) {
        return err(new ServiceError(
          'Email already in use',
          'EMAIL_EXISTS',
          409
        ));
      }

      const user = await db.user.create({ data: input });
      this.logger.info('User created', { userId: user.id });

      return ok(user);
    } catch (error) {
      return this.handleError('create', error, { email: input.email });
    }
  }

  async update(
    id: string,
    input: UpdateUserInput
  ): Promise<Result<User, ServiceError>> {
    try {
      const user = await db.user.update({
        where: { id },
        data: input,
      });

      this.logger.info('User updated', { userId: id });
      return ok(user);
    } catch (error) {
      return this.handleError('update', error, { id });
    }
  }

  async delete(id: string): Promise<Result<void, ServiceError>> {
    try {
      await db.user.delete({ where: { id } });
      this.logger.info('User deleted', { userId: id });
      return ok(undefined);
    } catch (error) {
      return this.handleError('delete', error, { id });
    }
  }
}

// Singleton instance
export const userService = new UserService();
```

## Mapper Pattern

```typescript
// mappers/user.mapper.ts
import { User as DbUser } from '@prisma/client';
import { User } from '@/types';

export class UserMapper {
  static toEntity(dbUser: DbUser): User {
    return {
      id: dbUser.id,
      email: dbUser.email,
      name: dbUser.name,
      createdAt: dbUser.created_at,
      updatedAt: dbUser.updated_at,
    };
  }

  static toEntities(dbUsers: DbUser[]): User[] {
    return dbUsers.map(this.toEntity);
  }
}
```

## Transaction Pattern

```typescript
async createUserWithProfile(
  userData: CreateUserInput,
  profileData: CreateProfileInput
): Promise<Result<{ user: User; profile: Profile }, ServiceError>> {
  try {
    const result = await db.$transaction(async (tx) => {
      const user = await tx.user.create({ data: userData });
      const profile = await tx.profile.create({
        data: { ...profileData, userId: user.id }
      });
      return { user, profile };
    });

    return ok(result);
  } catch (error) {
    return this.handleError('createUserWithProfile', error);
  }
}
```

## Batch Operations (Avoid N+1)

```typescript
// BAD: N+1 query
async getUsersWithPosts(userIds: string[]) {
  const users = await db.user.findMany({ where: { id: { in: userIds } } });

  // N+1: One query per user!
  for (const user of users) {
    user.posts = await db.post.findMany({ where: { userId: user.id } });
  }
}

// GOOD: Batch query
async getUsersWithPosts(userIds: string[]) {
  const [users, posts] = await Promise.all([
    db.user.findMany({ where: { id: { in: userIds } } }),
    db.post.findMany({ where: { userId: { in: userIds } } }),
  ]);

  // Join in memory
  const postsMap = new Map<string, Post[]>();
  for (const post of posts) {
    const userPosts = postsMap.get(post.userId) || [];
    userPosts.push(post);
    postsMap.set(post.userId, userPosts);
  }

  return users.map(user => ({
    ...user,
    posts: postsMap.get(user.id) || [],
  }));
}
```

## Service Usage in Actions

```typescript
'use server';

import { userService } from '@/services/user.service';
import { revalidatePath } from 'next/cache';

export async function createUserAction(formData: FormData) {
  const result = await userService.create({
    email: formData.get('email') as string,
    name: formData.get('name') as string,
  });

  if (!result.success) {
    return {
      success: false,
      error: result.error.message,
      code: result.error.code,
    };
  }

  revalidatePath('/users');
  return { success: true, data: result.data };
}
```

## Checklist

- [ ] Returns Result<T, E> - never throws
- [ ] Logs errors with context
- [ ] Uses transactions for multi-step operations
- [ ] Avoids N+1 queries
- [ ] Maps DB entities to domain types
- [ ] Validates business rules
- [ ] Handles edge cases
