---
name: backend-engineer
description: Expert in backend architecture, service patterns, testing, and API development using Express.js, TypeScript, and Drizzle ORM. Use when implementing backend services, APIs, controllers, database queries, error handling, testing server code, or writing migrations.
---

# Backend Engineer

Expert knowledge of backend patterns and architecture for Express.js APIs.

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

## Pattern References (ALWAYS CHECK THESE FIRST)

| Pattern            | Reference Path                         | Notes                            |
| ------------------ | -------------------------------------- | -------------------------------- |
| **Service**        | `src/services/*.service.ts`            | CRUD service with repository     |
| **Controller**     | `src/controllers/*.controller.ts`      | Request validation, error handling |
| **Repository**     | `src/repositories/*.repository.ts`     | Drizzle patterns, queries        |
| **Routes**         | `src/routes/*.routes.ts`               | DI scope resolution              |
| **Unit Tests**     | `src/services/__tests__/*.test.ts`     | Mock setup, test structure       |
| **API Schemas**    | `packages/schema/src/api/`             | Zod validation schemas           |

## Zod Validation Across All Layers (CRITICAL)

Every data boundary must have Zod validation. Never use magic strings — use enums/constants.

### Layer-by-Layer Validation

#### 1. Controller Layer (Request Validation)

```typescript
// Schemas defined in packages/schema/src/api/
const CreateItemRequestSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().optional(),
});

async createItem(req: Request, res: Response) {
  const validatedData = CreateItemRequestSchema.parse(req.body);
  const result = await this.itemService.create(validatedData);
  return res.status(201).json({ success: true, data: result });
}
```

#### 2. Service Layer (Business Logic)

```typescript
async create(input: CreateItemInput) {
  // Business rules here
  return await this.repository.create(input);
}
```

#### 3. Repository Layer (Database Operations)

```typescript
async create(data: NewItem) {
  const [item] = await this.db
    .insert(items)
    .values(data)
    .returning();
  return item;
}
```

### Shared Schema Location

```
packages/schema/src/
├── api/                # API Contracts (ALWAYS USE)
│   ├── items.ts        # Request/response schemas
│   ├── common.ts       # Shared schemas (pagination, etc.)
│   └── index.ts        # Re-exports
├── schema.ts           # Drizzle database schema
└── types.ts            # Database type exports
```

**CRITICAL**: All API request/response contracts MUST be in `packages/schema/src/api/`. Never create validation schemas in `server/src/`.

### Zod with Drizzle ORM

```typescript
import { createInsertSchema, createSelectSchema } from 'drizzle-zod';
import { items } from '@app/schema';

export const insertItemSchema = createInsertSchema(items);
export const createItemSchema = insertItemSchema
  .extend({ title: z.string().min(1).max(200) })
  .omit({ id: true, createdAt: true });
```

## Unit Testing Patterns

### Test Structure (TDD Approach)

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mock } from 'vitest-mock-extended';

describe('ItemService', () => {
  let service: ItemService;
  let mockRepo: MockType<ItemRepository>;

  beforeEach(() => {
    vi.clearAllMocks();
    mockRepo = mock<ItemRepository>();
    service = new ItemService(mockRepo);
  });

  describe('create', () => {
    it('should create item successfully', async () => {
      const input = { title: 'Test' };
      const expected = { id: '1', ...input };
      mockRepo.create.mockResolvedValue(expected);

      const result = await service.create(input);

      expect(result).toEqual(expected);
      expect(mockRepo.create).toHaveBeenCalledWith(input);
    });
  });
});
```

### Common Mock Patterns

```typescript
mockService.method.mockResolvedValue(result);
mockService.method.mockImplementation(async (id) => id === 'valid' ? data : null);
mockReset(mockService);  // Clear all mock data
mockClear(mockService);  // Clear call history only
```

## Database & Schema

### Schema Management

```bash
cd packages/schema
pnpm db:generate --name migration_name  # Generate migration
pnpm db:migrate                         # Run migrations
pnpm db:studio                          # Open Drizzle Studio
```

### Drizzle ORM Patterns

```typescript
class ItemRepository {
  constructor(private db: NodePgDatabase) {}

  async findById(id: string) {
    return this.db.query.items.findFirst({
      where: eq(items.id, id),
    });
  }

  async findAll() {
    return this.db.select().from(items).orderBy(desc(items.createdAt));
  }
}
```

## Error Handling

```typescript
// Standardized error response
return res.status(400).json({
  success: false,
  error: { code: 'VALIDATION_ERROR', message: 'Validation failed', details: error.issues },
});

// Success response
return res.status(200).json({ success: true, data: result });
```

## DI Container Tokens

```typescript
CONTAINER_TOKENS.DATABASE;
CONTAINER_TOKENS.LOGGER;
CONTAINER_TOKENS.ITEM_SERVICE;
CONTAINER_TOKENS.ITEM_CONTROLLER;
```

## Common Commands

```bash
pnpm dev                    # Start dev server
pnpm test:unit              # Run unit tests (fast)
pnpm test                   # All tests including integration
pnpm vitest run --no-coverage src/services/__tests__/item.service.test.ts  # Specific file
pnpm test:changed           # Test only changed packages
```

## Checklist

- [ ] Check pattern references before implementing
- [ ] Zod validation at ALL boundaries
- [ ] No magic strings — use enums/constants
- [ ] API schemas in packages/schema/src/api/
- [ ] Unit tests with vitest-mock-extended
- [ ] Test coverage >= 80%
- [ ] Standardized error responses
