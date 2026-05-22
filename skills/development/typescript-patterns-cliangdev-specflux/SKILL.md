---
name: typescript-patterns
description: TypeScript best practices. Use when writing TypeScript code for backend services, API handlers, or shared utilities. Applies async/await patterns, typed errors, and strict type safety.
---

# TypeScript Best Practices

## Patterns

### Async/Await Pattern
Always use async/await, never callbacks or .then():

```typescript
// Good
async function createTask(data: CreateTaskRequest): Promise<Task> {
  const task = await db.insert(tasks).values(data).returning();
  return task[0];
}

// Bad
function createTask(data: CreateTaskRequest): Promise<Task> {
  return db.insert(tasks).values(data).returning().then(result => result[0]);
}
```

### Error Handling
Always use typed errors:

```typescript
class EntityNotFoundError extends Error {
  constructor(entityType: string, id: string | number) {
    super(`${entityType} ${id} not found`);
    this.name = 'EntityNotFoundError';
  }
}

// Usage
async function getTask(id: number): Promise<Task> {
  const task = await db.query.tasks.findFirst({ where: eq(tasks.id, id) });
  if (!task) throw new EntityNotFoundError('Task', id);
  return task;
}
```

### Type Safety
Use strict TypeScript, never 'any':

```typescript
// Good
interface CreateTaskRequest {
  title: string;
  description?: string;
  epicId?: number;
}

// Bad
function createTask(data: any) { ... }
```

### API Response Pattern
All API responses follow this structure:

```typescript
type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: string };

// Usage
app.get('/tasks/:id', async (req, res) => {
  try {
    const task = await getTask(Number(req.params.id));
    res.json({ success: true, data: task });
  } catch (error) {
    res.status(404).json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});
```

### Discriminated Unions
Use discriminated unions for type-safe state handling:

```typescript
type RequestState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

// Usage
function handleState<T>(state: RequestState<T>) {
  switch (state.status) {
    case 'idle':
      return 'Not started';
    case 'loading':
      return 'Loading...';
    case 'success':
      return state.data; // TypeScript knows data exists
    case 'error':
      return state.error; // TypeScript knows error exists
  }
}
```

### Utility Types
Use built-in utility types effectively:

```typescript
// Partial - all properties optional
type UpdateTaskRequest = Partial<CreateTaskRequest>;

// Pick - select specific properties
type TaskSummary = Pick<Task, 'id' | 'title' | 'status'>;

// Omit - exclude specific properties
type CreateTaskInput = Omit<Task, 'id' | 'createdAt' | 'updatedAt'>;

// Required - all properties required
type RequiredConfig = Required<OptionalConfig>;

// Record - typed object with specific keys
type StatusCounts = Record<TaskStatus, number>;
```

### Generics
Use generics for reusable, type-safe functions:

```typescript
// Generic repository pattern
interface Repository<T, ID> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<void>;
}

// Generic API handler
async function handleRequest<T>(
  fn: () => Promise<T>,
  res: Response
): Promise<void> {
  try {
    const data = await fn();
    res.json({ success: true, data });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
```

## File Organization

```
src/
├── types/          # Shared TypeScript types
├── services/       # Business logic
├── routes/         # API endpoints
├── db/             # Database schema & migrations
└── utils/          # Helper functions
```

## Import Best Practices

```typescript
// Good - explicit imports
import { Task, TaskStatus } from './types';
import { createTask, updateTask } from './services/taskService';

// Bad - wildcard imports
import * as types from './types';
import * as taskService from './services/taskService';
```

## Null Handling

```typescript
// Use nullish coalescing
const name = user.name ?? 'Anonymous';

// Use optional chaining
const city = user.address?.city;

// Type guards for narrowing
function isTask(obj: unknown): obj is Task {
  return typeof obj === 'object' && obj !== null && 'id' in obj && 'title' in obj;
}
```
