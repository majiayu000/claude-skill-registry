---
name: backend-engineer
description: Expert in Template Project backend architecture, service patterns, testing, and API development using Express.js, TypeScript, and Drizzle ORM. Use when implementing backend services, APIs, controllers, database queries, error handling, testing server code, or writing migrations.
---

# Template Backend Engineer

Expert knowledge of backend patterns and architecture for the Template Project.

## Core Architecture

### Technology Stack

- **Runtime**: Node.js with TypeScript
- **Framework**: Express.js
- **Database**: PostgreSQL with Drizzle ORM
- **DI Container**: Awilix (Proxy injection mode)
- **Testing**: Vitest with vitest-mock-extended
- **Validation**: Zod schemas (CRITICAL: Use across ALL layers)

### Service Layer Architecture

```
HTTP Request -> Routes -> Middleware -> Controller -> Service -> Repository -> Database
                                            |           |           |
                                       Validation  Business    Drizzle
                                       & Mapping     Logic        ORM
```

## CRITICAL: Where to Look Before Making Changes

### Pattern References (ALWAYS CHECK THESE FIRST)

| Pattern               | Primary Reference                          | Example Implementation          |
| --------------------- | ------------------------------------------ | ------------------------------- |
| **New Service**       | `src/services/todo.service.ts`             | CRUD service with repository    |
| **New Controller**    | `src/controllers/todo.controller.ts`       | Request validation, error handling |
| **New Repository**    | `src/repositories/todo.repository.ts`      | Drizzle patterns, queries       |
| **New Route**         | `src/routes/todo.routes.ts`                | DI scope resolution             |
| **Unit Tests**        | `src/services/__tests__/*.test.ts`         | Mock setup, test structure      |
| **API Schemas**       | `packages/schema/src/api/todos.ts`         | Zod validation schemas          |

## CRITICAL: Zod Validation Across All Layers

### Why Zod Everywhere?

Strong typing with Zod schemas ensures type safety between server and client, catching errors at compile/validation time rather than runtime. **EVERY data boundary must have Zod validation.**

### Use Enums and Constants, Not Magic Strings

**Never use magic strings.** Always use enums or constants for:

- **Status values**: Use Zod enums for type safety
- **Configuration**: Store in constants files, not inline strings

**Example - Zod Enums**:

```typescript
// GOOD: Zod enum for validation + TypeScript type
const StatusSchema = z.enum(['pending', 'completed']);
type Status = z.infer<typeof StatusSchema>;

// BAD: Plain strings
type Status = string;
```

### Layer-by-Layer Validation

#### 1. Controller Layer (Request Validation)

```typescript
// Define request/response schemas in @todos/schema/src/api/
const CreateTodoRequestSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().optional(),
});

// In controller method
async createTodo(req: Request, res: Response) {
  // Validate request body
  const validatedData = CreateTodoRequestSchema.parse(req.body);

  // Pass to service (type-safe)
  const result = await this.todoService.create(validatedData);
}
```

#### 2. Service Layer (Business Logic)

```typescript
// Service method
async create(input: CreateTodoInput) {
  // Business rules validation
  return await this.repository.create(input);
}
```

#### 3. Repository Layer (Database Operations)

```typescript
// Repository method with Drizzle
async create(data: NewTodo) {
  const [todo] = await this.db
    .insert(todos)
    .values(data)
    .returning();
  return todo;
}
```

### Shared Schema Patterns

#### Location Strategy

```
packages/
├── schema/
│   └── src/
│       ├── api/                        # API Contracts (PRIMARY - ALWAYS USE)
│       │   ├── todos.ts                # Todo request/response schemas
│       │   ├── common.ts               # Shared API schemas (pagination, etc.)
│       │   └── index.ts                # Re-exports all API schemas
│       ├── schema.ts                   # Drizzle database schema
│       └── types.ts                    # Database type exports
└── server/
    └── src/
        ├── controllers/                # Import from @todos/schema/src/api
        ├── services/                   # Import from @todos/schema/src/api
        └── repositories/               # Drizzle ORM operations
```

**CRITICAL**:

- All API request/response contracts MUST be defined in `@todos/schema/src/api/`
- Never create validation schemas in `server/src/` - always use `@todos/schema/src/api/`
- Controllers import and use these schemas directly
- This ensures type safety between frontend and backend

### Zod with Drizzle ORM

```typescript
// Generate Zod schemas from Drizzle tables
import { createInsertSchema, createSelectSchema } from 'drizzle-zod';
import { todos } from '@todos/schema';

// Auto-generate schemas from Drizzle table definitions
export const insertTodoSchema = createInsertSchema(todos);
export const selectTodoSchema = createSelectSchema(todos);

// Extend with custom validations
export const createTodoSchema = insertTodoSchema
  .extend({
    title: z.string().min(1).max(200),
  })
  .omit({ id: true, createdAt: true });
```

## Unit Testing Patterns

### Test Structure (TDD Approach)

```typescript
// Standard test file structure
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mock } from 'vitest-mock-extended';

describe('ServiceName', () => {
  let service: ServiceName;
  let mockRepo: MockType<Repository>;

  beforeEach(() => {
    vi.clearAllMocks();
    mockRepo = mock<Repository>();
    service = new ServiceName(mockRepo);
  });

  describe('methodName', () => {
    it('should handle success case', async () => {
      // Arrange
      const input = { /* test data */ };
      const expected = { /* expected result */ };
      mockRepo.findById.mockResolvedValue(expected);

      // Act
      const result = await service.method(input);

      // Assert
      expect(result).toEqual(expected);
      expect(mockRepo.findById).toHaveBeenCalledWith(input.id);
    });

    it('should handle error case', async () => {
      // Test error scenarios
    });
  });
});
```

### Common Mock Patterns

```typescript
// Mock with specific return
mockService.method.mockResolvedValue(result);

// Mock with implementation
mockService.method.mockImplementation(async (id) => {
  return id === 'valid' ? data : null;
});

// Reset mocks
mockReset(mockService); // Clear all mock data
mockClear(mockService); // Clear call history only
```

## Database & Schema

### Schema Management

- **Schema Location**: `packages/schema/src/schema.ts`
- **Migrations**: `packages/schema/migrations/`
- **Commands**:
  ```bash
  cd packages/schema
  pnpm db:generate --name migration_name  # Generate migration
  pnpm db:migrate                         # Run migrations
  pnpm db:studio                          # Open Drizzle Studio
  ```

### Drizzle ORM Patterns

```typescript
// Repository pattern example
class TodoRepository {
  constructor(private db: NodePgDatabase) {}

  async findById(id: string) {
    return this.db.query.todos.findFirst({
      where: eq(todos.id, id),
    });
  }

  async findAll() {
    return this.db
      .select()
      .from(todos)
      .orderBy(desc(todos.createdAt));
  }
}
```

## Error Handling

### Standard Error Response

```typescript
// In controller - return standardized response
return res.status(400).json({
  success: false,
  error: {
    code: 'VALIDATION_ERROR',
    message: 'Validation failed',
    details: error.issues,
  },
});

// Success response
return res.status(200).json({
  success: true,
  data: result,
});
```

## Development Workflow

### Before Making Changes

1. **Check Pattern References** (table above)
2. **Read Existing Implementation** of similar feature
3. **Write Tests First** (TDD approach)

### Common Commands

```bash
# From packages/server
pnpm test:unit              # Run unit tests only (fast)
pnpm test                   # All tests including integration
pnpm dev                    # Start dev server

# Run specific test file (fastest for TDD)
pnpm vitest run --no-coverage src/services/__tests__/todo.service.test.ts

# From project root (Nx commands)
pnpm test:changed           # Test only changed packages
pnpm test:changed:all       # Include e2e for changed packages
```

## Quick Reference

### DI Container Tokens

```typescript
// Infrastructure
CONTAINER_TOKENS.DATABASE;
CONTAINER_TOKENS.LOGGER;

// Services
CONTAINER_TOKENS.TODO_SERVICE;

// Controllers
CONTAINER_TOKENS.TODO_CONTROLLER;
```

### Test Coverage Requirements

- **Target**: 80% coverage minimum
- **Check Coverage**: `pnpm test:coverage`

### Performance Considerations

- **Query Optimization**: Use Drizzle's query builder over raw SQL
- **Pagination**: Always paginate lists (default 20, max 100)
- **N+1 Prevention**: Use joins or batch queries

---

**Remember**: Always check existing patterns before implementing new ones. This maintains consistency and reduces technical debt.
