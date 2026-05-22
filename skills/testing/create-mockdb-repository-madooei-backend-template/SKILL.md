---
name: create-mockdb-repository
description: Create MockDB (in-memory) repository implementation for development and testing. Use when implementing repository interface with mock database, creating in-memory data store, or setting up test fixtures. Triggers on "mockdb repository", "mock repository", "in-memory repository", "test repository implementation".
---

# Create MockDB Repository

Creates an in-memory repository implementation using an array as the data store. Ideal for development, testing, and prototyping.

## Quick Reference

**Location**: `src/repositories/mockdb/{entity-name}.mockdb.repository.ts`
**Naming**: `{entity-name}.mockdb.repository.ts` (e.g., `note.mockdb.repository.ts`)

## Instructions

### Step 1: Create the Implementation File

Create `src/repositories/mockdb/{entity-name}.mockdb.repository.ts`

### Step 2: Import Dependencies

```typescript
import { v4 as uuidv4 } from "uuid";
import type {
  {Entity}Type,
  Create{Entity}Type,
  Update{Entity}Type,
  {Entity}QueryParamsType,
  {Entity}IdType,
} from "@/schemas/{entity-name}.schema";
import {
  DEFAULT_LIMIT,
  DEFAULT_PAGE,
  type PaginatedResultType,
} from "@/schemas/shared.schema";
import type { I{Entity}Repository } from "@/repositories/{entity-name}.repository";
import type { UserIdType } from "@/schemas/user.schemas";
```

### Step 3: Create the Class

```typescript
export class MockDb{Entity}Repository implements I{Entity}Repository {
  private {entities}: {Entity}Type[] = [];

  // Helper method for filtering, pagination, and sorting
  private applyQueryParams(
    {entities}: {Entity}Type[],
    params: {Entity}QueryParamsType,
  ): PaginatedResultType<{Entity}Type> {
    let filtered = {entities};

    // Apply entity-specific filters
    if (params.createdBy) {
      filtered = filtered.filter((item) => item.createdBy === params.createdBy);
    }

    // Apply search filter
    const searchTerm = params.search?.toLowerCase().trim();
    if (searchTerm) {
      filtered = filtered.filter((item) =>
        item.{searchableField}.toLowerCase().includes(searchTerm)
      );
    }

    // Pagination
    const page = params.page ?? DEFAULT_PAGE;
    const limit = params.limit ?? DEFAULT_LIMIT;
    const skip = (page - 1) * limit;
    let paginated = filtered.slice(skip, skip + limit);
    const totalPages = Math.ceil(filtered.length / limit);

    // Sorting
    const sortBy = (params.sortBy ?? "createdAt") as keyof {Entity}Type;
    const sortOrder = params.sortOrder;
    if (sortBy) {
      paginated = paginated.sort((a, b) => {
        if (sortOrder === "asc") {
          return a[sortBy]?.toString().localeCompare(b[sortBy]?.toString() ?? "") ?? 0;
        } else if (sortOrder === "desc") {
          return b[sortBy]?.toString().localeCompare(a[sortBy]?.toString() ?? "") ?? 0;
        }
        return 0;
      });
    }

    return {
      data: paginated,
      total: filtered.length,
      page,
      limit,
      totalPages,
    };
  }

  async findAll(params: {Entity}QueryParamsType): Promise<PaginatedResultType<{Entity}Type>> {
    return this.applyQueryParams(this.{entities}, params);
  }

  async findById(id: {Entity}IdType): Promise<{Entity}Type | null> {
    const item = this.{entities}.find((e) => e.id === id);
    return item || null;
  }

  async findAllByIds(
    ids: {Entity}IdType[],
    params: {Entity}QueryParamsType,
  ): Promise<PaginatedResultType<{Entity}Type>> {
    const filtered = this.{entities}.filter((item) => ids.includes(item.id));
    return this.applyQueryParams(filtered, params);
  }

  async create(
    data: Create{Entity}Type,
    createdByUserId: UserIdType,
  ): Promise<{Entity}Type> {
    const now = new Date();
    const new{Entity}: {Entity}Type = {
      id: uuidv4(),
      ...data,
      createdBy: createdByUserId,
      createdAt: now,
      updatedAt: now,
    };
    this.{entities}.push(new{Entity});
    return new{Entity};
  }

  async update(id: {Entity}IdType, data: Update{Entity}Type): Promise<{Entity}Type | null> {
    const index = this.{entities}.findIndex((e) => e.id === id);
    if (index === -1) {
      return null;
    }
    const existing = this.{entities}[index];
    const updated = {
      ...existing,
      ...data,
      updatedAt: new Date(),
    };
    this.{entities}[index] = updated;
    return updated;
  }

  async remove(id: {Entity}IdType): Promise<boolean> {
    const initialLength = this.{entities}.length;
    this.{entities} = this.{entities}.filter((e) => e.id !== id);
    return this.{entities}.length < initialLength;
  }

  // Helper method for testing: clear all data
  clear(): void {
    this.{entities} = [];
  }
}
```

## Patterns & Rules

### Class Naming

- **Class name**: `MockDb{Entity}Repository` (e.g., `MockDbNoteRepository`)
- **Implements**: `I{Entity}Repository` interface

### Private Data Store

```typescript
private {entities}: {Entity}Type[] = [];
```

Use a descriptive plural name for the array (e.g., `notes`, `courses`, `users`).

### ID Generation

Use `uuid` for generating unique IDs:

```typescript
import { v4 as uuidv4 } from "uuid";

// In create method:
id: uuidv4(),
```

### Timestamp Handling

Always set timestamps in create and update:

```typescript
// Create
const now = new Date();
createdAt: now,
updatedAt: now,

// Update
updatedAt: new Date(),
```

### The `applyQueryParams` Helper

This private method handles:

1. **Filtering** - Entity-specific filters (createdBy, status, etc.)
2. **Search** - Text search on searchable fields
3. **Pagination** - Skip and limit calculations
4. **Sorting** - Sort by field and order

### Testing Helper

Always include a `clear()` method for test cleanup:

```typescript
clear(): void {
  this.{entities} = [];
}
```

## Complete Example

See [REFERENCE.md](REFERENCE.md) for a full implementation example including:

- Complete `MockDbNoteRepository` class
- Custom method example (`findAllByIds`)
- Usage in tests with `clear()` helper

## What NOT to Do

- Do NOT add database connection logic - MockDB is in-memory only
- Do NOT validate with Zod in MockDB - that's the MongoDB pattern for document mapping
- Do NOT throw errors for not-found cases - return null/false
- Do NOT forget the `clear()` helper - tests need it
- Do NOT use synchronous methods - keep them async for interface compatibility
