---
name: Integration Testing
description: Database integration testing patterns in LivestockAI
---

# Integration Testing

Integration tests verify database operations and constraints using a separate test database.

## Setup

### 1. Create Test Database

```bash
# Create database named: livestockai_test
# Via Neon Console or CLI
```

### 2. Set Environment Variable

```bash
# .env.test or .env
DATABASE_URL_TEST=postgres://user:pass@ep-xxx.neon.tech/livestockai_test?sslmode=require
```

### 3. Run Migrations

```bash
DATABASE_URL=$DATABASE_URL_TEST bun run db:migrate
```

### 4. Run Tests

```bash
bun run test:integration
```

## Test Helpers

Located in `tests/helpers/db-integration.ts`:

```typescript
import {
  getTestDb,
  truncateAllTables,
  seedTestUser,
  seedTestFarm,
  seedTestBatch,
  closeTestDb,
} from '../helpers/db-integration'
```

## Example Integration Test

```typescript
import { describe, it, expect, beforeEach, afterAll } from 'vitest'
import {
  getTestDb,
  truncateAllTables,
  seedTestUser,
  seedTestFarm,
  seedTestBatch,
  closeTestDb,
} from '../helpers/db-integration'

describe('Batch Integration Tests', () => {
  beforeEach(async () => {
    await truncateAllTables()
  })

  afterAll(async () => {
    await closeTestDb()
  })

  it('creates batch with correct data', async () => {
    const { userId } = await seedTestUser({ email: 'test@example.com' })
    const { farmId } = await seedTestFarm(userId)
    const { batchId } = await seedTestBatch(farmId, {
      species: 'Broiler',
      initialQuantity: 500,
    })

    const db = getTestDb()
    const batch = await db
      .selectFrom('batches')
      .where('id', '=', batchId)
      .executeTakeFirst()

    expect(batch).toBeDefined()
    expect(batch?.species).toBe('Broiler')
    expect(batch?.initialQuantity).toBe(500)
  })

  it('enforces foreign key constraints', async () => {
    const db = getTestDb()

    await expect(
      db
        .insertInto('batches')
        .values({
          farmId: 'non-existent-uuid',
          species: 'Broiler',
          initialQuantity: 100,
        })
        .execute(),
    ).rejects.toThrow()
  })
})
```

## Seeding Helpers

```typescript
// Create user with auth
const { userId } = await seedTestUser({
  email: 'test@example.com',
  password: 'password123',
  name: 'Test User',
})

// Create farm with modules
const { farmId } = await seedTestFarm(userId, {
  name: 'Test Farm',
  modules: ['poultry', 'fish'],
})

// Create batch
const { batchId } = await seedTestBatch(farmId, {
  species: 'Broiler',
  initialQuantity: 500,
  livestockType: 'poultry',
})
```

## Truncation Order

`truncateAllTables()` respects foreign key order:

1. Dependent tables first (sales, mortality_records, etc.)
2. Parent tables last (users, farms)

## Related Skills

- `vitest-patterns` - Unit testing
- `neon-database` - Database patterns
- `better-auth` - User creation
