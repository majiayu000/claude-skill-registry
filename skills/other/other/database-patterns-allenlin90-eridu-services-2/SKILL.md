---
name: database-patterns
description: Provides Prisma-specific patterns for soft delete, transactions, optimistic locking, bulk operations, and performance optimization. This skill should be used when implementing data persistence, handling concurrent updates, managing complex multi-table operations, or optimizing query performance.
---

# Database Patterns Skill (Prisma/PostgreSQL)

**The Single Source of Truth for Database Interactions in Eridu Services.**

This skill provides mandatory patterns for using Prisma ORM effectively, ensuring data integrity, performance, and maintainability.

## 1. Soft Delete Pattern

**Rule**: NEVER permanently delete logic data. Use `deletedAt` timestamps.

### Schema Support
```prisma
model User {
  id        BigInt    @id @default(autoincrement())
  uid       String    @unique
  deletedAt DateTime? @map("deleted_at")
  
  @@index([deletedAt]) // Mandatory index for filtering
}
```

### Querying (The most common pitfall)
You **MUST** filter out deleted records in **every** query unless specifically introspecting history.

```typescript
// ✅ CORRECT
const activeUsers = await prisma.user.findMany({
  where: { deletedAt: null }
});

// ❌ WRONG (Returns deleted "zombie" records)
const users = await prisma.user.findMany();
```

### Implementing Soft Delete
```typescript
// ✅ CORRECT: Update timestamp
await prisma.user.update({
  where: { uid: 'u_1' },
  data: { deletedAt: new Date() }
});
```

---

## 2. Bulk Operations Pattern

**Rule**: NEVER loop over database calls. Use specialized bulk methods.

### Batch Insert
```typescript
// ✅ CORRECT: Single Query
await prisma.show.createMany({
  data: shows.map(s => ({ ...s, uid: generateUid() })),
  skipDuplicates: true // Optional resilience
});
```

### Batch Update
```typescript
// ✅ CORRECT: Update by criteria
await prisma.show.updateMany({
  where: { clientId: 1, deletedAt: null },
  data: { status: 'PUBLISHED' }
});
```

---

## 3. Transaction Pattern

**Rule**: Use the `@Transactional()` decorator via CLS (Continuation-Local Storage) for **Atomic Multi-Entity Operations**.

Transactions are propagated automatically through the async context — no `tx` parameter passing between methods.

**Scenario**: Creating a Show requires creating ShowMCs and ShowPlatforms simultaneously.

```typescript
import { Transactional } from '@nestjs-cls/transactional';

@Injectable()
export class ShowOrchestrationService {
  constructor(
    private readonly showService: ShowService,
    private readonly showMcService: ShowMcService,
  ) {}

  @Transactional()
  async createShowWithMcs(data: CreateShowWithMcsPayload) {
    // No `tx` passed — CLS propagates it to all repository calls automatically
    const show = await this.showService.createShow(data);
    await this.showMcService.createMany(show.id, data.mcs);
    return show;
  }
}
```

**Critical Rules**:
1.  Apply `@Transactional()` on the **Orchestration Service** method, not on individual repository/model-service calls.
2.  Keep transactions **short**. Do not await external API calls (HTTP, email) inside a transaction.
3.  Never pass `tx` as a method parameter — CLS handles propagation transparently.
4.  Repositories access the active transaction via `TransactionHost` (injected by the CLS adapter).

> [!NOTE]
> **Legacy `$transaction` calls**: Some existing code may still use `prisma.$transaction(async (tx) => {...})` with explicit `tx` passing.
> This is the **old pattern** and will be migrated to `@Transactional()` in Phase 2. Do NOT write new code using the old pattern.

---

## 4. Query Optimization Patterns

### N+1 Prevention (Eager Loading)
**Rule**: Fetch related data in a single query using `include`.

```typescript
// ✅ CORRECT: 1 Query
const shows = await prisma.show.findMany({
  include: { client: true }
});

// ❌ WRONG: 1 + N Queries
const shows = await prisma.show.findMany();
for (const show of shows) {
  await prisma.client.findUnique({ where: { id: show.clientId } });
}
```

### Parallel Execution
**Rule**: Independent queries should run concurrently.

```typescript
// ✅ CORRECT: Runs in parallel
const [users, count] = await Promise.all([
  prisma.user.findMany({ where }),
  prisma.user.count({ where })
]);

// ❌ WRONG: Runs sequentially (slower)
const users = await prisma.user.findMany({ where });
const count = await prisma.user.count({ where });
```

---

## 5. Nested Connect Pattern

**Rule**: Use `connect: { uid }` to link entities. avoids an extra read query to find the `id`.

```typescript
// ✅ CORRECT
await prisma.show.create({
  data: {
    client: { connect: { uid: 'client_123' } } // Prisma handles the lookup
  }
});

// ❌ WRONG
const client = await prisma.client.findUnique({ where: { uid: 'client_123' }});
await prisma.show.create({
  data: { clientId: client.id }
});
```

---

## 6. Optimistic Locking (Version Check)

**Rule**: Use a `version` integer to prevent overwriting concurrent updates.

### Schema Support
```prisma
model TaskTemplate {
  id      BigInt @id @default(autoincrement())
  uid     String @unique
  version Int    @default(1)
  // ... other fields
}
```

### Implementation Pattern

**Repository Layer**: Implement version check and throw domain error

```typescript
async updateWithVersionCheck(
  where: Prisma.TaskTemplateWhereUniqueInput & { version?: number },
  data: Prisma.TaskTemplateUpdateInput,
): Promise<TaskTemplate> {
  try {
    return await this.prisma.taskTemplate.update({
      where: { ...where, deletedAt: null },
      data,
    });
  } catch (error) {
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      if (error.code === PRISMA_ERROR.RecordNotFound && where.version) {
        const existing = await this.findOne({ uid: where.uid, deletedAt: null });
        
        if (!existing) {
          throw error; // Actually not found
        }
        
        // Version conflict - throw domain error
        throw new VersionConflictError(
          'Task template version is outdated',
          where.version,
          existing.version,
        );
      }
    }
    throw error;
  }
}
```

**Service Layer**: Catch and convert to HTTP error

```typescript
try {
  const newVersion = (payload.version as number) + 1;
  return await this.repository.updateWithVersionCheck(
    where,
    {
      ...data,
      version: newVersion,
    },
  );
} catch (error) {
  if (error instanceof VersionConflictError) {
    throw HttpError.conflict(
      `Record is out of date. Please refresh and try again.`,
    );
  }
  throw error;
}
```

### Why Use Domain Error?

- **Layer Separation**: Repository doesn't know about HTTP
- **Testability**: Can test version conflicts without HTTP context
- **Reusability**: Same error handling across different transport layers

---

## 7. Relationships vs Polymorphism

**Rule**: PREFER Explicit Foreign Keys over Polymorphic IDs (`entity_id` + `entity_type`).

**Why?**
1.  **Strict Integrity**: Polymorphism bypasses Foreign Key constraints, leading to "orphan data" (e.g., a Task pointing to a deleted Show).
2.  **Performance (N+1)**: Prisma cannot `include` polymorphic relations natively. You are forced to loop and fetch manually, killing performance.
3.  **Type Safety**: Explicit relations (`show: Show?`) are fully typed. Polymorphic IDs needs manual type narrowing.

```typescript
// ✅ CORRECT: Explicit Nullable FKs ("Exclusive Arc" Pattern)
model Task {
  id       BigInt @id
  showId   BigInt?
  show     Show?   @relation(fields: [showId], references: [id])
  // If we ever need Client tasks:
  clientId BigInt?
  client   Client? @relation(fields: [clientId], references: [id])
}

// ❌ WRONG: Polymorphic Anti-Pattern
model Task {
  id           BigInt @id
  taskableId   BigInt // No FK constraint!
  taskableType String // "show", "client"
}
```

---

## 8. Nested Writes Pattern

**Rule**: Use Prisma's nested writes for atomic parent + child creation.

### When to Use

- Creating a parent record with related children in one transaction
- Simpler than manual transactions for single-parent scenarios
- Prisma handles the transaction automatically

### Implementation

```typescript
// Service method
async createTemplateWithSnapshot(payload: CreateTaskTemplatePayload): Promise<TaskTemplate> {
  const version = payload.version ?? 1;

  return this.repository.create({
    ...payload,
    uid: payload.uid ?? this.generateUid(),
    version,
    snapshots: {
      create: {
        version,
        schema: payload.currentSchema ?? {},
      },
    },
  });
}
```

### Nested Writes vs Transactions

| Pattern | Use When |
|---------|----------|
| **Nested Writes** | Single parent + direct children, simple relation |
| **Transactions** | Multiple parents, complex orchestration, external API calls |

---

## Related Skills

- **[Repository Pattern](../repository-pattern-nestjs/SKILL.md)**: How to wrap these patterns in a reusable class.
- **[Service Pattern](../service-pattern-nestjs/SKILL.md)**: Where to use Transactions and business logic.
