---
name: write-model
description: Write database models following the Epic architecture patterns. Use when creating Active Record models for database tables with CRUD operations. Triggers on "create a model", "add a model", or "write a model for".
---

# Write Model

## Overview

This skill creates database models that follow the Epic three-layer architecture. Models belong to the **Infrastructure layer** and provide Active Record wrappers over Drizzle tables.

## Architecture Context

```
Backend: Actions call models
            |
            v
Infrastructure: Models (database operations)
                  |
                  v
              Drizzle ORM -> Database
```

Models:
- Run on the server (Infrastructure layer)
- Thin Active Record wrappers over Drizzle tables
- Handle ALL database operations
- May only be imported by Backend layer (Actions, Routes)
- NEVER imported by Frontend

## Model Location

```
shared/models/
  model-name.ts
```

## Class Specification Format

Follow the Epic Class specification format from `docs/Epic.md`:

```markdown
# ModelName

[Description of what this model manages]

## Properties
- db: Database

## Methods
- findAll(): Promise<ModelName[]>
- findById(id: string): Promise<ModelName | null>
- findByUserId(userId: string): Promise<ModelName[]>
- create(data: NewModelName): Promise<ModelName>
- update(id: string, data: Partial<NewModelName>): Promise<ModelName | null>
- delete(id: string): Promise<boolean>
```

## Implementation Pattern

```typescript
import { db } from '@/db/client';
import { modelNameTable, InsertModelName, SelectModelName } from '@/db/schema';
import { eq, and, isNull, desc } from 'drizzle-orm';

// Export the type for use in other files
export type ModelName = SelectModelName;

// Export the model object with all methods
export const ModelName = {
  async findAll(): Promise<ModelName[]> {
    return await db
      .select()
      .from(modelNameTable)
      .where(isNull(modelNameTable.deletedAt))
      .orderBy(desc(modelNameTable.createdAt));
  },

  async findById(id: string): Promise<ModelName | null> {
    const results = await db
      .select()
      .from(modelNameTable)
      .where(
        and(
          eq(modelNameTable.id, id),
          isNull(modelNameTable.deletedAt)
        )
      )
      .limit(1);
    return results[0] || null;
  },

  async findByUserId(userId: string): Promise<ModelName[]> {
    return await db
      .select()
      .from(modelNameTable)
      .where(
        and(
          eq(modelNameTable.userId, userId),
          isNull(modelNameTable.deletedAt)
        )
      )
      .orderBy(desc(modelNameTable.createdAt));
  },

  async create(
    data: Omit<InsertModelName, 'id' | 'createdAt' | 'updatedAt'>
  ): Promise<ModelName> {
    const id = crypto.randomUUID();
    const now = new Date();

    const [created] = await db
      .insert(modelNameTable)
      .values({
        ...data,
        id,
        createdAt: now,
        updatedAt: now,
      })
      .returning();

    return created;
  },

  async update(
    id: string,
    data: Partial<Omit<InsertModelName, 'id' | 'createdAt'>>
  ): Promise<ModelName | null> {
    const [updated] = await db
      .update(modelNameTable)
      .set({
        ...data,
        updatedAt: new Date(),
      })
      .where(
        and(
          eq(modelNameTable.id, id),
          isNull(modelNameTable.deletedAt)
        )
      )
      .returning();

    return updated || null;
  },

  async delete(id: string): Promise<boolean> {
    // Soft delete
    const result = await db
      .update(modelNameTable)
      .set({
        deletedAt: new Date(),
        updatedAt: new Date(),
      })
      .where(eq(modelNameTable.id, id));

    return result.rowsAffected > 0;
  },
};
```

## Standard Methods

Every model should include:

| Method | Description |
|--------|-------------|
| `findAll()` | Returns all non-deleted records |
| `findById(id)` | Returns single record or null |
| `findByUserId(userId)` | Returns user-owned records |
| `create(data)` | Creates new record with UUID |
| `update(id, data)` | Updates record, returns updated or null |
| `delete(id)` | Soft deletes record |

## Key Patterns

### 1. Soft Delete Handling
```typescript
// Always filter out deleted records
.where(isNull(modelNameTable.deletedAt))

// Soft delete implementation
async delete(id: string): Promise<boolean> {
  const result = await db
    .update(modelNameTable)
    .set({ deletedAt: new Date(), updatedAt: new Date() })
    .where(eq(modelNameTable.id, id));
  return result.rowsAffected > 0;
}
```

### 2. ID and Timestamp Generation
```typescript
const id = crypto.randomUUID();
const now = new Date();

await db.insert(table).values({
  ...data,
  id,
  createdAt: now,
  updatedAt: now,
});
```

### 3. User-Scoped Queries
```typescript
async findByUserId(userId: string): Promise<ModelName[]> {
  return await db
    .select()
    .from(table)
    .where(and(
      eq(table.userId, userId),
      isNull(table.deletedAt)
    ));
}
```

### 4. Custom Query Methods
```typescript
async findActiveByUserId(userId: string): Promise<ModelName[]> {
  return await db
    .select()
    .from(table)
    .where(and(
      eq(table.userId, userId),
      eq(table.status, 'active'),
      isNull(table.deletedAt)
    ));
}
```

## Constraints

- Export both TypeScript type AND methods object
- Handle soft deletes if schema has `deletedAt`
- Generate UUIDs for new records
- Set `createdAt` and `updatedAt` automatically
- User-scoped resources need `findByUserId`
- NEVER import from Frontend or Backend layers

## Checklist

Before finalizing a model:
- [ ] Schema alignment: matches Drizzle schema exactly
- [ ] Type safety: all types properly defined and exported
- [ ] Soft delete: queries filter out deletedAt when present
- [ ] User scoping: findByUserId for user-owned resources
- [ ] Timestamps: createdAt/updatedAt handled automatically
- [ ] Consistency: patterns match existing models

## Example Specification

```markdown
# Project

Manages project records for user workspaces.

## Properties
- db: Database

## Methods
- findAll(): Promise<Project[]>
- findById(id: string): Promise<Project | null>
- findByUserId(userId: string): Promise<Project[]>
- findByNameAndUser(name: string, userId: string): Promise<Project | null>
- create(data: NewProject): Promise<Project>
- update(id: string, data: Partial<NewProject>): Promise<Project | null>
- delete(id: string): Promise<boolean>

## Relationships
- Composes: Database
```
