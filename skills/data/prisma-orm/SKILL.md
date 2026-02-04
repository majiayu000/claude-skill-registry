---
name: prisma-orm
description: Type-safe database access with Prisma ORM. Covers schema design, migrations, relations, queries, and TypeScript integration. Use when working with Prisma, database modeling, or building type-safe data layers for Node.js/TypeScript projects.
---

# Prisma ORM Skill

## Triggers

Use this skill when:
- Setting up Prisma in a Node.js/TypeScript project
- Designing Prisma schemas with models, relations, and enums
- Creating and managing database migrations
- Writing Prisma Client queries (CRUD, filtering, aggregations)
- Implementing raw SQL queries with Prisma
- Working with database transactions
- Building type-safe repository patterns
- Testing with Prisma (factories, mocking)
- Keywords: prisma, orm, database, typescript, schema, migrations, prisma client, type-safe queries, relations

## Overview

Prisma is a next-generation Node.js and TypeScript ORM that provides:
- **Prisma Schema**: Declarative data modeling language
- **Prisma Migrate**: Database migration system
- **Prisma Client**: Auto-generated, type-safe query builder
- **Prisma Studio**: GUI for database exploration

## Quick Start

```bash
# Initialize Prisma in a project
npm install prisma --save-dev
npm install @prisma/client
npx prisma init

# Common commands
npx prisma generate      # Generate Prisma Client
npx prisma migrate dev   # Create and apply migrations
npx prisma db push       # Push schema without migrations (dev)
npx prisma studio        # Open database GUI
npx prisma db seed       # Run seed script
```

---

## Schema Design

### Basic Model Structure

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql" // mysql, sqlite, sqlserver, mongodb
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@map("users") // Custom table name
}
```

### Field Types & Modifiers

```prisma
model Example {
  // Scalar types
  id          Int       @id @default(autoincrement())
  uuid        String    @id @default(uuid())
  cuid        String    @id @default(cuid())
  name        String    @db.VarChar(255)
  content     String    @db.Text
  count       Int       @default(0)
  price       Decimal   @db.Decimal(10, 2)
  rating      Float
  isActive    Boolean   @default(true)
  data        Json
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  // Optional field
  deletedAt   DateTime?

  // Unique constraint
  slug        String    @unique

  // Composite unique
  @@unique([categoryId, slug])

  // Composite index
  @@index([createdAt, isActive])
}
```

### Enums

```prisma
enum Role {
  USER
  ADMIN
  MODERATOR
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

model User {
  id   String @id @default(cuid())
  role Role   @default(USER)
}
```

### Relations

```prisma
// One-to-One
model User {
  id      String   @id @default(cuid())
  profile Profile?
}

model Profile {
  id     String @id @default(cuid())
  bio    String
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId String @unique
}

// One-to-Many
model User {
  id    String @id @default(cuid())
  posts Post[]
}

model Post {
  id       String @id @default(cuid())
  title    String
  author   User   @relation(fields: [authorId], references: [id])
  authorId String
}

// Many-to-Many (implicit)
model Post {
  id         String     @id @default(cuid())
  categories Category[]
}

model Category {
  id    String @id @default(cuid())
  name  String
  posts Post[]
}

// Many-to-Many (explicit - for extra fields)
model Post {
  id       String        @id @default(cuid())
  tags     PostTag[]
}

model Tag {
  id    String    @id @default(cuid())
  name  String    @unique
  posts PostTag[]
}

model PostTag {
  post      Post     @relation(fields: [postId], references: [id])
  postId    String
  tag       Tag      @relation(fields: [tagId], references: [id])
  tagId     String
  assignedAt DateTime @default(now())
  assignedBy String

  @@id([postId, tagId])
}

// Self-relation
model Category {
  id       String     @id @default(cuid())
  name     String
  parent   Category?  @relation("CategoryHierarchy", fields: [parentId], references: [id])
  parentId String?
  children Category[] @relation("CategoryHierarchy")
}
```

---

## Migrations

### Development Workflow

```bash
# Create migration from schema changes
npx prisma migrate dev --name add_user_table

# Apply migrations without creating new ones
npx prisma migrate deploy

# Reset database (drops all data!)
npx prisma migrate reset

# Check migration status
npx prisma migrate status

# Resolve failed migration
npx prisma migrate resolve --applied "20240115120000_migration_name"
```

---

## Prisma Client Queries

### Setup & Instantiation

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development'
    ? ['query', 'error', 'warn']
    : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}

export default prisma;
```

### CRUD Operations

```typescript
import { prisma } from './lib/prisma';

// CREATE
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John Doe',
    profile: {
      create: { bio: 'Hello world' }, // Nested create
    },
  },
});

// Create many
const users = await prisma.user.createMany({
  data: [
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
  ],
  skipDuplicates: true,
});

// READ - Find unique
const user = await prisma.user.findUnique({
  where: { id: 'cuid123' },
});

// Find unique or throw
const user = await prisma.user.findUniqueOrThrow({
  where: { email: 'user@example.com' },
});

// Find first
const user = await prisma.user.findFirst({
  where: { role: 'ADMIN' },
  orderBy: { createdAt: 'desc' },
});

// Find many with pagination
const users = await prisma.user.findMany({
  where: { isActive: true },
  orderBy: { name: 'asc' },
  skip: 0,
  take: 10,
});

// UPDATE
const user = await prisma.user.update({
  where: { id: 'cuid123' },
  data: { name: 'Updated Name' },
});

// Upsert (create or update)
const user = await prisma.user.upsert({
  where: { email: 'user@example.com' },
  update: { name: 'Updated Name' },
  create: { email: 'user@example.com', name: 'New User' },
});

// DELETE
const user = await prisma.user.delete({
  where: { id: 'cuid123' },
});
```

### Filtering

```typescript
// Comparison operators
const users = await prisma.user.findMany({
  where: {
    age: { gt: 18 },           // greater than
    score: { gte: 90 },        // greater than or equal
    price: { lt: 100 },        // less than
    count: { lte: 10 },        // less than or equal
    status: { not: 'DELETED' }, // not equal
    role: { in: ['ADMIN', 'MODERATOR'] },
    type: { notIn: ['SPAM', 'BOT'] },
  },
});

// String filters
const users = await prisma.user.findMany({
  where: {
    email: { contains: '@example.com' },
    name: { startsWith: 'John' },
    bio: { endsWith: 'developer' },
    // Case insensitive (PostgreSQL, MySQL)
    email: { contains: 'JOHN', mode: 'insensitive' },
  },
});

// Logical operators
const users = await prisma.user.findMany({
  where: {
    AND: [
      { isActive: true },
      { role: 'ADMIN' },
    ],
    OR: [
      { email: { contains: '@company.com' } },
      { role: 'ADMIN' },
    ],
    NOT: {
      deletedAt: { not: null },
    },
  },
});

// Relation filters
const posts = await prisma.post.findMany({
  where: {
    author: {
      email: { contains: '@example.com' },
    },
    comments: {
      some: { isApproved: true },  // At least one
      every: { isSpam: false },    // All must match
      none: { isSpam: true },      // None must match
    },
  },
});
```

### Select & Include (Relations)

```typescript
// Select specific fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    name: true,
    // Nested select
    posts: {
      select: { id: true, title: true },
      take: 5,
    },
  },
});

// Include relations
const user = await prisma.user.findUnique({
  where: { id: 'cuid123' },
  include: {
    profile: true,
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
      take: 10,
      include: {
        comments: {
          take: 3,
          orderBy: { createdAt: 'desc' },
        },
      },
    },
  },
});

// Count relations
const usersWithCounts = await prisma.user.findMany({
  include: {
    _count: {
      select: { posts: true, followers: true },
    },
  },
});
```

### Aggregations

```typescript
// Count
const userCount = await prisma.user.count({
  where: { isActive: true },
});

// Aggregate
const stats = await prisma.order.aggregate({
  _sum: { amount: true },
  _avg: { amount: true },
  _min: { amount: true },
  _max: { amount: true },
  _count: true,
  where: { status: 'COMPLETED' },
});

// Group by
const ordersByStatus = await prisma.order.groupBy({
  by: ['status'],
  _count: true,
  _sum: { amount: true },
  having: {
    amount: { _sum: { gt: 1000 } },
  },
});
```

---

## Transactions

```typescript
// Sequential operations (auto-rollback on error)
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'user@example.com' } }),
  prisma.post.create({ data: { title: 'Hello', authorId: 'existing-id' } }),
]);

// Interactive transaction (full control)
const result = await prisma.$transaction(async (tx) => {
  // Decrement sender balance
  const sender = await tx.account.update({
    where: { id: senderId },
    data: { balance: { decrement: amount } },
  });

  if (sender.balance < 0) {
    throw new Error('Insufficient funds');
  }

  // Increment recipient balance
  const recipient = await tx.account.update({
    where: { id: recipientId },
    data: { balance: { increment: amount } },
  });

  // Create transaction record
  const transaction = await tx.transaction.create({
    data: { senderId, recipientId, amount },
  });

  return transaction;
}, {
  maxWait: 5000,    // Max time to acquire connection
  timeout: 10000,   // Max transaction duration
});
```

---

## TypeScript Integration

### Generated Types

```typescript
import {
  User,
  Post,
  Prisma,
  Role
} from '@prisma/client';

// Use generated types
function processUser(user: User): void {
  console.log(user.email);
}

// Input types for create/update
type UserCreateInput = Prisma.UserCreateInput;
type UserUpdateInput = Prisma.UserUpdateInput;

// Where clause types
type UserWhereInput = Prisma.UserWhereInput;
type UserWhereUniqueInput = Prisma.UserWhereUniqueInput;

// Include/Select types
type UserWithPosts = Prisma.UserGetPayload<{
  include: { posts: true };
}>;

// Custom payload type
type UserSummary = Prisma.UserGetPayload<{
  select: {
    id: true;
    email: true;
    name: true;
    _count: { select: { posts: true } };
  };
}>;
```

---

## Best Practices

### Performance

```typescript
// Use select to limit fields
const users = await prisma.user.findMany({
  select: { id: true, email: true }, // Only fetch needed fields
});

// Batch operations
const users = await prisma.user.createMany({
  data: usersToCreate,
  skipDuplicates: true,
});

// Use cursor pagination for large datasets
const users = await prisma.user.findMany({
  take: 10,
  cursor: { id: lastUserId },
  skip: 1, // Skip the cursor
});
```

### Error Handling

```typescript
import { Prisma } from '@prisma/client';

try {
  await prisma.user.create({ data });
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    if (error.code === 'P2002') {
      throw new Error('Email already exists');
    }
    if (error.code === 'P2025') {
      throw new Error('Record not found');
    }
  }
  throw error;
}
```

---

## Raw Queries

```typescript
// Raw query (typed result)
const users = await prisma.$queryRaw<User[]>`
  SELECT * FROM users
  WHERE email LIKE ${`%@example.com`}
  ORDER BY created_at DESC
  LIMIT 10
`;

// Parameterized queries (safe from SQL injection)
const email = 'user@example.com';
const user = await prisma.$queryRaw`
  SELECT * FROM users WHERE email = ${email}
`;

// Raw execute (for INSERT, UPDATE, DELETE)
const result = await prisma.$executeRaw`
  UPDATE users SET last_login = NOW() WHERE id = ${userId}
`;

// Using Prisma.sql for dynamic queries
import { Prisma } from '@prisma/client';

const orderBy = Prisma.sql`ORDER BY created_at DESC`;
const users = await prisma.$queryRaw`
  SELECT * FROM users ${orderBy}
`;
```

---

## Connection Pooling

### Configuration

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Connection pool settings via URL params
  // postgresql://user:pass@host:5432/db?connection_limit=5&pool_timeout=10
}
```

```typescript
// Programmatic pool configuration
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
});

// Graceful shutdown
process.on('beforeExit', async () => {
  await prisma.$disconnect();
});
```

### Serverless / Edge

```typescript
// For serverless environments (Vercel, AWS Lambda)
import { PrismaClient } from '@prisma/client';

// Use connection pooler like PgBouncer or Prisma Accelerate
const connectionString = process.env.DATABASE_URL;

// With Prisma Accelerate
const prisma = new PrismaClient({
  datasourceUrl: process.env.ACCELERATE_URL,
});
```

---

## Validation with Zod

```typescript
import { z } from 'zod';
import { Prisma } from '@prisma/client';

// Zod schema matching Prisma model
const UserCreateSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100).optional(),
  role: z.enum(['USER', 'ADMIN', 'MODERATOR']).default('USER'),
}) satisfies z.ZodType<Prisma.UserCreateInput>;

// Usage
function createUser(input: unknown) {
  const validated = UserCreateSchema.parse(input);
  return prisma.user.create({ data: validated });
}
```

---

## Testing Patterns

### Test Setup

```typescript
// test/setup.ts
import { PrismaClient } from '@prisma/client';
import { execSync } from 'child_process';

const prisma = new PrismaClient();

beforeAll(async () => {
  // Push schema to test database
  execSync('npx prisma db push --force-reset', {
    env: { ...process.env, DATABASE_URL: process.env.TEST_DATABASE_URL },
  });
});

beforeEach(async () => {
  // Clean tables before each test
  const tablenames = await prisma.$queryRaw<{ tablename: string }[]>`
    SELECT tablename FROM pg_tables WHERE schemaname='public'
  `;

  for (const { tablename } of tablenames) {
    if (tablename !== '_prisma_migrations') {
      await prisma.$executeRawUnsafe(
        `TRUNCATE TABLE "public"."${tablename}" CASCADE;`
      );
    }
  }
});

afterAll(async () => {
  await prisma.$disconnect();
});

export { prisma };
```

### Test Factories

```typescript
// test/factories/user.ts
import { faker } from '@faker-js/faker';
import { Prisma } from '@prisma/client';
import { prisma } from '../setup';

export function buildUser(
  overrides?: Partial<Prisma.UserCreateInput>
): Prisma.UserCreateInput {
  return {
    email: faker.internet.email(),
    name: faker.person.fullName(),
    role: 'USER',
    ...overrides,
  };
}

export async function createUser(
  overrides?: Partial<Prisma.UserCreateInput>
) {
  return prisma.user.create({
    data: buildUser(overrides),
  });
}

export async function createUsers(count: number) {
  return Promise.all(
    Array.from({ length: count }, () => createUser())
  );
}
```

### Integration Tests

```typescript
// test/user.test.ts
import { prisma, createUser } from './setup';
import { userService } from '../src/services/user';

describe('UserService', () => {
  describe('findByEmail', () => {
    it('returns user when found', async () => {
      const created = await createUser({ email: 'test@example.com' });

      const found = await userService.findByEmail('test@example.com');

      expect(found).toMatchObject({
        id: created.id,
        email: 'test@example.com',
      });
    });

    it('returns null when not found', async () => {
      const found = await userService.findByEmail('nonexistent@example.com');

      expect(found).toBeNull();
    });
  });
});
```

### Mocking Prisma

```typescript
// test/mocks/prisma.ts
import { PrismaClient } from '@prisma/client';
import { mockDeep, DeepMockProxy } from 'jest-mock-extended';

export type MockPrismaClient = DeepMockProxy<PrismaClient>;

export const createMockPrisma = (): MockPrismaClient => {
  return mockDeep<PrismaClient>();
};

// Usage in tests
import { createMockPrisma } from './mocks/prisma';

describe('UserService (unit)', () => {
  const mockPrisma = createMockPrisma();
  const userService = new UserService(mockPrisma);

  it('calls prisma.user.findUnique', async () => {
    mockPrisma.user.findUnique.mockResolvedValue({
      id: '1',
      email: 'test@example.com',
      name: 'Test',
      role: 'USER',
      createdAt: new Date(),
      updatedAt: new Date(),
    });

    const result = await userService.findById('1');

    expect(mockPrisma.user.findUnique).toHaveBeenCalledWith({
      where: { id: '1' },
    });
    expect(result?.email).toBe('test@example.com');
  });
});
```

---

## Soft Deletes

```typescript
// Middleware for soft deletes
prisma.$use(async (params, next) => {
  if (params.model === 'User') {
    if (params.action === 'delete') {
      params.action = 'update';
      params.args.data = { deletedAt: new Date() };
    }
    if (params.action === 'findMany' || params.action === 'findFirst') {
      params.args.where = { ...params.args.where, deletedAt: null };
    }
  }
  return next(params);
});
```

---

## Common Error Codes

| Code   | Description                  | Solution                       |
|--------|------------------------------|--------------------------------|
| P2002  | Unique constraint violation  | Handle duplicate entries       |
| P2003  | Foreign key constraint       | Ensure related records exist   |
| P2025  | Record not found             | Validate before update/delete  |
| P2024  | Connection pool timeout      | Increase pool size/timeout     |
| P1001  | Can't reach database         | Check connection string        |
| P1008  | Operations timed out         | Optimize query or increase timeout |
