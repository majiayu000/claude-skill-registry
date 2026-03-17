---
name: prisma
description: Provides type-safe database access with Prisma ORM including schema definition, migrations, queries, and relations. Use when setting up database connections, defining data models, writing queries, or managing database migrations.
---

# Prisma

Type-safe ORM for Node.js and TypeScript with auto-generated queries, migrations, and database introspection.

## Quick Start

**Install Prisma:**
```bash
npm install prisma --save-dev
npm install @prisma/client
npx prisma init
```

**Essential files:**
```
prisma/
  schema.prisma    # Data model and configuration
  migrations/      # Database migrations
```

## Schema Definition

### Basic Schema

```prisma
// prisma/schema.prisma

// Database connection
datasource db {
  provider = "postgresql"  // postgresql, mysql, sqlite, mongodb, sqlserver
  url      = env("DATABASE_URL")
}

// Client generator
generator client {
  provider = "prisma-client-js"
}

// Data models
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  password  String
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users")  // Table name in database
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  tags      Tag[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@map("posts")
}

model Profile {
  id     String  @id @default(cuid())
  bio    String?
  avatar String?
  user   User    @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId String  @unique

  @@map("profiles")
}

model Tag {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[]

  @@map("tags")
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

### Field Types

| Prisma Type | PostgreSQL | MySQL | SQLite |
|-------------|------------|-------|--------|
| String | text | varchar(191) | TEXT |
| Int | integer | int | INTEGER |
| BigInt | bigint | bigint | BIGINT |
| Float | double precision | double | REAL |
| Decimal | decimal(65,30) | decimal(65,30) | DECIMAL |
| Boolean | boolean | tinyint(1) | INTEGER |
| DateTime | timestamp(3) | datetime(3) | DATETIME |
| Json | jsonb | json | TEXT |
| Bytes | bytea | longblob | BLOB |

### Field Attributes

```prisma
model Example {
  // Primary key
  id String @id @default(cuid())

  // Auto-increment
  sequence Int @id @default(autoincrement())

  // UUID
  uuid String @id @default(uuid())

  // Unique constraint
  email String @unique

  // Default value
  role String @default("user")

  // Optional field
  bio String?

  // Database column name
  firstName String @map("first_name")

  // Timestamps
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Database-level default
  dbDefault String @default(dbgenerated("gen_random_uuid()"))
}
```

### Model Attributes

```prisma
model Post {
  id       String @id
  authorId String
  slug     String
  title    String

  // Composite unique constraint
  @@unique([authorId, slug])

  // Index
  @@index([authorId])

  // Composite primary key
  // @@id([field1, field2])

  // Table name
  @@map("blog_posts")
}
```

## Relations

### One-to-One

```prisma
model User {
  id      String   @id @default(cuid())
  profile Profile?
}

model Profile {
  id     String @id @default(cuid())
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId String @unique  // Foreign key + unique = one-to-one
}
```

### One-to-Many

```prisma
model User {
  id    String @id @default(cuid())
  posts Post[]  // One user has many posts
}

model Post {
  id       String @id @default(cuid())
  author   User   @relation(fields: [authorId], references: [id])
  authorId String // Foreign key

  @@index([authorId])
}
```

### Many-to-Many

```prisma
// Implicit (Prisma manages join table)
model Post {
  id   String @id @default(cuid())
  tags Tag[]
}

model Tag {
  id    String @id @default(cuid())
  posts Post[]
}

// Explicit (custom join table)
model Post {
  id   String    @id @default(cuid())
  tags PostTag[]
}

model Tag {
  id    String    @id @default(cuid())
  posts PostTag[]
}

model PostTag {
  post      Post     @relation(fields: [postId], references: [id])
  postId    String
  tag       Tag      @relation(fields: [tagId], references: [id])
  tagId     String
  assignedAt DateTime @default(now())

  @@id([postId, tagId])
}
```

### Self-Relations

```prisma
model User {
  id         String  @id @default(cuid())
  name       String
  followedBy User[]  @relation("Follows")
  following  User[]  @relation("Follows")
}

model Category {
  id       String     @id @default(cuid())
  name     String
  parent   Category?  @relation("CategoryHierarchy", fields: [parentId], references: [id])
  parentId String?
  children Category[] @relation("CategoryHierarchy")
}
```

## Migrations

### Development Workflow

```bash
# Create and apply migration
npx prisma migrate dev --name init

# Apply pending migrations
npx prisma migrate dev

# Reset database (drops all data)
npx prisma migrate reset

# Generate Prisma Client (without migration)
npx prisma generate
```

### Production

```bash
# Apply migrations (CI/CD)
npx prisma migrate deploy

# Check migration status
npx prisma migrate status
```

### Prototyping

```bash
# Push schema changes without migration (dev only)
npx prisma db push

# Pull existing database schema
npx prisma db pull
```

## Prisma Client

### Setup

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query'] : [],
  });

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

### CRUD Operations

#### Create

```typescript
// Create single record
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    name: 'Alice',
    password: hashedPassword,
  },
});

// Create with relation
const userWithProfile = await prisma.user.create({
  data: {
    email: 'bob@example.com',
    name: 'Bob',
    password: hashedPassword,
    profile: {
      create: {
        bio: 'Hello!',
      },
    },
  },
  include: {
    profile: true,
  },
});

// Create many
const users = await prisma.user.createMany({
  data: [
    { email: 'user1@example.com', name: 'User 1', password: 'hash1' },
    { email: 'user2@example.com', name: 'User 2', password: 'hash2' },
  ],
  skipDuplicates: true,
});
```

#### Read

```typescript
// Find unique
const user = await prisma.user.findUnique({
  where: { email: 'alice@example.com' },
});

// Find unique or throw
const user = await prisma.user.findUniqueOrThrow({
  where: { id: 'user-id' },
});

// Find first matching
const post = await prisma.post.findFirst({
  where: { published: true },
  orderBy: { createdAt: 'desc' },
});

// Find many
const users = await prisma.user.findMany({
  where: {
    email: { contains: '@example.com' },
    role: 'USER',
  },
  orderBy: { createdAt: 'desc' },
  take: 10,
  skip: 0,
});

// With relations
const userWithPosts = await prisma.user.findUnique({
  where: { id: 'user-id' },
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
    },
    profile: true,
  },
});

// Select specific fields
const userNames = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true,
  },
});
```

#### Update

```typescript
// Update single
const user = await prisma.user.update({
  where: { id: 'user-id' },
  data: { name: 'New Name' },
});

// Update many
const result = await prisma.user.updateMany({
  where: { role: 'USER' },
  data: { role: 'ADMIN' },
});

// Upsert (create or update)
const user = await prisma.user.upsert({
  where: { email: 'alice@example.com' },
  update: { name: 'Alice Updated' },
  create: {
    email: 'alice@example.com',
    name: 'Alice',
    password: 'hash',
  },
});

// Update relation
const user = await prisma.user.update({
  where: { id: 'user-id' },
  data: {
    profile: {
      update: { bio: 'Updated bio' },
    },
  },
});
```

#### Delete

```typescript
// Delete single
const user = await prisma.user.delete({
  where: { id: 'user-id' },
});

// Delete many
const result = await prisma.user.deleteMany({
  where: { role: 'USER' },
});

// Cascade delete (configured in schema)
const user = await prisma.user.delete({
  where: { id: 'user-id' },
  // Profile is deleted automatically if onDelete: Cascade
});
```

### Filtering

```typescript
const posts = await prisma.post.findMany({
  where: {
    // Exact match
    published: true,

    // String filters
    title: { contains: 'prisma', mode: 'insensitive' },
    content: { startsWith: 'Hello' },

    // Number filters
    views: { gte: 100, lt: 1000 },

    // Date filters
    createdAt: { gte: new Date('2024-01-01') },

    // Relation filters
    author: {
      email: { endsWith: '@example.com' },
    },

    // OR
    OR: [
      { title: { contains: 'prisma' } },
      { content: { contains: 'database' } },
    ],

    // AND
    AND: [
      { published: true },
      { views: { gte: 100 } },
    ],

    // NOT
    NOT: { author: { role: 'ADMIN' } },

    // Array contains (PostgreSQL)
    tags: { some: { name: 'typescript' } },
  },
});
```

### Pagination

```typescript
// Offset pagination
const page = 1;
const pageSize = 10;

const [posts, total] = await prisma.$transaction([
  prisma.post.findMany({
    skip: (page - 1) * pageSize,
    take: pageSize,
    orderBy: { createdAt: 'desc' },
  }),
  prisma.post.count(),
]);

const totalPages = Math.ceil(total / pageSize);

// Cursor pagination
const posts = await prisma.post.findMany({
  take: 10,
  skip: 1, // Skip cursor
  cursor: { id: lastPostId },
  orderBy: { createdAt: 'desc' },
});
```

### Transactions

```typescript
// Interactive transaction
const result = await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { email: 'alice@example.com', name: 'Alice', password: 'hash' },
  });

  const post = await tx.post.create({
    data: { title: 'First Post', authorId: user.id },
  });

  return { user, post };
});

// Batch transaction
const [users, posts] = await prisma.$transaction([
  prisma.user.findMany(),
  prisma.post.findMany(),
]);
```

### Aggregations

```typescript
// Count
const count = await prisma.post.count({
  where: { published: true },
});

// Aggregate
const result = await prisma.post.aggregate({
  _count: true,
  _avg: { views: true },
  _sum: { views: true },
  _min: { views: true },
  _max: { views: true },
  where: { published: true },
});

// Group by
const grouped = await prisma.post.groupBy({
  by: ['authorId'],
  _count: { id: true },
  _avg: { views: true },
  orderBy: { _count: { id: 'desc' } },
});
```

### Raw Queries

```typescript
// Raw query
const users = await prisma.$queryRaw<User[]>`
  SELECT * FROM users WHERE email LIKE ${`%@example.com`}
`;

// Raw execute
const result = await prisma.$executeRaw`
  UPDATE users SET role = 'ADMIN' WHERE id = ${userId}
`;

// Typed raw query
import { Prisma } from '@prisma/client';

const email = 'alice@example.com';
const users = await prisma.$queryRaw(
  Prisma.sql`SELECT * FROM users WHERE email = ${email}`
);
```

## Seeding

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // Clean existing data
  await prisma.post.deleteMany();
  await prisma.user.deleteMany();

  // Create users
  const alice = await prisma.user.create({
    data: {
      email: 'alice@example.com',
      name: 'Alice',
      password: 'hashed_password',
      posts: {
        create: [
          { title: 'First Post', published: true },
          { title: 'Draft Post', published: false },
        ],
      },
    },
  });

  console.log({ alice });
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

```json
// package.json
{
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  }
}
```

```bash
npx prisma db seed
```

## Common Patterns

### Soft Delete

```prisma
model Post {
  id        String    @id @default(cuid())
  title     String
  deletedAt DateTime?

  @@index([deletedAt])
}
```

```typescript
// Soft delete
await prisma.post.update({
  where: { id: postId },
  data: { deletedAt: new Date() },
});

// Query excluding deleted
const posts = await prisma.post.findMany({
  where: { deletedAt: null },
});
```

### Middleware

```typescript
const prisma = new PrismaClient();

// Soft delete middleware
prisma.$use(async (params, next) => {
  if (params.model === 'Post') {
    if (params.action === 'delete') {
      params.action = 'update';
      params.args['data'] = { deletedAt: new Date() };
    }

    if (params.action === 'findMany' || params.action === 'findFirst') {
      params.args['where'] = {
        ...params.args['where'],
        deletedAt: null,
      };
    }
  }

  return next(params);
});
```

## Best Practices

1. **Use singleton pattern** - Prevent multiple client instances
2. **Enable query logging** - In development for debugging
3. **Use transactions** - For related operations
4. **Add indexes** - On frequently queried fields
5. **Use select/include wisely** - Only fetch needed data

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Creating multiple clients | Use singleton pattern |
| N+1 queries | Use include/select with relations |
| No indexes | Add @@index to foreign keys |
| Ignoring migrations | Always use migrate dev |
| Raw strings in queries | Use Prisma.sql for safety |

## Reference Files

- [references/relations.md](references/relations.md) - Relation patterns
- [references/queries.md](references/queries.md) - Advanced query patterns
- [references/migrations.md](references/migrations.md) - Migration strategies
