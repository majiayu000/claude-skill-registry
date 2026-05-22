---
name: Prisma ORM Guide
description: Comprehensive guide to Prisma ORM including schema definition, migrations, queries, and best practices.
---

# Prisma ORM Guide

## Overview

Prisma is a next-generation TypeScript ORM for Node.js and TypeScript that makes database access easy with auto-generated types and queries. This skill covers schema definition, migrations, query patterns, transactions, and performance optimization.

## Prerequisites

- Understanding of TypeScript
- Knowledge of database concepts (SQL, relationships, indexes)
- Familiarity with Node.js and npm
- Basic understanding of database migrations

## Key Concepts

### Prisma Architecture

- **Prisma Client**: Auto-generated type-safe database client
- **Prisma Schema**: Declarative schema definition language
- **Prisma Migrate**: Database migration tool
- **Prisma Studio**: Visual database IDE
- **Type Safety**: Auto-generated TypeScript types

### Schema Design Philosophy

Prisma's schema allows:
- **Declarative Models**: Define models using Prisma Schema
- **Type Safety**: Auto-generated TypeScript types
- **Relations**: Define relationships between models
- **Constraints**: Database-level constraints
-- **Indexes**: Define indexes for performance

## Implementation Guide

### Schema Definition

#### Basic Models

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
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  password  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

#### Relations

```prisma
// prisma/schema.prisma

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Profile {
  id        String   @id @default(cuid())
  bio       String?
  userId    String   @unique
  user      User     @relation(fields: [userId], references: [id])
}
```

#### Enums

```prisma
// prisma/schema.prisma

enum Role {
  USER
  ADMIN
  MODERATOR
}

enum Status {
  DRAFT
  PUBLISHED
  ARCHIVED
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  role      Role     @default(USER)
  status    Status  @default(DRAFT)
}
```

#### Indexes

```prisma
// prisma/schema.prisma

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email, name])
  @@index([createdAt])
  @@index([updatedAt])
}

model Post {
  id        String   @id @default(cuid())
  title     String
  published Boolean  @default(false)
  authorId  String
  createdAt DateTime @default(now)

  @@index([authorId, published])
  @@index([createdAt])
}
```

#### Constraints

```prisma
// prisma/schema.prisma

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  age       Int

  @@map("users")
  @@index([email], name: "user_email_name_idx")
}

model Product {
  id          String   @id @default(cuid())
  name        String
  price       Float
  quantity    Int

  @@check: "price >= 0"
  @@check: "quantity >= 0"
}
```

### Migrations Workflow

#### Creating a Migration

```bash
# Create a new migration
npx prisma migrate dev --name add_user_profile

# Create migration without name (auto-generated)
npx prisma migrate dev
```

#### Applying Migrations to Production

```bash
# Generate migration SQL for review
npx prisma migrate dev --create-only --name add_user_profile

# Deploy migration to production
npx prisma migrate deploy

# Deploy specific migration
npx prisma migrate deploy --name add_user_profile
```

#### Migration History

```bash
# View migration history
npx prisma migrate status

# Resolve migration conflicts
npx prisma migrate resolve --applied "add_user_profile"

# Reset database and reapply migrations
npx prisma migrate reset
```

### Query Patterns

#### CRUD Operations

```typescript
// Create
const user = await prisma.user.create({
  data: {
    name: 'John Doe',
    email: 'john@example.com',
    password: 'hashed_password'
  }
})

// Read - Find many
const users = await prisma.user.findMany({
  orderBy: { createdAt: 'desc' }
})

// Read - Find one
const user = await prisma.user.findUnique({
  where: { email: 'john@example.com' }
})

// Update
const updatedUser = await prisma.user.update({
  where: { id: userId },
  data: { name: 'John Smith' }
})

// Delete
await prisma.user.delete({
  where: { id: userId }
})

// Delete many
await prisma.user.deleteMany({
  where: { status: 'inactive' }
})
```

#### Filtering

```typescript
// String filters
const users = await prisma.user.findMany({
  where: {
    OR: [
      { email: { contains: 'example.com' } },
      { name: { startsWith: 'John' } }
    ]
  }
})

// Number filters
const products = await prisma.product.findMany({
  where: {
    AND: [
      { price: { gte: 10, lte: 100 } },
      { quantity: { gt: 0 } }
    ]
  }
})

// Date filters
const posts = await prisma.post.findMany({
  where: {
    createdAt: {
      gte: new Date('2024-01-01'),
      lte: new Date('2024-12-31')
    }
  }
})

// Array filters
const users = await prisma.user.findMany({
  where: {
    tags: { hasEvery: ['admin', 'moderator'] }
  }
})

// Null filters
const usersWithProfile = await prisma.user.findMany({
  where: {
    profile: { isNot: null }
  }
})
```

#### Relations

```typescript
// Create with nested relation
const post = await prisma.post.create({
  data: {
    title: 'New Post',
    content: 'Post content',
    author: {
      connect: {
        id: userId,
      },
      create: {
        name: 'Author Name',
        email: 'author@example.com'
      }
    }
  }
})

// Include relations in queries
const postWithAuthor = await prisma.post.findUnique({
  where: { id: postId },
  include: {
    author: true
  }
})

// Include multiple relations
const postWithRelations = await prisma.post.findUnique({
  where: { id: postId },
  include: {
    author: {
      include: {
        profile: true
      }
    },
    comments: true
  }
})
```

#### Pagination

```typescript
// Skip and limit
const page = 1
const pageSize = 10

const users = await prisma.user.findMany({
  skip: (page - 1) * pageSize,
  take: pageSize,
  orderBy: { createdAt: 'desc' }
})

// Get total count for pagination
const total = await prisma.user.count()
const totalPages = Math.ceil(total / pageSize)
```

#### Sorting

```typescript
// Single field sort
const users = await prisma.user.findMany({
  orderBy: { name: 'asc' }
})

// Multiple field sort
const users = await prisma.user.findMany({
  orderBy: [
  { createdAt: 'desc' },
  { name: 'asc' }
  ]
})
```

### Transactions

#### Basic Transaction

```typescript
const session = await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { name: 'John' }
  })

  const post = await tx.post.create({
    data: {
      title: 'Post 1',
      authorId: user.id
    }
  })

  await tx.post.create({
    data: {
      title: 'Post 2',
      authorId: user.id
    }
  })
})
```

#### Transaction with Multiple Operations

```typescript
const session = await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { name: 'John' }
  })

  await tx.post.createMany({
    data: [
      { title: 'Post 1', authorId: user.id },
      { title: 'Post 2', authorId: user.id }
    ]
  })

  await tx.user.update({
    where: { id: user.id },
    data: { postCount: 2 }
  })
})
```

#### Transaction with Error Handling

```typescript
async function transferFunds(fromId: string, toId: string, amount: number) {
  const session = await prisma.$transaction(async (tx) => {
    const [fromUser, toUser] = await tx.user.findMany({
      where: { id: { in: [fromId, toId] } }
    })

    if (!fromUser || !toUser) {
      throw new Error('User not found')
    }

    if (fromUser.balance < amount) {
      throw new Error('Insufficient funds')
    }

    await tx.user.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } }
    })

    await tx.user.update({
      where: { id: toId },
      data: { balance: { increment: amount } }
    })

    await tx.transaction.create({
      data: {
        fromId,
        toId,
        amount,
        type: 'transfer'
      }
    })
  })
}
```

#### Interactive Transactions

```typescript
async function createUserWithProfile(userData: any, profileData: any) {
  return await prisma.$transaction(async (tx) => {
    const user = await tx.user.create({
      data: userData
    })

    const profile = await tx.profile.create({
      data: {
        ...profileData,
        userId: user.id
      }
    })

    return { user, profile }
  })
}
```

### Performance Optimization

#### Query Optimization

```typescript
// Good: Select only needed fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    name: true
  }
})

// Bad: Get all fields
const users = await prisma.user.findMany()
```

#### Connection Pooling

```typescript
// prisma/schema.prisma

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  
  // Connection pool settings
  connection_limit = 10
  pool_timeout = 20
}
```

#### Batch Operations

```typescript
// Good: Use createMany for bulk inserts
const users = await prisma.user.createMany({
  data: [
    { name: 'User 1', email: 'user1@example.com' },
    { name: 'User 2', email: 'user2@example.com' },
    { name: 'User 3', email: 'user3@example.com' }
  ]
})

// Bad: Multiple individual creates
for (const userData of userDataArray) {
  await prisma.user.create({ data: userData })
}
```

## Best Practices

1. **Schema Design**
   - Use appropriate field types for your data
   - Define relations properly
   - Add indexes for frequently queried fields
   - Use enums for fixed value sets
   - Add constraints for data integrity

2. **Migrations**
   - Always review generated migrations before deploying
   - Use descriptive migration names
   - Test migrations in development first
   - Use transactions for data migrations
   - Keep migration history clean

3. **Query Optimization**
   - Select only needed fields
   - Use appropriate indexes
   - Use pagination for large datasets
   - Use findFirst instead of findMany when possible
   - Avoid N+1 query problems with includes

4. **Transactions**
   - Use transactions for multi-step operations
   - Keep transactions short
   - Handle errors properly with rollback
   - Use appropriate isolation levels

5. **Error Handling**
   - Handle known Prisma errors gracefully
   - Implement proper error logging
   - Use type-safe error handling
   - Provide meaningful error messages

6. **Testing**
   - Write unit tests for critical operations
   - Test migrations thoroughly
   - Use Prisma's mock client for testing
   - Test edge cases and error scenarios

## Related Skills

- [`04-database/database-transactions`](04-database/database-transactions/SKILL.md)
- [`04-database/database-migrations`](04-database/database-migrations/SKILL.md)
- [`04-database/database-optimization`](04-database/database-optimization/SKILL.md)
- [`01-foundations/typescript-standards`](01-foundations/typescript-standards/SKILL.md)
