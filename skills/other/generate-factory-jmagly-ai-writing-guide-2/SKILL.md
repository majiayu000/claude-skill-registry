---
name: generate-factory
description: Auto-generate test data factories from schemas, types, or models. Use when creating test data infrastructure, setting up fixtures, or reducing test setup boilerplate.
version: 1.0.0
---

# Generate Factory Skill

## Purpose

Auto-generate test data factories from database schemas, TypeScript interfaces, or model definitions. Factories produce realistic test data using Faker.js patterns, reducing test setup time by 60%.

## Research Foundation

| Pattern | Source | Reference |
|---------|--------|-----------|
| Factory Pattern | ThoughtBot | [FactoryBot](https://github.com/thoughtbot/factory_bot) |
| Faker.js | Open Source | [fakerjs.dev](https://fakerjs.dev/) |
| Test Data Management | ISTQB | CT-TAS Test Automation Strategy |
| Synthetic Data | Tonic.ai | [Faker Best Practices](https://www.tonic.ai/blog/how-to-generate-simple-test-data-with-faker) |

## When This Skill Applies

- User needs to create test data factories
- Setting up test infrastructure for new project
- Existing tests use hard-coded data
- Schema/model changes require test data updates
- Need realistic but deterministic test data

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Generate factory for User model" | Create user factory |
| "Create test data factories" | Generate factories for all models |
| "Add faker to tests" | Integrate faker with existing tests |
| "Make test data realistic" | Convert hard-coded to factory |
| "Generate fixtures from schema" | Schema-aware factory generation |

## Factory Concepts

### Factory vs Fixture vs Mock

| Type | Purpose | When to Use |
|------|---------|-------------|
| **Factory** | Generate dynamic test data | When you need many variations |
| **Fixture** | Static, predefined data | When exact values matter |
| **Mock** | Fake external dependencies | When isolating units |

### Factory Features

```typescript
// Basic factory
const user = userFactory.build();
// { id: 'uuid-1', name: 'John Doe', email: 'john@example.com' }

// With overrides
const admin = userFactory.build({ role: 'admin' });
// { id: 'uuid-2', name: 'Jane Doe', email: 'jane@example.com', role: 'admin' }

// Build multiple
const users = userFactory.buildList(5);
// Array of 5 users

// With traits
const inactiveUser = userFactory.build({}, { trait: 'inactive' });
// { id: 'uuid-3', ..., status: 'inactive', deactivatedAt: Date }

// With relationships
const userWithOrders = userFactory.build({}, { with: ['orders'] });
// { id: 'uuid-4', ..., orders: [{ id: 'order-1', ... }] }
```

## Generation Process

### 1. Analyze Source

Detect schema/type from:
- TypeScript interfaces
- Prisma schema
- JSON Schema
- Database migrations
- OpenAPI specs

```typescript
// Input: TypeScript interface
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
  role: 'admin' | 'user' | 'guest';
  createdAt: Date;
  preferences?: UserPreferences;
}
```

### 2. Map Types to Faker

```typescript
const TYPE_MAPPING = {
  // Primitives
  'string': 'faker.string.alphanumeric(10)',
  'number': 'faker.number.int({ min: 0, max: 100 })',
  'boolean': 'faker.datatype.boolean()',
  'Date': 'faker.date.past()',

  // Named fields (semantic mapping)
  'id': 'faker.string.uuid()',
  'name': 'faker.person.fullName()',
  'email': 'faker.internet.email()',
  'phone': 'faker.phone.number()',
  'address': 'faker.location.streetAddress()',
  'age': 'faker.number.int({ min: 18, max: 80 })',
  'createdAt': 'faker.date.past()',
  'updatedAt': 'faker.date.recent()',

  // Enums
  'role': 'faker.helpers.arrayElement(["admin", "user", "guest"])',
};
```

### 3. Generate Factory

```typescript
// Generated: factories/user.factory.ts
import { faker } from '@faker-js/faker';
import type { User } from '../types';

export const userFactory = {
  /**
   * Build a single User with optional overrides
   */
  build: (overrides: Partial<User> = {}): User => ({
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    age: faker.number.int({ min: 18, max: 80 }),
    role: faker.helpers.arrayElement(['admin', 'user', 'guest']),
    createdAt: faker.date.past(),
    ...overrides,
  }),

  /**
   * Build multiple Users
   */
  buildList: (count: number, overrides: Partial<User> = {}): User[] =>
    Array.from({ length: count }, () => userFactory.build(overrides)),

  /**
   * Traits for common variations
   */
  traits: {
    admin: { role: 'admin' as const },
    inactive: {
      status: 'inactive',
      deactivatedAt: faker.date.past(),
    },
    newUser: {
      createdAt: faker.date.recent(),
    },
  },

  /**
   * Build with trait
   */
  buildWithTrait: (trait: keyof typeof userFactory.traits, overrides: Partial<User> = {}): User =>
    userFactory.build({ ...userFactory.traits[trait], ...overrides }),
};
```

### 4. Generate Related Factories

For entities with relationships:

```typescript
// factories/order.factory.ts
import { faker } from '@faker-js/faker';
import { userFactory } from './user.factory';

export const orderFactory = {
  build: (overrides = {}) => ({
    id: faker.string.uuid(),
    userId: faker.string.uuid(),
    items: [],
    total: faker.number.float({ min: 10, max: 500, fractionDigits: 2 }),
    status: faker.helpers.arrayElement(['pending', 'shipped', 'delivered']),
    createdAt: faker.date.past(),
    ...overrides,
  }),

  /**
   * Build with related user
   */
  buildWithUser: (overrides = {}) => {
    const user = userFactory.build();
    return {
      ...orderFactory.build({ userId: user.id, ...overrides }),
      user,
    };
  },
};
```

## Output Format

```markdown
## Factory Generation Report

**Source**: `src/types/user.ts`
**Output**: `test/factories/user.factory.ts`

### Generated Factory

```typescript
import { faker } from '@faker-js/faker';
import type { User } from '../../src/types';

export const userFactory = {
  build: (overrides: Partial<User> = {}): User => ({
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    age: faker.number.int({ min: 18, max: 80 }),
    role: faker.helpers.arrayElement(['admin', 'user', 'guest']),
    createdAt: faker.date.past(),
    preferences: null,
    ...overrides,
  }),

  buildList: (count: number, overrides: Partial<User> = {}): User[] =>
    Array.from({ length: count }, () => userFactory.build(overrides)),

  traits: {
    admin: { role: 'admin' as const },
    inactive: { status: 'inactive' },
  },
};
```

### Field Mappings

| Field | Type | Faker Method |
|-------|------|--------------|
| id | string | `faker.string.uuid()` |
| name | string | `faker.person.fullName()` |
| email | string | `faker.internet.email()` |
| age | number | `faker.number.int({ min: 18, max: 80 })` |
| role | enum | `faker.helpers.arrayElement([...])` |
| createdAt | Date | `faker.date.past()` |

### Usage Examples

```typescript
// Basic usage
const user = userFactory.build();

// With override
const admin = userFactory.build({ role: 'admin' });

// Multiple users
const users = userFactory.buildList(10);

// With trait
const inactive = userFactory.build(userFactory.traits.inactive);
```

### Dependencies Added

```json
{
  "devDependencies": {
    "@faker-js/faker": "^8.0.0"
  }
}
```
```

## Deterministic Mode

For tests requiring reproducible data:

```typescript
// Set seed for reproducible data
import { faker } from '@faker-js/faker';

beforeEach(() => {
  faker.seed(12345);  // Same data every run
});

// Or per-factory
export const userFactory = {
  buildDeterministic: (seed: number, overrides = {}) => {
    faker.seed(seed);
    return userFactory.build(overrides);
  },
};
```

## Batch Generation

Generate factories for all models:

```bash
# From Prisma schema
npx generate-factory --source prisma/schema.prisma --output test/factories/

# From TypeScript types
npx generate-factory --source src/types/ --output test/factories/
```

## Integration Points

- Works with `tdd-enforce` for test data requirements
- Used by Test Engineer for test creation
- Feeds into integration test setup
- Compatible with database seeders

## Script Reference

### factory_generator.py
Generate factory from schema:
```bash
python scripts/factory_generator.py --source src/types/user.ts
```

### batch_generate.py
Generate all factories:
```bash
python scripts/batch_generate.py --source src/types/ --output test/factories/
```
