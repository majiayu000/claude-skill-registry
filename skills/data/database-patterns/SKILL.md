---
name: database-patterns
description: |
  Database design patterns, SQL best practices, ORM usage (Prisma/Drizzle), and migration strategies.
  Use when designing schemas, writing queries, or optimizing database operations.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Database Patterns & Best Practices

## Schema Design Principles

### 1. Normalization (3NF minimum)
- No repeating groups
- No partial dependencies
- No transitive dependencies

### 2. Use UUIDs vs Auto-Increment
```sql
-- GOOD: UUID for distributed systems
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- OK: Auto-increment for simple cases
id SERIAL PRIMARY KEY
```

### 3. Timestamps on Every Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Prisma ORM Patterns

### Schema Definition

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@map("users")
}

model Post {
  id        String   @id @default(uuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  tags      Tag[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@index([published])
  @@map("posts")
}

enum Role {
  USER
  ADMIN
}
```

### CRUD Operations

```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Create
async function createUser(data: { name: string; email: string }) {
  return prisma.user.create({
    data,
    select: {
      id: true,
      name: true,
      email: true,
      createdAt: true
    }
  })
}

// Read with relations
async function getUserWithPosts(id: string) {
  return prisma.user.findUnique({
    where: { id },
    include: {
      posts: {
        where: { published: true },
        orderBy: { createdAt: 'desc' },
        take: 10
      },
      profile: true
    }
  })
}

// Update
async function updateUser(id: string, data: Partial<User>) {
  return prisma.user.update({
    where: { id },
    data
  })
}

// Delete (soft delete pattern)
async function deleteUser(id: string) {
  return prisma.user.update({
    where: { id },
    data: { deletedAt: new Date() }
  })
}
```

### Transactions

```typescript
// Interactive transaction
async function transferFunds(fromId: string, toId: string, amount: number) {
  return prisma.$transaction(async (tx) => {
    const from = await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } }
    })

    if (from.balance < 0) {
      throw new Error('Insufficient funds')
    }

    await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } }
    })

    return tx.transaction.create({
      data: { fromId, toId, amount }
    })
  })
}

// Sequential transaction
async function createUserWithProfile(data: CreateUserInput) {
  return prisma.$transaction([
    prisma.user.create({ data: data.user }),
    prisma.profile.create({ data: data.profile })
  ])
}
```

### Pagination

```typescript
// Cursor-based (recommended for large datasets)
async function getUsers(cursor?: string, limit = 20) {
  const users = await prisma.user.findMany({
    take: limit + 1,
    cursor: cursor ? { id: cursor } : undefined,
    orderBy: { createdAt: 'desc' },
    skip: cursor ? 1 : 0 // Skip the cursor itself
  })

  const hasMore = users.length > limit
  const data = hasMore ? users.slice(0, -1) : users

  return {
    data,
    nextCursor: hasMore ? data[data.length - 1].id : null
  }
}

// Offset-based
async function getUsersWithOffset(page = 1, limit = 20) {
  const [users, total] = await Promise.all([
    prisma.user.findMany({
      skip: (page - 1) * limit,
      take: limit
    }),
    prisma.user.count()
  ])

  return {
    data: users,
    meta: { total, page, limit, totalPages: Math.ceil(total / limit) }
  }
}
```

## Query Optimization

### Avoid N+1 Queries

```typescript
// BAD: N+1 problem
const users = await prisma.user.findMany()
for (const user of users) {
  const posts = await prisma.post.findMany({
    where: { authorId: user.id }
  })
}

// GOOD: Include in single query
const users = await prisma.user.findMany({
  include: { posts: true }
})

// GOOD: Select only needed fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    posts: {
      select: {
        id: true,
        title: true
      }
    }
  }
})
```

### Use Indexes Properly

```prisma
model Post {
  id        String @id
  authorId  String
  status    Status
  createdAt DateTime

  // Compound index for common query patterns
  @@index([authorId, status])
  @@index([status, createdAt])
}
```

```sql
-- For frequently queried columns
CREATE INDEX idx_posts_author_status ON posts(author_id, status);

-- For text search
CREATE INDEX idx_posts_title_gin ON posts USING gin(to_tsvector('english', title));

-- For JSON columns
CREATE INDEX idx_metadata_gin ON posts USING gin(metadata);
```

### Batch Operations

```typescript
// Batch create
await prisma.user.createMany({
  data: users,
  skipDuplicates: true
})

// Batch update with raw SQL (when needed)
await prisma.$executeRaw`
  UPDATE posts 
  SET status = 'archived' 
  WHERE created_at < NOW() - INTERVAL '1 year'
`

// Batch delete
await prisma.user.deleteMany({
  where: {
    deletedAt: { not: null },
    deletedAt: { lt: thirtyDaysAgo }
  }
})
```

## Migration Patterns

### Prisma Migrations

```bash
# Create migration
npx prisma migrate dev --name add_user_role

# Apply in production
npx prisma migrate deploy

# Reset database (dev only)
npx prisma migrate reset
```

### Safe Schema Changes

```typescript
// Step 1: Add nullable column
model User {
  newField String?  // nullable first
}

// Step 2: Backfill data
await prisma.$executeRaw`
  UPDATE users SET new_field = 'default' WHERE new_field IS NULL
`

// Step 3: Make non-nullable
model User {
  newField String @default("default")
}
```

### Rollback Strategy

```sql
-- Always create down migrations
-- up.sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- down.sql
ALTER TABLE users DROP COLUMN phone;
```

## Connection Management

### Connection Pooling

```typescript
// Singleton pattern for Prisma
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: ['error', 'warn'],
  datasources: {
    db: {
      url: process.env.DATABASE_URL
    }
  }
})

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}
```

### Serverless Configuration

```typescript
// For serverless (Vercel, AWS Lambda)
import { PrismaClient } from '@prisma/client'
import { Pool } from '@neondatabase/serverless'
import { PrismaNeon } from '@prisma/adapter-neon'

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
const adapter = new PrismaNeon(pool)
const prisma = new PrismaClient({ adapter })
```

## Soft Delete Pattern

```prisma
model User {
  id        String    @id @default(uuid())
  email     String    @unique
  deletedAt DateTime?

  @@index([deletedAt])
}
```

```typescript
// Middleware for automatic filtering
prisma.$use(async (params, next) => {
  if (params.model === 'User') {
    if (params.action === 'findMany' || params.action === 'findFirst') {
      params.args.where = {
        ...params.args.where,
        deletedAt: null
      }
    }
  }
  return next(params)
})

// Soft delete
async function softDelete(id: string) {
  return prisma.user.update({
    where: { id },
    data: { deletedAt: new Date() }
  })
}

// Hard delete (permanent)
async function hardDelete(id: string) {
  return prisma.user.delete({ where: { id } })
}
```

## Audit Trail Pattern

```prisma
model AuditLog {
  id         String   @id @default(uuid())
  entityType String
  entityId   String
  action     String   // CREATE, UPDATE, DELETE
  changes    Json?
  userId     String?
  createdAt  DateTime @default(now())

  @@index([entityType, entityId])
  @@index([userId])
  @@index([createdAt])
}
```

```typescript
// Middleware for automatic audit logging
prisma.$use(async (params, next) => {
  const result = await next(params)
  
  if (['create', 'update', 'delete'].includes(params.action)) {
    await prisma.auditLog.create({
      data: {
        entityType: params.model!,
        entityId: result.id,
        action: params.action.toUpperCase(),
        changes: params.args.data,
        userId: getCurrentUserId()
      }
    })
  }
  
  return result
})
```

## Multi-Tenant Pattern

```prisma
model Organization {
  id    String @id @default(uuid())
  name  String
  users User[]
  posts Post[]
}

model User {
  id             String       @id @default(uuid())
  organization   Organization @relation(fields: [organizationId], references: [id])
  organizationId String

  @@index([organizationId])
}
```

```typescript
// Row-level security with Prisma extension
const prismaWithTenant = prisma.$extends({
  query: {
    $allModels: {
      async $allOperations({ args, query, model }) {
        const tenantId = getTenantId()
        
        if (tenantId && hasTenantField(model)) {
          args.where = { ...args.where, organizationId: tenantId }
        }
        
        return query(args)
      }
    }
  }
})
```

## Raw SQL When Needed

```typescript
// Complex aggregations
const stats = await prisma.$queryRaw<Stats[]>`
  SELECT 
    DATE_TRUNC('day', created_at) as date,
    COUNT(*) as count,
    SUM(amount) as total
  FROM transactions
  WHERE created_at >= ${startDate}
  GROUP BY DATE_TRUNC('day', created_at)
  ORDER BY date DESC
`

// Full-text search
const results = await prisma.$queryRaw<Post[]>`
  SELECT * FROM posts
  WHERE to_tsvector('english', title || ' ' || content) 
    @@ plainto_tsquery('english', ${searchTerm})
  ORDER BY ts_rank(
    to_tsvector('english', title || ' ' || content),
    plainto_tsquery('english', ${searchTerm})
  ) DESC
  LIMIT ${limit}
`
```

## Checklist

- [ ] UUIDs for distributed systems
- [ ] Timestamps on all tables
- [ ] Proper indexes for query patterns
- [ ] N+1 queries avoided (use include/join)
- [ ] Transactions for multi-step operations
- [ ] Soft delete where appropriate
- [ ] Connection pooling configured
- [ ] Migrations tested (up and down)
- [ ] Audit logging for sensitive data
- [ ] Query performance monitored
