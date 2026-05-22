---
name: cermont.backend.prisma-v7
description: Expert guidance for Prisma ORM v7 (7.0+). Use when working with Prisma schema files, migrations, Prisma Client queries, database setup. Covers ESM modules, driver adapters, prisma.config.ts, Rust-free client.
triggers:
  - Prisma
  - schema.prisma
  - "@prisma/client"
  - database models
  - ORM
  - migrations
role: secondary
scope: backend
---

<!-- Cermont Project Fit -->
## Project Fit

| Attribute | Value |
|-----------|-------|
| **Applies to** | backend |
| **Requires** | NestJS, Prisma, pnpm |
| **Not for this repo** | TypeORM, Sequelize |
| **Status** | Active (v7 patterns for future upgrade) |

> [!NOTE]
> Cermont currently uses Prisma v6. This skill documents v7 patterns for future migration.

### Guardrails

**Safety Checklist:**
```bash
pnpm --filter @cermont/backend prisma validate
pnpm --filter @cermont/backend prisma generate
pnpm --filter @cermont/backend test
# Rollback: git restore -SW .
```
<!-- End Project Fit -->

## Core v7 Changes

### 1. ES Modules (ESM) Required
Prisma v7 ships as an ES module. Your project must use ESM:

**package.json:**
```json
{
  "type": "module"
}
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "Node",
    "target": "ES2023",
    "strict": true,
    "esModuleInterop": true
  }
}
```

### 2. Driver Adapters Required
All databases now require driver adapters. The Rust-free client provides better performance and smaller bundle sizes.

**Available Adapters:**
- PostgreSQL: `@prisma/adapter-pg` (with `pg` driver)
- MySQL/MariaDB: `@prisma/adapter-mariadb` (with `mariadb` driver)
- SQLite: `@prisma/adapter-better-sqlite3` (with `better-sqlite3`)
- CockroachDB: `@prisma/adapter-pg` (with `pg` driver)
- Neon: `@prisma/adapter-neon` (with `@neondatabase/serverless`)
- PlanetScale: `@prisma/adapter-planetscale` (with `@planetscale/database`)
- D1 (Cloudflare): `@prisma/adapter-d1`
- MSSQL: `@prisma/adapter-mssql`

### 3. Generator Configuration
The `output` field is now **required** and the new `prisma-client` provider is standard:

```prisma
generator client {
  provider = "prisma-client"
  output   = "./generated/prisma"
}
```

Note: Client is no longer generated in `node_modules` by default.

### 4. Prisma Config File (prisma.config.ts)
Database URLs and CLI configuration now live in `prisma.config.ts` instead of the schema file.

**Basic setup:**
```typescript
import 'dotenv/config'
import { defineConfig, env } from 'prisma/config'

export default defineConfig({
  schema: 'prisma/schema.prisma',
  migrations: {
    path: 'prisma/migrations',
  },
  datasource: {
    url: env('DATABASE_URL'),
  },
})
```

**Note:** For Bun, skip `import 'dotenv/config'` as it auto-loads .env files.

### 5. Schema Datasource Block
Remove `url`, `directUrl`, and `shadowDatabaseUrl` from schema.prisma:

**v7 schema.prisma:**
```prisma
datasource db {
  provider = "postgresql"
  // url field removed - now in prisma.config.ts
}

generator client {
  provider = "prisma-client"
  output   = "./generated/prisma"
}
```

## Installation & Setup

### New Project

```bash
# Install dependencies
npm install prisma@latest @prisma/client@latest

# Choose appropriate adapter
npm install @prisma/adapter-pg pg          # PostgreSQL
npm install @prisma/adapter-mariadb mariadb # MySQL/MariaDB
npm install @prisma/adapter-better-sqlite3 better-sqlite3 # SQLite

# Install dev tools
npm install -D tsx dotenv

# Initialize Prisma (creates prisma.config.ts automatically)
npx prisma init
```

### Upgrading from v6

```bash
# Update packages
npm install prisma@latest @prisma/client@latest

# Install adapter for your database
npm install @prisma/adapter-pg pg  # for PostgreSQL

# Install dotenv if not using Bun
npm install dotenv

# Regenerate client
npx prisma generate
```

## Client Instantiation

### PostgreSQL Example

```typescript
import { PrismaClient } from './generated/prisma/client'
import { PrismaPg } from '@prisma/adapter-pg'
import 'dotenv/config'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL
})

const prisma = new PrismaClient({ adapter })

export default prisma
```

### MySQL/MariaDB Example

```typescript
import { PrismaClient } from './generated/prisma/client'
import { PrismaMariaDb } from '@prisma/adapter-mariadb'
import 'dotenv/config'

const adapter = new PrismaMariaDb({
  host: 'localhost',
  port: 3306,
  connectionLimit: 5
})

const prisma = new PrismaClient({ adapter })

export default prisma
```

### SQLite Example

```typescript
import { PrismaClient } from './generated/prisma/client'
import { PrismaBetterSqlite3 } from '@prisma/adapter-better-sqlite3'
import 'dotenv/config'

const adapter = new PrismaBetterSqlite3({
  url: process.env.DATABASE_URL || 'file:./dev.db'
})

const prisma = new PrismaClient({ adapter })

export default prisma
```

### Prisma Accelerate (Caching/Pooling)

If using Prisma Accelerate for caching, do NOT use a driver adapter:

```typescript
import { PrismaClient } from './generated/prisma/client'
import { withAccelerate } from '@prisma/extension-accelerate'

const prisma = new PrismaClient({
  accelerateUrl: process.env.DATABASE_URL // prisma:// or prisma+postgres:// URL
}).$extends(withAccelerate())

export default prisma
```

**Important:** Never pass `prisma://` or `prisma+postgres://` URLs to driver adapters.

## Schema Best Practices

### Complete Schema Example

```prisma
// schema.prisma
datasource db {
  provider = "postgresql"
}

generator client {
  provider = "prisma-client"
  output   = "./generated/prisma"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
}
```

### Relations

**One-to-Many:**
```prisma
model User {
  id    Int    @id @default(autoincrement())
  posts Post[]
}

model Post {
  id       Int  @id @default(autoincrement())
  author   User @relation(fields: [authorId], references: [id])
  authorId Int
  
  @@index([authorId])
}
```

**Many-to-Many:**
```prisma
model Post {
  id         Int        @id @default(autoincrement())
  categories Category[]
}

model Category {
  id    Int    @id @default(autoincrement())
  posts Post[]
}
```

**One-to-One:**
```prisma
model User {
  id      Int      @id @default(autoincrement())
  profile Profile?
}

model Profile {
  id     Int  @id @default(autoincrement())
  user   User @relation(fields: [userId], references: [id])
  userId Int  @unique
}
```

## Common Commands

```bash
# Generate Prisma Client
npx prisma generate

# Create and apply migration
npx prisma migrate dev --name init

# Apply migrations in production
npx prisma migrate deploy

# Reset database (dev only)
npx prisma migrate reset

# Open Prisma Studio
npx prisma studio

# Format schema
npx prisma format

# Validate schema
npx prisma validate

# Pull schema from database
npx prisma db pull

# Push schema to database (prototyping)
npx prisma db push

# Seed database
npx prisma db seed
```

## Prisma Client Queries

### Basic CRUD

```typescript
// Create
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John Doe',
  },
})

// Read
const user = await prisma.user.findUnique({
  where: { id: 1 },
})

const users = await prisma.user.findMany({
  where: { email: { contains: '@example.com' } },
  orderBy: { createdAt: 'desc' },
  take: 10,
})

// Update
const user = await prisma.user.update({
  where: { id: 1 },
  data: { name: 'Jane Doe' },
})

// Delete
const user = await prisma.user.delete({
  where: { id: 1 },
})
```

### Relations

```typescript
// Create with relations
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    posts: {
      create: [
        { title: 'First Post', content: 'Content...' },
        { title: 'Second Post', content: 'More content...' },
      ],
    },
  },
})

// Query with relations
const userWithPosts = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: true,
  },
})

// Select specific fields
const user = await prisma.user.findUnique({
  where: { id: 1 },
  select: {
    id: true,
    email: true,
    posts: {
      select: {
        id: true,
        title: true,
      },
    },
  },
})
```

### Advanced Queries

```typescript
// Filtering
const posts = await prisma.post.findMany({
  where: {
    OR: [
      { title: { contains: 'Prisma' } },
      { content: { contains: 'database' } },
    ],
    published: true,
    author: {
      email: { endsWith: '@prisma.io' },
    },
  },
})

// Aggregations
const result = await prisma.post.aggregate({
  _count: true,
  _avg: { authorId: true },
  _sum: { authorId: true },
})

// Group by
const groups = await prisma.post.groupBy({
  by: ['authorId'],
  _count: true,
  having: {
    authorId: { gt: 10 },
  },
})

// Transactions
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'user@example.com' } }),
  prisma.post.create({ data: { title: 'Post', authorId: 1 } }),
])

// Interactive transactions
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { email: 'user@example.com' },
  })
  
  await tx.post.create({
    data: { title: 'Post', authorId: user.id },
  })
})
```

## Migration Workflow

### Development
```bash
# Create migration and apply
npx prisma migrate dev --name add_user_table

# Apply pending migrations
npx prisma migrate dev

# Reset database
npx prisma migrate reset
```

### Production
```bash
# Apply migrations
npx prisma migrate deploy

# Check migration status
npx prisma migrate status
```

### Prototyping
```bash
# Push schema changes without creating migrations
npx prisma db push
```

## Environment Variables

**.env:**
```bash
# PostgreSQL
DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"

# MySQL
DATABASE_URL="mysql://user:password@localhost:3306/mydb"

# SQLite
DATABASE_URL="file:./dev.db"

# Prisma Accelerate
DATABASE_URL="prisma://accelerate.prisma-data.net/?api_key=..."

# Direct URL (for migrations with Accelerate)
DIRECT_DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

## Connection Pooling

In v7, connection pooling is handled by the driver adapter, not by Prisma's URL parameters.

**PostgreSQL with pg driver:**
```typescript
import { Pool } from 'pg'
import { PrismaPg } from '@prisma/adapter-pg'
import { PrismaClient } from './generated/prisma/client'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10, // connection pool size
})

const adapter = new PrismaPg(pool)
const prisma = new PrismaClient({ adapter })
```

## Seeding

**package.json:**
```json
{
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  }
}
```

**prisma/seed.ts:**
```typescript
import { PrismaClient } from '../generated/prisma/client'
import { PrismaPg } from '@prisma/adapter-pg'
import 'dotenv/config'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL
})

const prisma = new PrismaClient({ adapter })

async function main() {
  const user = await prisma.user.create({
    data: {
      email: 'admin@example.com',
      name: 'Admin User',
    },
  })
  
  console.log('Seeded:', user)
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
```

Run with: `npx prisma db seed`

## Troubleshooting

### Module Resolution Errors
**Problem:** `Cannot find module './generated/prisma/client'`

**Solution:**
1. Ensure `"type": "module"` in package.json
2. Run `npx prisma generate`
3. Check output path in generator block
4. Restart TypeScript server

### Connection Errors (P1017)
**Problem:** Cannot connect to database

**Solution:**
1. Verify DATABASE_URL is correct
2. Ensure `import 'dotenv/config'` is at the top of files
3. Check network connectivity
4. Verify database is running

### Migration Fails
**Problem:** Migration cannot be applied

**Solution:**
1. Check schema syntax with `npx prisma validate`
2. Review migration file in `prisma/migrations/`
3. Use `npx prisma migrate reset` in development
4. For production, manually fix and use `npx prisma migrate resolve`

## Performance Tips

1. **Use select instead of include** when you don't need all fields
2. **Add indexes** for frequently queried fields:
   ```prisma
   @@index([email])
   @@index([authorId, createdAt])
   ```
3. **Use connection pooling** with appropriate pool sizes
4. **Batch operations** when possible:
   ```typescript
   await prisma.user.createMany({
     data: [{ email: 'a@b.com' }, { email: 'c@d.com' }]
   })
   ```
5. **Use raw queries** for complex operations:
   ```typescript
   await prisma.$queryRaw`SELECT * FROM users WHERE email LIKE ${'%@example.com'}`
   ```

## Security Best Practices

1. **Never commit .env files** - add to .gitignore
2. **Use environment variables** for sensitive data
3. **Validate input** before passing to Prisma queries
4. **Use parameterized queries** (Prisma does this automatically)
5. **Limit exposed fields** with select/omit in production APIs
6. **Set appropriate connection limits** to prevent exhaustion
7. **Use read replicas** for scaling read operations

## Key Differences from v6

| Aspect | v6 | v7 |
|--------|----|----|
| Module System | CommonJS or ESM | ESM only |
| Client Generator | `prisma-client-js` | `prisma-client` |
| Output Location | `node_modules` default | Custom path required |
| Database Connection | Built-in drivers | Driver adapters required |
| Config Location | schema.prisma | prisma.config.ts |
| Environment Variables | Auto-loaded | Must use dotenv or Bun |
| Rust Dependencies | Yes | No (Rust-free) |

## Additional Resources

- Official Docs: https://www.prisma.io/docs
- Migration Guide: https://www.prisma.io/docs/orm/more/upgrade-guides/upgrading-versions/upgrading-to-prisma-7
- Driver Adapters: https://www.prisma.io/docs/orm/overview/databases/database-drivers
- Prisma Schema Reference: https://www.prisma.io/docs/orm/reference/prisma-schema-reference

## Common Patterns

### Singleton Pattern for Prisma Client
```typescript
// lib/prisma.ts
import { PrismaClient } from './generated/prisma/client'
import { PrismaPg } from '@prisma/adapter-pg'
import 'dotenv/config'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL
})

export const prisma = globalForPrisma.prisma ?? new PrismaClient({ adapter })

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}
```

### Type-safe Enums
```prisma
enum Role {
  USER
  ADMIN
  MODERATOR
}

model User {
  id   Int  @id @default(autoincrement())
  role Role @default(USER)
}
```

Usage:
```typescript
import { Role } from './generated/prisma/client'

const admin = await prisma.user.create({
  data: {
    email: 'admin@example.com',
    role: Role.ADMIN,
  },
})
```

## When to Use Prisma

**Good fit:**
- Type-safe database access
- Complex relations and queries
- Auto-generated migrations
- TypeScript projects
- Need for type safety and IntelliSense

**Consider alternatives if:**
- Need MongoDB (wait for v7 support)
- Existing complex SQL procedures
- Extreme performance requirements
- Very simple CRUD without relations

## Notes

- Always run `npx prisma generate` after schema changes
- Use `npx prisma studio` to visualize your database
- Keep migrations in version control
- Test migrations on staging before production
- Use `npx prisma format` to keep schema clean
- The Rust-free client in v7 is faster and has a smaller bundle size
- Driver adapters enable serverless/edge deployment