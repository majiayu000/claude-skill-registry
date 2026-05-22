---
name: hono-ipc-patterns
description: Advanced patterns for Hono-based Electron IPC including CQRS, Zod validation, error handling, and reactive data with RxJS. Use when implementing complex IPC patterns or needing guidance on architecture decisions.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Hono IPC Patterns

This skill provides advanced patterns for building robust IPC communication in Electron applications using Hono.

## When This Skill Applies

- Implementing CQRS (Command Query Responsibility Segregation) pattern
- Adding Zod validation to routes
- Handling errors with Result types (neverthrow)
- Implementing reactive data streams with RxJS
- Testing IPC routes

## CQRS Pattern

### Core Principles

| Aspect | Query | Command |
|--------|-------|---------|
| Purpose | Read data | Modify state |
| Return Type | `Observable<T>` | `ResultAsync<void, Error>` |
| Side Effects | None | Database/API writes |
| Caching | Yes (reactive updates) | No |

### Service Interface Example

```typescript
// src/shared/services/event.service.ts
import type { Observable } from 'rxjs';
import type { ResultAsync } from 'neverthrow';

export interface EventService {
  // === QUERIES (return Observable) ===

  // Get active event (reactive - auto-updates on changes)
  active(): Observable<EventInstance | undefined>;

  // Get event history (reactive)
  histories(includeHidden?: boolean): Observable<EventInstance[]>;

  // Get single event
  get(id: number): Observable<EventInstance | undefined>;

  // === COMMANDS (return ResultAsync) ===

  // Create event (one-shot operation)
  create(data: CreateEventData): ResultAsync<void, ApplicationError>;

  // Update event
  update(id: number, data: UpdateEventData): ResultAsync<void, ApplicationError>;

  // Delete event
  delete(id: number): ResultAsync<void, ApplicationError>;

  // Perform action on event
  invite(userId: string, location: Location): ResultAsync<void, ApplicationError>;
}
```

### Route Handler Pattern

```typescript
// For Queries - convert Observable to single value
.get('/', async (c) => {
  const result = await firstValueFrom(c.var.services.events.histories());
  return c.json(result, 200);
})

// For Commands - use Result pattern matching
.post('/', zValidator('json', CreateEventBody), async (c) => {
  const body = c.req.valid('json');

  const result = await c.var.services.events.create(body);

  return result.match(
    () => c.json({ success: true }, 201),
    (error) => c.json({ error: error.message }, error.statusCode ?? 500)
  );
})
```

See [CQRS.md](CQRS.md) for complete CQRS documentation.

## Zod Validation Patterns

### Request Validation Layers

```typescript
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

// Path parameter validation
const IdParam = z.object({
  id: z.string().regex(/^[a-z]{3}_[a-zA-Z0-9]+$/),
});

// Query parameter validation (with coercion)
const PaginationQuery = z.object({
  limit: z.coerce.number().int().positive().max(100).default(10),
  offset: z.coerce.number().int().nonnegative().default(0),
});

// JSON body validation
const CreateBody = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(1000).optional(),
});

// Combined usage
.get('/:id', zValidator('param', IdParam), (c) => { ... })
.get('/', zValidator('query', PaginationQuery), (c) => { ... })
.post('/', zValidator('json', CreateBody), (c) => { ... })
```

See [ZOD-VALIDATION.md](ZOD-VALIDATION.md) for complete validation documentation.

## Error Handling Patterns

### Centralized Error Handler

```typescript
const factory = (deps: Dependencies) =>
  createFactory<HonoEnv>({
    initApp(app) {
      // Global error handler
      app.onError((err, c) => {
        // Log error
        deps.logger?.error('Request error:', err);

        // Handle known error types
        if (err instanceof HTTPException) {
          return c.json({ error: err.message }, err.status);
        }

        if (err instanceof ValidationError) {
          return c.json({ error: err.message, details: err.issues }, 400);
        }

        // Unknown errors
        return c.json({ error: 'Internal Server Error' }, 500);
      });
    },
  });
```

### Result Type Pattern Matching

```typescript
.post('/action', async (c) => {
  const result = await c.var.services.action.perform();

  return result.match(
    (data) => c.json(data, 200),
    (error) => {
      // Type-safe error handling
      switch (error.code) {
        case 'NOT_FOUND':
          return c.json({ error: error.message }, 404);
        case 'UNAUTHORIZED':
          return c.json({ error: error.message }, 401);
        case 'VALIDATION_ERROR':
          return c.json({ error: error.message, details: error.details }, 400);
        default:
          return c.json({ error: 'Operation failed' }, 500);
      }
    }
  );
})
```

## Reactive Data Patterns

### BehaviorSubject for Query Updates

```typescript
// Service implementation pattern
export class UserServiceImpl implements UserService {
  #notify = new BehaviorSubject(Date.now());

  // Query: Returns Observable that updates on changes
  list(): Observable<User[]> {
    return concat(
      // Initial data fetch
      from(this.#fetchUsers()),
      // Re-fetch when notified
      this.#notify.pipe(
        distinctUntilChanged(),
        mergeMap(() => this.#fetchUsers())
      )
    );
  }

  // Command: Modifies data and notifies subscribers
  async create(data: CreateUserData): ResultAsync<void, Error> {
    const result = await this.#createUser(data);

    if (result.isOk()) {
      // Notify all query subscribers to refresh
      this.#notify.next(Date.now());
    }

    return result;
  }
}
```

### Helper for Observable to Value

```typescript
// utils/observable.ts
import { firstValueFrom, Observable } from 'rxjs';

export const firstValueFromResult = <T>(
  observable: Observable<T>
): Promise<T> => {
  return firstValueFrom(observable);
};

// Usage in routes
.get('/', async (c) => {
  const users = await firstValueFromResult(c.var.services.users.list());
  return c.json(users, 200);
})
```

## Testing Patterns

### Route Unit Testing

```typescript
import { Hono } from 'hono';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { of } from 'rxjs';
import { ok, err } from 'neverthrow';

describe('Events Route', () => {
  let app: Hono<HonoEnv>;
  let mockEventService: Partial<EventService>;

  beforeEach(() => {
    mockEventService = {
      list: vi.fn(),
      create: vi.fn(),
    };

    app = new Hono<HonoEnv>();
    app.use((c, next) => {
      c.set('services', { events: mockEventService } as any);
      return next();
    });
    app.route('/events', routes);
  });

  it('should list events', async () => {
    mockEventService.list.mockReturnValue(of([{ id: 1, name: 'Event' }]));

    const res = await app.request('/events');
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data).toHaveLength(1);
  });

  it('should handle create error', async () => {
    mockEventService.create.mockReturnValue(
      err({ code: 'VALIDATION_ERROR', message: 'Invalid data' })
    );

    const res = await app.request('/events', {
      method: 'POST',
      body: JSON.stringify({ name: '' }),
      headers: { 'Content-Type': 'application/json' },
    });

    expect(res.status).toBe(400);
  });
});
```

## Files Reference

- [CQRS.md](CQRS.md) - Complete CQRS pattern documentation
- [ZOD-VALIDATION.md](ZOD-VALIDATION.md) - Zod validation patterns
