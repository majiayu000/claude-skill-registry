---
name: repository-pattern
description: Create and manage Dexie/IndexedDB repositories with type-safe interfaces, converters, and standardized CRUD operations. Use when (1) adding entity storage, (2) implementing save/load/delete operations, (3) designing database schema and indexes, (4) converting between database (Db*) and domain types, (5) handling database errors or migrations, (6) using existing repositories (SettingsRepository, WorkoutsRepository, TemplatesRepository, CustomExercisesRepository, BenchmarksRepository, ActiveWorkoutRepository). Triggers include "database", "repository", "save data", "fetch from database", "delete from storage", "database schema", "database table", "indexes", "migration", "persist", "convert workout", "converter", "buildPartialUpdate", "mock repository", "database error", "bulk operations", "import/export", or specific repository names.
---

# Repository Pattern

## Overview

This skill helps implement the repository pattern used in this workout tracker application. The pattern provides a clean abstraction over Dexie (IndexedDB) with type-safe interfaces, consistent error handling, and standardized CRUD operations.

## Architecture Overview

**Layered Approach:**
```
Interfaces → Implementations → Provider → Public API
    ↓              ↓              ↓           ↓
db/interfaces  db/impl/dexie  db/provider  db/index
```

**Flow:**
1. Define repository interface in `db/interfaces.ts`
2. Implement with Dexie in `db/implementations/dexie/[entity].ts`
3. Register in factory provider (`db/implementations/dexie/index.ts`)
4. Export public getter (`db/index.ts`)
5. Use in features via `getEntityRepository()`

## Core Workflow

Follow these 6 steps when creating a new repository:

### Step 1: Define Interface

Location: `src/db/interfaces.ts`

Define the repository interface with standard CRUD methods:

```typescript
export type EntityRepository = {
  getAll(): Promise<ReadonlyArray<DbEntity>>
  getById(id: string): Promise<DbEntity | undefined>
  create(entity: Omit<DbEntity, 'id' | 'createdAt'>): Promise<DbEntity>
  update(id: string, updates: Partial<Omit<DbEntity, 'id' | 'createdAt'>>): Promise<void>
  delete(id: string): Promise<void>
  // ... entity-specific queries
}
```

Add to `RepositoryProvider`:
```typescript
export type RepositoryProvider = {
  // ... existing
  entity: EntityRepository
}
```

**Guidelines:**
- Use `ReadonlyArray<T>` and `Readonly<T>` for arguments
- `getById` returns `undefined` (not throw) when not found
- `create` returns the created entity with generated ID
- `update` and `delete` return `void`
- Use `Omit<>` to exclude auto-generated fields (`id`, `createdAt`)

### Step 2: Add Schema Type

Location: `src/db/schema.ts`

Define database type with `Db` prefix:

```typescript
/**
 * Entity stored in database.
 * Uses null instead of undefined for explicit "no value" semantics.
 */
export type DbEntity = {
  id: string
  name: string
  value: string | null        // Use null, not undefined
  createdAt: number
  updatedAt: number | null    // null until first update
}
```

**Key Conventions:**
- **Always** use `Db` prefix for database types
- Use `null` for "no value" (not `undefined`)
- Store user input numbers as `string` (e.g., `kg: string`, `reps: string`)
- Use discriminated unions with `kind` property for variants
- Include type guards if needed: `export function isDbEntity(x: unknown): x is DbEntity`

### Step 3: Update Database Class

Location: `src/db/implementations/dexie/database.ts`

Add table and indexes:

```typescript
export class WorkoutTrackerDb extends Dexie {
  // ... existing tables
  entities!: Table<DbEntity, string>

  constructor() {
    super('WorkoutTracker')

    // Increment version number
    this.version(3).stores({
      // ... existing tables
      entities: 'id, name, createdAt',  // Index: primary + frequently queried fields
    })
  }
}
```

**Indexing Guidelines:**
- Always index primary key (automatic)
- Index fields used in `where()`, `orderBy()`, `equals()`
- Index foreign keys for joins
- Compound indexes for junction tables: `'[field1+field2], field1, field2'`

### Step 4: Implement Repository

Location: `src/db/implementations/dexie/[entity].ts`

Create factory function returning repository implementation:

```typescript
import type { EntityRepository } from '@/db/interfaces'
import type { DbEntity } from '@/db/schema'
import { createDatabaseError, tryCatch } from '@/lib/tryCatch'
import type { WorkoutTrackerDb } from './database'
import { generateId } from './database'

/**
 * Dexie implementation of EntityRepository.
 */
export function createDexieEntityRepository(db: WorkoutTrackerDb): EntityRepository {
  return {
    async getAll(): Promise<ReadonlyArray<DbEntity>> {
      const [error, entities] = await tryCatch(
        db.entities.orderBy('createdAt').reverse().toArray(),
      )
      if (error) {
        throw createDatabaseError('LOAD_FAILED', 'retrieve entities', error)
      }
      return entities
    },

    async getById(id: string): Promise<DbEntity | undefined> {
      const [error, entity] = await tryCatch(db.entities.get(id))
      if (error) {
        throw createDatabaseError('LOAD_FAILED', `retrieve entity with id ${id}`, error)
      }
      return entity
    },

    async create(
      entity: Omit<DbEntity, 'id' | 'createdAt'>,
    ): Promise<DbEntity> {
      const newEntity: DbEntity = {
        ...entity,
        id: generateId(),
        createdAt: Date.now(),
      }

      const [error] = await tryCatch(db.entities.add(newEntity))
      if (error) {
        throw createDatabaseError('SAVE_FAILED', 'create entity', error)
      }

      return newEntity
    },

    async update(
      id: string,
      updates: Partial<Omit<DbEntity, 'id' | 'createdAt'>>,
    ): Promise<void> {
      const [error, updatedCount] = await tryCatch(
        db.entities.update(id, {
          ...updates,
          updatedAt: Date.now(),  // Auto-inject timestamp
        }),
      )

      if (error) {
        throw createDatabaseError('SAVE_FAILED', `update entity with id ${id}`, error)
      }

      if (updatedCount === 0) {
        throw createDatabaseError('NOT_FOUND', `entity with id ${id} not found`)
      }
    },

    async delete(id: string): Promise<void> {
      const [error] = await tryCatch(db.entities.delete(id))
      if (error) {
        throw createDatabaseError('SAVE_FAILED', `delete entity with id ${id}`, error)
      }
      // Soft delete: no NOT_FOUND check
    },
  }
}
```

**Key Patterns:**
- Use `tryCatch()` wrapper for all operations (preferred pattern)
- Two-phase error checking: operation failure + not found
- Auto-inject timestamps: `createdAt`, `updatedAt`
- Use `generateId()` for new IDs
- Soft delete: no error if entity doesn't exist

### Step 5: Register in Factory Provider

Location: `src/db/implementations/dexie/index.ts`

Import and add to provider:

```typescript
import { createDexieEntityRepository } from './entity'

export function createDexieRepositoryProvider(): RepositoryProvider {
  return {
    activeWorkout: createDexieActiveWorkoutRepository(db),
    workouts: createDexieWorkoutsRepository(db),
    // ... existing repositories
    entity: createDexieEntityRepository(db),  // ADD THIS
  }
}
```

### Step 6: Export Public Getter

Location: `src/db/index.ts`

Add getter function:

```typescript
export function getEntityRepository(): EntityRepository {
  return getRepositoryProvider().entity
}
```

## Usage in Features

```typescript
import { getEntityRepository } from '@/db'
import type { DbEntity } from '@/db/schema'

export function useEntities() {
  const entities = ref<ReadonlyArray<DbEntity>>([])
  const entityRepo = getEntityRepository()

  async function loadEntities() {
    entities.value = await entityRepo.getAll()
  }

  async function createEntity(name: string, value: string | null) {
    const newEntity = await entityRepo.create({ name, value, updatedAt: null })
    entities.value = [...entities.value, newEntity]
  }

  async function updateEntity(id: string, updates: Partial<DbEntity>) {
    await entityRepo.update(id, updates)
    await loadEntities()
  }

  async function deleteEntity(id: string) {
    await entityRepo.delete(id)
    entities.value = entities.value.filter(e => e.id !== id)
  }

  onMounted(() => loadEntities())

  return {
    entities: readonly(entities),
    createEntity,
    updateEntity,
    deleteEntity,
  }
}
```

## Key Principles

### 1. Error Handling

**Preferred: tryCatch wrapper**
```typescript
const [error, result] = await tryCatch(operation)
if (error) {
  throw createDatabaseError('ERROR_CODE', 'description', error)
}
```

**Error codes:**
- `SAVE_FAILED` - Create, update, delete operations
- `LOAD_FAILED` - Read operations
- `NOT_FOUND` - Entity doesn't exist

### 2. Timestamp Management

Auto-inject timestamps in repository methods:
- `createdAt: Date.now()` in `create()`
- `updatedAt: Date.now()` in `update()`
- `lastUsedAt: Date.now()` when accessing entity

### 3. ID Generation

Always use `generateId()` from `database.ts`:
```typescript
import { generateId } from './database'

const newEntity = {
  ...entity,
  id: generateId(),  // crypto.randomUUID()
}
```

### 4. Soft Delete

Delete operations don't throw if entity doesn't exist:
```typescript
async delete(id: string): Promise<void> {
  await tryCatch(db.entities.delete(id))
  // No NOT_FOUND check - silent success
}
```

### 5. Type Safety

- Use `Readonly<T>` and `ReadonlyArray<T>` for function parameters
- Use `Omit<>` to exclude auto-generated fields
- Use discriminated unions with exhaustive checking
- Define type guards for runtime type checking

## File Reference

**Critical files when creating repository:**
- `src/db/interfaces.ts` - Interface definition + RepositoryProvider
- `src/db/schema.ts` - Db-prefixed type definitions
- `src/db/implementations/dexie/database.ts` - Table + indexes
- `src/db/implementations/dexie/[entity].ts` - Implementation
- `src/db/implementations/dexie/index.ts` - Factory registration
- `src/db/index.ts` - Public getter export

**Utility imports:**
- `@/lib/tryCatch` - Error handling utilities
- `@/db/implementations/dexie/database` - generateId()

## Detailed References

For complete examples and advanced patterns, see:

- **[references/examples.md](references/examples.md)** - Complete end-to-end examples:
  - Example 1: Simple CRUD repository (Notes)
  - Example 2: Complex transformations (Tags with many-to-many)
  - Example 3: Extending Settings with function overloads

- **[references/patterns.md](references/patterns.md)** - Detailed pattern catalog:
  - Error handling patterns (direct throw vs tryCatch)
  - CRUD patterns (getAll, create, update, delete, timestamps)
  - Type transformation patterns (helper utilities, deep cloning)
  - Advanced patterns (function overloads, singleton, transactions, bulk ops)
  - Schema design patterns (discriminated unions, indexing, embedded vs referenced)

## Common Scenarios

### Scenario 1: Simple CRUD Repository

Need basic storage for an entity? See **examples.md → Example 1 (Notes)**.

**Quick checklist:**
1. Define interface with getAll/getById/create/update/delete
2. Add DbEntity type with Db prefix
3. Add table with indexes
4. Implement using tryCatch pattern
5. Register and export

### Scenario 2: Complex Relationships

Need many-to-many relationships or complex queries? See **examples.md → Example 2 (Tags)**.

**Pattern:** Junction table + transaction handling + usage tracking.

### Scenario 3: Extending Settings

Adding new setting? See **examples.md → Example 3**.

**Pattern:** Add discriminated union member + function overload + default value.

### Scenario 4: Conversions Between Types

Need to convert between templates and workouts? See **patterns.md → Type Transformation Patterns**.

**Pattern:** Helper utilities with exhaustive switch statements.

### Scenario 5: Bulk Operations

Import/export or batch delete? See **patterns.md → Advanced Patterns → Bulk Operations**.

**Pattern:** Transactions + `Promise.all()` + `bulkAdd()`.

## Testing Support

Mock repositories for unit tests:
```typescript
import { createMockRepositories } from '@/__tests__/helpers/mockRepositories'

const mockRepos = createMockRepositories()
mockRepos.entity.getAll.mockResolvedValue([...])
```

Integration tests with fake-indexeddb are automatically set up via test helpers.

## Migration Strategy

When updating schema version:
1. Increment version number in `database.ts`
2. Add new table/indexes in `.stores({})`
3. Dexie handles migrations automatically
4. For data migrations, use `.upgrade()` callback

```typescript
this.version(3)
  .stores({
    entities: 'id, name, createdAt',
  })
  .upgrade(tx => {
    // Optional data migration logic
    return tx.table('entities').toCollection().modify(entity => {
      entity.newField = 'default'
    })
  })
```

## Project-Specific Repositories

### `Db*` Types vs Domain Types

| Aspect | Database (`Db*`) | Domain |
|--------|------------------|--------|
| File | `src/db/schema.ts` | `src/types/` |
| Prefix | `DbWorkout`, `DbSet` | `Workout`, `Set` |
| No value | `null` | `undefined` |
| Optimized for | Storage | App logic |

### Available Repositories

**SettingsRepository** - Key-value store with defaults:
```ts
const repo = getSettingsRepository()
await repo.get('theme')           // 'light' | 'dark' | 'system'
await repo.get('defaultRestTimer') // number
await repo.set({ key: 'theme', value: 'dark' })
await repo.getAll()               // All settings merged with defaults
await repo.reset('theme')
```

**CustomExercisesRepository** - Exercise CRUD:
```ts
const repo = getCustomExercisesRepository()
await repo.getAll()
await repo.getById(id)
await repo.add({ id: generateId(), name: 'Squat', ... })
await repo.update(id, { name: 'Back Squat' })
await repo.delete(id)
```

**WorkoutsRepository** - Completed workouts:
```ts
const repo = getWorkoutsRepository()
await repo.getAll()
await repo.getById(id)
await repo.create(convertWorkoutToDb(workout))
await repo.delete(id)
```

**ActiveWorkoutRepository** - Singleton active workout:
```ts
const repo = getActiveWorkoutRepository()
await repo.load()
await repo.save(dbActiveWorkout)
await repo.delete()
await repo.exists()
```

**BenchmarksRepository** - Benchmark workouts:
```ts
const repo = getBenchmarksRepository()
await repo.getAll()
await repo.getById(id)
await repo.create({ id: generateId(), name: 'Fran', ... })
await repo.update(id, { name: 'Fran (Scaled)' })
await repo.delete(id)
```

**TemplatesRepository** - Workout templates:
```ts
const repo = getTemplatesRepository()
await repo.getAll()
await repo.getById(id)
await repo.create(template)
await repo.update(id, changes)
await repo.delete(id)
```

### Using Converters

Always convert when crossing domain/database boundary:

```ts
import { convertWorkoutToDb, convertDbToWorkout } from '@/db/converters'

// Domain → Database
const dbWorkout = convertWorkoutToDb(workout)
await getWorkoutsRepository().create(dbWorkout)

// Database → Domain
const dbWorkout = await getWorkoutsRepository().getById(id)
const workout = convertDbToWorkout(dbWorkout)
```

### Partial Updates with buildPartialUpdate

Dexie's `update()` overwrites all keys in the object. Use `buildPartialUpdate` to only modify provided fields:

```ts
import { buildPartialUpdate } from '@/db/partialUpdate'

const NULLABLE_FIELDS = ['equipment', 'muscle', 'image']

// Only includes keys present in updates
// Converts undefined → null for nullable fields
const dbUpdates = buildPartialUpdate(updates, NULLABLE_FIELDS)
await repo.update(id, dbUpdates)
```

**Why**: Without filtering, `{ name: 'Squat', equipment: undefined }` would set equipment to null even if you only meant to update the name.

## Project-Specific Gotchas

### 1. Use `null` in Database, `undefined` in Domain

IndexedDB doesn't support `undefined`:

```ts
// Database types
type DbExercise = {
  equipment: Equipment | null  // Use null
}

// Domain types
type Exercise = {
  equipment?: Equipment  // Use undefined
}
```

### 2. Always Reset Database in Tests

```ts
import { resetDatabase } from '@/__tests__/setup'

beforeEach(async () => {
  await resetDatabase()
})
```

### 3. Convert Types at Boundaries

```ts
// BAD - Type mismatch
await getWorkoutsRepository().create(workout)

// GOOD - Convert first
const dbWorkout = convertWorkoutToDb(workout)
await getWorkoutsRepository().create(dbWorkout)
```
