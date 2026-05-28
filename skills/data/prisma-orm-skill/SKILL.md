---
name: "Prisma ORM Database"
description: "Design database schemas, create migrations, manage data relationships, and sync with production using Prisma. Apply when designing database schemas, creating migrations, or defining data models."
allowed-tools: Read, Write, Edit, Bash
version: 1.0.0
---

# Prisma ORM Database

Systematic Prisma workflow ensuring type-safe database operations with zero migration errors.

## Overview

This Skill enforces:
- Prisma schema definition (source of truth)
- Model-first migration pattern
- Safe migrations with rollback testing
- Type-safe database queries
- Environment-specific workflows
- Schema drift detection
- Production deployment safety

Apply when designing database schemas, creating migrations, or generating Prisma Client.

## Prisma Workflow

**Every schema change follows this process**:

```
Step 1: Update schema.prisma
  ↓
Step 2: Create migration
  ↓
Step 3: Test migration locally
  ↓
Step 4: Deploy to preview
  ↓
Step 5: Merge and deploy production
```

## Step 1: Setup

### Install Prisma

```bash
npm install @prisma/client
npm install -D prisma

# Initialize Prisma
npx prisma init
```

### Configure Database Connection

Create `.env.local`:

```
DATABASE_URL="postgresql://user:password@host:5432/dbname"
```

For Neon:

```
DATABASE_URL="postgresql://user:password@host-pooler.neon.tech/dbname?sslmode=require"
```

## Step 2: Schema Definition

### Create Models

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
  name      String
  password  String   @db.VarChar(255)
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
}

model Profile {
  id     String @id @default(cuid())
  bio    String?
  avatar String?
  userId String @unique
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String   @db.Text
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  tags      Tag[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@index([published])
}

model Tag {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[]
}

enum Role {
  ADMIN
  USER
  GUEST
}
```

## Step 3: Relationships

### One-to-Many Relationship

```prisma
model Author {
  id    String @id @default(cuid())
  name  String
  books Book[]
}

model Book {
  id       String @id @default(cuid())
  title    String
  authorId String
  author   Author @relation(fields: [authorId], references: [id])
}
```

### One-to-One Relationship

```prisma
model User {
  id      String  @id @default(cuid())
  email   String  @unique
  profile Profile?
}

model Profile {
  id     String  @id @default(cuid())
  userId String  @unique
  user   User    @relation(fields: [userId], references: [id], onDelete: Cascade)
}
```

### Many-to-Many Relationship

```prisma
model Student {
  id       String   @id @default(cuid())
  name     String
  courses  Course[]
}

model Course {
  id       String    @id @default(cuid())
  name     String
  students Student[]
}
```

## Step 4: Create Migrations

### LOCAL DEVELOPMENT Workflow

```bash
# 1. Update schema.prisma
# (Add, modify, or remove models)

# 2. Create migration
npx prisma migrate dev --name add-user-model

# 3. Migration file created in prisma/migrations/
# 4. Database updated automatically
# 5. Prisma Client regenerated
```

### Check Migration Status

```bash
# View migration history
npx prisma migrate status

# Show which migrations are pending
npx prisma migrate status --verbose
```

### Rollback Migration

```bash
# Reset database (careful! loses all data)
npx prisma migrate reset

# This:
# 1. Deletes database
# 2. Recreates from scratch
# 3. Applies all migrations
# 4. Seeds data (if seed.ts exists)
```

## Step 5: Push vs Migrate

### npx prisma db push (Prototyping)

**Use for**: Rapid development, testing, no production

```bash
npx prisma db push
```

**Pros**:
- Fast
- No migration files created
- Good for early stages

**Cons**:
- No migration history
- Can't reproduce changes
- Not safe for production

### npx prisma migrate dev (Production-Safe)

**Use for**: Everything! Development, preview, production

```bash
npx prisma migrate dev --name descriptive_name
```

**Pros**:
- Creates migration files (version control)
- Reproducible on any environment
- Safe rollback capability
- Production-ready

## Step 6: Deploy Migrations

### Preview/Staging Environment

```bash
# GitHub Actions workflow
npx prisma migrate deploy
```

### Production Environment

```bash
# Automated deployment (never manual!)
npx prisma migrate deploy
```

**Checklist**:
- [ ] All migrations tested locally
- [ ] No destructive changes without data migration
- [ ] Rollback plan documented
- [ ] Backups taken
- [ ] Team notified of changes

## Step 7: Querying Data

### Type-Safe Queries

```ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// ✅ GOOD: Type-safe query
const user = await prisma.user.findUnique({
  where: { id: 'user-123' }
});
// user is fully typed: { id: string, email: string, name: string, ... }

// ✅ GOOD: Create with relations
const newUser = await prisma.user.create({
  data: {
    email: 'test@example.com',
    name: 'Test User',
    profile: {
      create: {
        bio: 'My bio',
        avatar: 'https://...'
      }
    }
  },
  include: { profile: true }
});

// ✅ GOOD: Query with relations
const users = await prisma.user.findMany({
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' }
    },
    profile: true
  }
});

// ✅ GOOD: Update with nested operations
const updated = await prisma.user.update({
  where: { id: 'user-123' },
  data: {
    email: 'newemail@example.com',
    profile: {
      update: { bio: 'Updated bio' }
    }
  }
});

// ✅ GOOD: Delete with cascading
await prisma.user.delete({
  where: { id: 'user-123' }
  // Posts automatically deleted (onDelete: Cascade)
});
```

## Step 8: Anti-Patterns

```ts
// ❌ BAD: Manual SQL queries (lose type safety)
const result = await prisma.$queryRaw`SELECT * FROM users`;

// ✅ GOOD: Use Prisma query builder
const users = await prisma.user.findMany();

// ❌ BAD: N+1 queries
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({
    where: { authorId: user.id }
  });
  // Database hit per user!
}

// ✅ GOOD: Query with relations
const users = await prisma.user.findMany({
  include: { posts: true }
});

// ❌ BAD: Creating migrations without testing
npx prisma migrate deploy  // Without local testing!

// ✅ GOOD: Test locally first
npx prisma migrate dev --name test-migration
npx prisma migrate reset
npx prisma migrate dev
```

## Step 9: Schema Drift Detection

### Detect and Fix Drift

```bash
# Compare migration history with actual database
npx prisma migrate diff

# Generate SQL to fix drift
npx prisma migrate diff \
  --from-schema-datamodel prisma/schema.prisma \
  --to-schema-datasource
```

## Step 10: Seeding Database

### Create Seed File

Create `prisma/seed.ts`:

```ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // Create users
  const user1 = await prisma.user.create({
    data: {
      email: 'alice@example.com',
      name: 'Alice',
      password: 'hashedpassword123'
    }
  });

  // Create posts
  const post1 = await prisma.post.create({
    data: {
      title: 'First Post',
      content: 'Content here',
      authorId: user1.id
    }
  });

  console.log('Database seeded successfully');
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

Configure `package.json`:

```json
{
  "prisma": {
    "seed": "ts-node prisma/seed.ts"
  }
}
```

Run seed:

```bash
npx prisma db seed
```

## Step 11: Production Deployment

### CI/CD Pipeline

```yaml
# .github/workflows/migrations.yaml
name: Deploy Migrations

on:
  push:
    branches: [main]

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Deploy migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: npx prisma migrate deploy
```

## Verification Before Production

- [ ] All schema changes defined in prisma/schema.prisma
- [ ] Migrations created with descriptive names
- [ ] Migrations tested locally (push and reset)
- [ ] No data loss in migrations
- [ ] Rollback plan documented
- [ ] Prisma Client regenerated
- [ ] Type safety verified
- [ ] CI/CD pipeline configured
- [ ] Backups taken before production
- [ ] Team notified of schema changes

## Common Commands

```bash
# Generate Prisma Client
npx prisma generate

# Create migration
npx prisma migrate dev --name migration_name

# Deploy migrations
npx prisma migrate deploy

# Reset database
npx prisma migrate reset

# View Prisma Studio (UI)
npx prisma studio

# Format schema
npx prisma format

# Check migrations status
npx prisma migrate status

# Seed database
npx prisma db seed

# Push without migrations (dev only)
npx prisma db push
```

## Integration with Project Standards

Enforces database best practices:
- D-1: Models defined in organized files
- D-2: Type-safe validation
- D-3: Migrations are reproducible
- Type safety eliminates SQL injection
- No hardcoded secrets (uses .env)

## Resources

- Prisma Documentation: https://www.prisma.io/docs
- Prisma Migrate: https://www.prisma.io/docs/orm/prisma-migrate
- Schema: https://www.prisma.io/docs/orm/prisma-schema
- Relations: https://www.prisma.io/docs/orm/prisma-schema/relations
