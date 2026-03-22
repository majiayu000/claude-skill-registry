---
name: prisma-orm
description: Prisma ORM patterns for Node.js/TypeScript backends. Use when defining Prisma schemas, writing queries, handling relations, migrations, or any database work in a Node.js/TypeScript project.
---

# Prisma ORM Patterns

## Schema Design
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
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String
  password  String
  role      Role     @default(USER)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  deletedAt DateTime? // Soft delete

  posts     Post[]
  sessions  Session[]

  @@index([email])
  @@map("users")  // Table name
}

enum Role {
  USER
  ADMIN
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String   @db.VarChar(255)
  body      String
  published Boolean  @default(false)
  authorId  Int
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  author    User     @relation(fields: [authorId], references: [id])
  tags      Tag[]    @relation("PostTags")

  @@index([authorId])
  @@index([published, createdAt(sort: Desc)])
}

model Tag {
  id    Int    @id @default(autoincrement())
  name  String @unique
  posts Post[] @relation("PostTags")
}
```

## Client Setup
```typescript
// lib/db.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = global as unknown as { prisma: PrismaClient }

export const db = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error'] : ['error'],
})

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db
// Single instance pattern prevents connection exhaustion in dev (Next.js HMR)
```

## Query Patterns
```typescript
// Find with relations (avoid N+1)
const posts = await db.post.findMany({
  where: { published: true, author: { deletedAt: null } },
  include: { author: { select: { id: true, name: true } }, tags: true },
  orderBy: { createdAt: 'desc' },
  take: 20,
  skip: (page - 1) * 20,
})

// Upsert
const setting = await db.setting.upsert({
  where: { userId_key: { userId, key } },
  create: { userId, key, value },
  update: { value },
})

// Transaction
const [user, post] = await db.$transaction([
  db.user.update({ where: { id: userId }, data: { postCount: { increment: 1 } } }),
  db.post.create({ data: { title, body, authorId: userId } }),
])

// Interactive transaction (for complex logic)
const result = await db.$transaction(async (tx) => {
  const user = await tx.user.findUniqueOrThrow({ where: { id: userId } })
  if (user.balance < amount) throw new Error('Insufficient balance')
  await tx.user.update({ where: { id: userId }, data: { balance: { decrement: amount } } })
  return tx.payment.create({ data: { userId, amount } })
})

// Raw SQL for complex queries
const stats = await db.$queryRaw<{ date: Date; count: bigint }[]>`
  SELECT date_trunc('day', created_at) as date, COUNT(*) as count
  FROM posts
  WHERE created_at > ${thirtyDaysAgo}
  GROUP BY 1 ORDER BY 1
`
```

## Migrations
```bash
# Dev workflow
npx prisma migrate dev --name add_user_role      # Create + apply migration
npx prisma migrate dev --create-only             # Create only, don't apply
npx prisma db push                               # Push schema without migration (prototyping)
npx prisma studio                                # GUI to inspect DB

# Production
npx prisma migrate deploy                        # Apply pending migrations
npx prisma generate                              # Regenerate client after schema change
```

## Soft Delete Pattern
```typescript
// Middleware to filter soft-deleted records globally
db.$use(async (params, next) => {
  if (params.model === 'User') {
    if (params.action === 'findMany' || params.action === 'findFirst') {
      params.args.where = { ...params.args.where, deletedAt: null }
    }
    if (params.action === 'delete') {
      params.action = 'update'
      params.args.data = { deletedAt: new Date() }
    }
  }
  return next(params)
})
```

## Rules
- Always use `select` to fetch only needed fields (never fetch passwords)
- Use `include` for relations instead of multiple queries (prevent N+1)
- Transactions for multi-table writes (consistency guarantee)
- `findUniqueOrThrow` / `findFirstOrThrow` to get automatic 404 behavior
- Add `@@index` for all foreign keys and frequent filter columns
- Never use `db.raw` with user input — always use parameterized `$queryRaw`
- Single PrismaClient instance (global pattern above) for connection pooling
