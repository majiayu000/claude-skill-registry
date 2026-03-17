---
name: create-repository
description: Create repository interface for data access abstraction. Use when adding a new resource that needs database operations, defining CRUD interface, or setting up repository pattern. Triggers on "new repository", "repository interface", "data access layer", "create repository".
---

# Create Repository Interface

Creates the repository interface that defines data access operations for an entity. Implementations (MockDB, MongoDB, etc.) will implement this interface.

## Quick Reference

**Location**: `src/repositories/{entity-name}.repository.ts`
**Naming**: Singular, kebab-case (e.g., `note.repository.ts`, `course.repository.ts`)

## Instructions

### Step 1: Create the Interface File

Create `src/repositories/{entity-name}.repository.ts`

### Step 2: Import Schema Types

```typescript
import type {
  {Entity}Type,
  Create{Entity}Type,
  Update{Entity}Type,
  {Entity}QueryParamsType,
  {Entity}IdType,
} from "@/schemas/{entity-name}.schema";
import type { PaginatedResultType } from "@/schemas/shared.schema";
import type { UserIdType } from "@/schemas/user.schemas";
```

### Step 3: Define the Interface

```typescript
export interface I{Entity}Repository {
  findAll(params: {Entity}QueryParamsType): Promise<PaginatedResultType<{Entity}Type>>;
  findById(id: {Entity}IdType): Promise<{Entity}Type | null>;
  create(data: Create{Entity}Type, createdByUserId: UserIdType): Promise<{Entity}Type>;
  update(id: {Entity}IdType, data: Update{Entity}Type): Promise<{Entity}Type | null>;
  remove(id: {Entity}IdType): Promise<boolean>;
}
```

## Standard CRUD Methods

Every repository interface should include these standard CRUD methods:

| Method     | Parameters                 | Returns                                    | Description                    |
| ---------- | -------------------------- | ------------------------------------------ | ------------------------------ |
| `findAll`  | `params: QueryParamsType`  | `Promise<PaginatedResultType<EntityType>>` | List with pagination/filtering |
| `findById` | `id: EntityIdType`         | `Promise<EntityType \| null>`              | Single entity or null          |
| `create`   | `data: CreateType, userId` | `Promise<EntityType>`                      | Create and return new entity   |
| `update`   | `id, data: UpdateType`     | `Promise<EntityType \| null>`              | Update and return, or null     |
| `remove`   | `id: EntityIdType`         | `Promise<boolean>`                         | True if deleted                |

## Patterns & Rules

### Naming Conventions

- **Interface name**: `I{Entity}Repository` (e.g., `INoteRepository`, `ICourseRepository`)
- **File name**: `{entity-name}.repository.ts` (singular, kebab-case)

### Return Type Patterns

- **Single entity lookups**: Return `EntityType | null` (null if not found)
- **List operations**: Return `PaginatedResultType<EntityType>` (always, even if empty)
- **Create operations**: Return the created `EntityType` (with generated ID and timestamps)
- **Update operations**: Return `EntityType | null` (null if entity doesn't exist)
- **Delete operations**: Return `boolean` (true if deleted, false if not found)

### Parameter Patterns

- **Create method**: Takes `Create{Entity}Type` + `createdByUserId: UserIdType`
- **Update method**: Takes `id` separately (from URL) + `Update{Entity}Type` (from body)
- **Query methods**: Take `{Entity}QueryParamsType` for filtering/pagination

### Import Rules

- Always use path aliases: `@/schemas/...`, `@/repositories/...`
- Import types with `import type { ... }` for type-only imports
- Import from specific schema files, not barrel exports

## Adding Custom Methods

Add custom methods based on your system's requirements. Common patterns include:

### Query by Attribute (`findByX`)

Find entities by a specific attribute:

```typescript
findByStatus(status: StatusType, params: {Entity}QueryParamsType): Promise<PaginatedResultType<{Entity}Type>>;
findByOwner(ownerId: UserIdType, params: {Entity}QueryParamsType): Promise<PaginatedResultType<{Entity}Type>>;
findByCategory(categoryId: CategoryIdType, params: {Entity}QueryParamsType): Promise<PaginatedResultType<{Entity}Type>>;
```

### Batch Operations

Operate on multiple entities at once:

```typescript
// Batch queries
findAllByIds(ids: {Entity}IdType[], params: {Entity}QueryParamsType): Promise<PaginatedResultType<{Entity}Type>>;
findAllByStatus(status: StatusType, params: {Entity}QueryParamsType): Promise<PaginatedResultType<{Entity}Type>>;

// Batch mutations
createMany(data: Create{Entity}Type[], createdByUserId: UserIdType): Promise<{Entity}Type[]>;
updateMany(ids: {Entity}IdType[], data: Update{Entity}Type): Promise<number>; // returns count updated
removeMany(ids: {Entity}IdType[]): Promise<number>; // returns count deleted
removeByOwner(ownerId: UserIdType): Promise<number>; // returns count deleted
```

### Aggregation Operations

Get counts or summaries without fetching full entities:

```typescript
countByStatus(status: StatusType): Promise<number>;
countByOwner(ownerId: UserIdType): Promise<number>;
```

## Complete Example

```typescript
import type {
  NoteType,
  CreateNoteType,
  UpdateNoteType,
  NoteQueryParamsType,
  NoteIdType,
} from "@/schemas/note.schema";
import type { PaginatedResultType } from "@/schemas/shared.schema";
import type { UserIdType } from "@/schemas/user.schemas";

export interface INoteRepository {
  // Standard CRUD
  findAll(params: NoteQueryParamsType): Promise<PaginatedResultType<NoteType>>;
  findById(id: NoteIdType): Promise<NoteType | null>;
  create(data: CreateNoteType, createdByUserId: UserIdType): Promise<NoteType>;
  update(id: NoteIdType, data: UpdateNoteType): Promise<NoteType | null>;
  remove(id: NoteIdType): Promise<boolean>;

  // Custom methods (assuming it was needed)
  findAllByIds(
    ids: NoteIdType[],
    params: NoteQueryParamsType,
  ): Promise<PaginatedResultType<NoteType>>;
}
```

## Next Steps

After creating the interface, create an implementation:

- **For development/testing**: Use `create-mockdb-repository` skill
- **For production**: Use `create-mongodb-repository` skill

## What NOT to Do

- Do NOT include implementation details in the interface
- Do NOT use concrete types (use the interface for dependency injection)
- Do NOT add business logic - repositories only handle data access
- Do NOT throw domain errors - return null/false and let the service handle it
- Do NOT use plural naming (`notes.repository.ts`) - use singular (`note.repository.ts`)
