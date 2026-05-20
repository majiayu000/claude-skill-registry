# Neon Serverless Postgres Skill

---
progressive_disclosure:
  entry_point:
    summary: "Serverless Postgres with autoscaling, branching, and instant database provisioning"
    when_to_use:
      - "When needing serverless Postgres"
      - "When building edge and serverless apps"
      - "When implementing database branching for dev/staging"
      - "When using Drizzle, Prisma, or raw SQL"
    quick_start:
      - "Create project on Neon console"
      - "Get connection string"
      - "Connect with Drizzle/Prisma/pg"
      - "Deploy with Vercel/Netlify"
  token_estimate:
    entry: 75-90
    full: 3800-4800
---

## Core Concepts

### Neon Architecture
- **Projects**: Top-level container for databases and branches
- **Databases**: Postgres databases within a project
- **Branches**: Git-like database copies for development
- **Compute**: Autoscaling Postgres instances
- **Storage**: Separated from compute for instant branching

### Key Features
- **Serverless**: Pay-per-use, scales to zero
- **Branching**: Instant database copies from any point in time
- **Autoscaling**: Compute scales based on load
- **Instant Provisioning**: Databases ready in seconds
- **Connection Pooling**: Built-in PgBouncer support

## Connection Strings

### Standard Connection
```bash
# Direct connection (for migrations, admin tasks)
DATABASE_URL="postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname"

# Pooled connection (for application queries)
DATABASE_URL="postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require"
```

### Connection Pooling
```bash
# PgBouncer pooled connection (recommended for serverless)
DATABASE_URL="postgresql://user:password@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require"

# Direct connection for migrations
DIRECT_URL="postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname"
```

## Drizzle ORM Integration

### Setup
```typescript
// drizzle.config.ts
import type { Config } from "drizzle-kit";

export default {
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  driver: "pg",
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
} satisfies Config;

// src/db/index.ts
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql);
```

### Schema Definition
```typescript
// src/db/schema.ts
import { pgTable, serial, text, timestamp, varchar } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: varchar("name", { length: 255 }).notNull(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  createdAt: timestamp("created_at").defaultNow(),
});

export const posts = pgTable("posts", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  content: text("content"),
  userId: serial("user_id").references(() => users.id),
  createdAt: timestamp("created_at").defaultNow(),
});
```

### Queries
```typescript
import { db } from "./db";
import { users, posts } from "./db/schema";
import { eq } from "drizzle-orm";

// Insert
const newUser = await db.insert(users).values({
  name: "John Doe",
  email: "john@example.com",
}).returning();

// Query
const allUsers = await db.select().from(users);

// Join
const userPosts = await db
  .select()
  .from(posts)
  .leftJoin(users, eq(posts.userId, users.id));

// Update
await db.update(users)
  .set({ name: "Jane Doe" })
  .where(eq(users.id, 1));
```

### Migrations
```bash
# Generate migration
npx drizzle-kit generate:pg

# Run migration (use direct connection)
npx drizzle-kit push:pg

# Or use custom script
# src/db/migrate.ts
import { drizzle } from "drizzle-orm/postgres-js";
import { migrate } from "drizzle-orm/postgres-js/migrator";
import postgres from "postgres";

const sql = postgres(process.env.DIRECT_URL!, { max: 1 });
const db = drizzle(sql);

await migrate(db, { migrationsFolder: "./drizzle" });
await sql.end();
```

## Prisma Integration

### Setup
```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  directUrl = env("DIRECT_URL") // For migrations
}

model User {
  id        Int      @id @default(autoincrement())
  name      String
  email     String   @unique
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  userId    Int
  user      User     @relation(fields: [userId], references: [id])
  createdAt DateTime @default(now())
}
```

### Client Usage
```typescript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

// Create
const user = await prisma.user.create({
  data: {
    name: "John Doe",
    email: "john@example.com",
  },
});

// Query with relations
const userWithPosts = await prisma.user.findUnique({
  where: { id: 1 },
  include: { posts: true },
});

// Transaction
await prisma.$transaction([
  prisma.user.create({ data: { name: "User 1", email: "u1@example.com" } }),
  prisma.user.create({ data: { name: "User 2", email: "u2@example.com" } }),
]);
```

### Migrations
```bash
# Create migration
npx prisma migrate dev --name init

# Deploy to production (uses DIRECT_URL)
npx prisma migrate deploy

# Generate client
npx prisma generate
```

## Node-Postgres (pg) Integration

### Direct Connection
```typescript
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

// Query
const result = await pool.query("SELECT * FROM users WHERE email = $1", [
  "john@example.com",
]);

// Transaction
const client = await pool.connect();
try {
  await client.query("BEGIN");
  await client.query("INSERT INTO users (name, email) VALUES ($1, $2)", [
    "John",
    "john@example.com",
  ]);
  await client.query("COMMIT");
} catch (e) {
  await client.query("ROLLBACK");
  throw e;
} finally {
  client.release();
}
```

### Serverless Driver
```typescript
import { neon, neonConfig } from "@neondatabase/serverless";

// Configure for edge runtime
neonConfig.fetchConnectionCache = true;

const sql = neon(process.env.DATABASE_URL!);

// Execute query
const result = await sql`SELECT * FROM users WHERE email = ${email}`;

// Transactions
const [user] = await sql.transaction([
  sql`INSERT INTO users (name, email) VALUES (${name}, ${email}) RETURNING *`,
  sql`INSERT INTO audit_log (action) VALUES ('user_created')`,
]);
```

## Database Branching

### Branch Types
- **Main**: Production branch
- **Development**: Feature development
- **Preview**: PR/deployment previews
- **Testing**: QA and testing environments

### Creating Branches
```bash
# Via CLI
neonctl branches create --name dev --parent main

# Via API
curl -X POST https://console.neon.tech/api/v2/projects/{project_id}/branches \
  -H "Authorization: Bearer $NEON_API_KEY" \
  -d '{"name": "dev", "parent_id": "main"}'

# Via Console
# Navigate to project → Branches → Create branch
```

### Branch Workflows

#### Feature Development
```bash
# 1. Create feature branch
neonctl branches create --name feature/user-auth --parent dev

# 2. Get connection string
neonctl connection-string feature/user-auth

# 3. Update .env.local
DATABASE_URL="postgresql://...feature-user-auth..."

# 4. Run migrations
npm run migrate

# 5. Develop and test

# 6. Merge changes (via schema migration)

# 7. Delete branch
neonctl branches delete feature/user-auth
```

#### Preview Deployments
```typescript
// vercel.json
{
  "env": {
    "DATABASE_URL": "@database-url-main"
  },
  "build": {
    "env": {
      "DATABASE_URL": "@database-url-preview"
    }
  }
}

// Create preview branch on deploy
// .github/workflows/preview.yml
- name: Create Neon Branch
  run: |
    BRANCH_NAME="preview-${{ github.event.number }}"
    neonctl branches create --name $BRANCH_NAME --parent main
    DATABASE_URL=$(neonctl connection-string $BRANCH_NAME)
    echo "DATABASE_URL=$DATABASE_URL" >> $GITHUB_ENV
```

### Point-in-Time Recovery
```bash
# Create branch from specific timestamp
neonctl branches create --name recovery \
  --parent main \
  --timestamp "2024-01-15T10:30:00Z"

# Restore from branch
neonctl branches reset main --from recovery
```

## Vercel Integration

### Automatic Setup
```bash
# Install Vercel CLI
npm i -g vercel

# Link project
vercel link

# Add Neon integration
vercel integration add neon

# Vercel automatically:
# - Creates main branch connection
# - Creates preview branch per PR
# - Sets DATABASE_URL environment variable
```

### Manual Configuration
```bash
# Add to Vercel project settings
vercel env add DATABASE_URL

# For preview branches
vercel env add DATABASE_URL preview

# For production
vercel env add DATABASE_URL production
```

### Next.js Integration
```typescript
// app/api/users/route.ts
import { neon } from "@neondatabase/serverless";

export const runtime = "edge";

export async function GET() {
  const sql = neon(process.env.DATABASE_URL!);
  const users = await sql`SELECT * FROM users`;

  return Response.json(users);
}

// app/api/users/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const sql = neon(process.env.DATABASE_URL!);
  const [user] = await sql`SELECT * FROM users WHERE id = ${params.id}`;

  if (!user) {
    return new Response("Not found", { status: 404 });
  }

  return Response.json(user);
}
```

## Connection Pooling

### PgBouncer Pooling
```typescript
// Use pooled connection for queries
const pooledDb = drizzle(neon(process.env.DATABASE_URL!));

// Use direct connection for migrations
const directDb = drizzle(neon(process.env.DIRECT_URL!));

// package.json scripts
{
  "scripts": {
    "migrate": "DATABASE_URL=$DIRECT_URL drizzle-kit push:pg",
    "dev": "next dev"
  }
}
```

### Connection Limits
```typescript
// Configure pool size
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20, // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// For serverless, use Neon's serverless driver
import { neon } from "@neondatabase/serverless";
// Automatically handles connection pooling
```

## Autoscaling and Compute

### Compute Units
```yaml
# Free Tier
- 0.25 Compute Units (CU)
- Scales to zero when idle
- Shared compute

# Pro Tier
- 0.25 - 4 CU autoscaling
- Configurable min/max
- Dedicated compute
```

### Configuration
```bash
# Via CLI
neonctl set-compute --min 0.25 --max 2 --branch main

# Via API
curl -X PATCH https://console.neon.tech/api/v2/projects/{id}/branches/{branch_id} \
  -d '{"compute": {"min_cu": 0.25, "max_cu": 2}}'
```

### Autoscaling Strategy
```typescript
// Development: Scale to zero
// min: 0.25 CU, max: 1 CU

// Staging: Minimal baseline
// min: 0.5 CU, max: 2 CU

// Production: Always-on baseline
// min: 1 CU, max: 4 CU

// Configure per branch
const computeConfig = {
  dev: { min: 0.25, max: 1 },
  staging: { min: 0.5, max: 2 },
  main: { min: 1, max: 4 },
};
```

## Read Replicas

### Setup
```bash
# Create read replica
neonctl read-replica create --branch main --region us-east-1

# Get connection string
neonctl connection-string --replica
```

### Usage Pattern
```typescript
// Write to primary
const writeDb = drizzle(neon(process.env.DATABASE_URL!));

// Read from replica
const readDb = drizzle(neon(process.env.DATABASE_URL_REPLICA!));

// Application logic
async function getUser(id: number) {
  return await readDb.select().from(users).where(eq(users.id, id));
}

async function updateUser(id: number, data: any) {
  return await writeDb.update(users).set(data).where(eq(users.id, id));
}

// Load balancing
const replicas = [
  process.env.DATABASE_URL_REPLICA_1!,
  process.env.DATABASE_URL_REPLICA_2!,
];

function getReadConnection() {
  const url = replicas[Math.floor(Math.random() * replicas.length)];
  return drizzle(neon(url));
}
```

## CLI Usage

### Installation
```bash
npm install -g neonctl

# Or use npx
npx neonctl --help
```

### Common Commands
```bash
# Authentication
neonctl auth

# List projects
neonctl projects list

# Create project
neonctl projects create --name my-app

# List branches
neonctl branches list

# Create branch
neonctl branches create --name dev --parent main

# Get connection string
neonctl connection-string main

# Database operations
neonctl databases create --name analytics
neonctl databases list

# Compute settings
neonctl set-compute --min 0.5 --max 2

# Delete branch
neonctl branches delete dev
```

## Migration Strategies

### Drizzle Migrations
```typescript
// drizzle/migrate.ts
import { drizzle } from "drizzle-orm/postgres-js";
import { migrate } from "drizzle-orm/postgres-js/migrator";
import postgres from "postgres";

const runMigrations = async () => {
  const connection = postgres(process.env.DIRECT_URL!, { max: 1 });
  const db = drizzle(connection);

  console.log("Running migrations...");
  await migrate(db, { migrationsFolder: "./drizzle" });
  console.log("Migrations complete!");

  await connection.end();
};

runMigrations();
```

### Prisma Migrations
```bash
# Development
npx prisma migrate dev --name add_users_table

# Production (uses DIRECT_URL)
npx prisma migrate deploy

# Reset database (dev only)
npx prisma migrate reset
```

### Zero-Downtime Migrations
```sql
-- 1. Add new column (nullable)
ALTER TABLE users ADD COLUMN new_email VARCHAR(255);

-- 2. Backfill data
UPDATE users SET new_email = email;

-- 3. Make non-nullable (after verification)
ALTER TABLE users ALTER COLUMN new_email SET NOT NULL;

-- 4. Drop old column
ALTER TABLE users DROP COLUMN email;

-- 5. Rename column
ALTER TABLE users RENAME COLUMN new_email TO email;
```

### Branch-Based Migrations
```bash
# 1. Create migration branch
neonctl branches create --name migration/add-index --parent main

# 2. Test migration on branch
DATABASE_URL=$(neonctl connection-string migration/add-index) \
  npm run migrate

# 3. Verify on branch
DATABASE_URL=$(neonctl connection-string migration/add-index) \
  npm run test

# 4. Apply to main
npm run migrate:production

# 5. Delete migration branch
neonctl branches delete migration/add-index
```

## Best Practices

### Serverless Optimization
```typescript
// ✅ Use Neon serverless driver for edge
import { neon } from "@neondatabase/serverless";
const sql = neon(process.env.DATABASE_URL!);

// ✅ Enable connection caching
import { neonConfig } from "@neondatabase/serverless";
neonConfig.fetchConnectionCache = true;

// ✅ Use pooled connections
const pooledUrl = process.env.DATABASE_URL; // -pooler endpoint

// ❌ Don't use standard pg in edge runtime
// import { Pool } from "pg"; // Won't work in edge
```

### Connection Management
```typescript
// ✅ Reuse connections in serverless
let cachedDb: ReturnType<typeof drizzle> | null = null;

function getDb() {
  if (!cachedDb) {
    const sql = neon(process.env.DATABASE_URL!);
    cachedDb = drizzle(sql);
  }
  return cachedDb;
}

// ✅ Use transactions for consistency
await db.transaction(async (tx) => {
  await tx.insert(users).values({ name: "John" });
  await tx.insert(auditLog).values({ action: "user_created" });
});

// ❌ Don't forget to close pools in long-running processes
// await pool.end();
```

### Branch Strategy
```yaml
Environments:
  main: Production data
  staging: Pre-production testing
  dev: Shared development
  feature/*: Individual features
  preview/*: PR previews (auto-created)

Lifecycle:
  - Create from parent on feature start
  - Run migrations independently
  - Test thoroughly
  - Merge schema changes
  - Delete after feature completion
```

### Cost Optimization
```typescript
// Development: Scale to zero
// - min_cu: 0.25
// - Suspend after 5 minutes idle

// Staging: Minimal always-on
// - min_cu: 0.5
// - Reduce during off-hours

// Production: Right-size baseline
// - min_cu: Based on traffic patterns
// - max_cu: Handle peak load

// Branch cleanup
// Delete unused preview branches after PR merge
```

## Environment Variables

### Required Variables
```bash
# Neon connection strings
DATABASE_URL="postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/db?sslmode=require"
DIRECT_URL="postgresql://user:pass@ep-xxx.region.aws.neon.tech/db?sslmode=require"

# API access (for CLI/automation)
NEON_API_KEY="your_api_key"

# Project configuration
NEON_PROJECT_ID="your_project_id"
```

### Multi-Environment Setup
```bash
# .env.local (development)
DATABASE_URL="postgresql://...dev-branch..."

# .env.staging
DATABASE_URL="postgresql://...staging-branch..."

# .env.production (via Vercel)
DATABASE_URL="postgresql://...main-branch..."
```

## Common Patterns

### API Route with Caching
```typescript
import { neon } from "@neondatabase/serverless";

export const runtime = "edge";

export async function GET() {
  const sql = neon(process.env.DATABASE_URL!);

  const users = await sql`SELECT * FROM users ORDER BY created_at DESC LIMIT 10`;

  return Response.json(users, {
    headers: {
      "Cache-Control": "s-maxage=60, stale-while-revalidate",
    },
  });
}
```

### Server Actions (Next.js)
```typescript
"use server";

import { neon } from "@neondatabase/serverless";
import { revalidatePath } from "next/cache";

export async function createUser(formData: FormData) {
  const sql = neon(process.env.DATABASE_URL!);

  const name = formData.get("name") as string;
  const email = formData.get("email") as string;

  await sql`INSERT INTO users (name, email) VALUES (${name}, ${email})`;

  revalidatePath("/users");
}
```

### Connection Testing
```typescript
async function testConnection() {
  const sql = neon(process.env.DATABASE_URL!);

  try {
    const result = await sql`SELECT version()`;
    console.log("✅ Connected to Neon:", result[0].version);
    return true;
  } catch (error) {
    console.error("❌ Connection failed:", error);
    return false;
  }
}
```

## Troubleshooting

### Connection Issues
```typescript
// Check SSL requirement
const url = new URL(process.env.DATABASE_URL!);
if (!url.searchParams.has("sslmode")) {
  url.searchParams.set("sslmode", "require");
}

// Verify endpoint type
// -pooler: For application queries
// direct: For migrations and admin tasks

// Test connectivity
import { neon } from "@neondatabase/serverless";
const sql = neon(process.env.DATABASE_URL!);
await sql`SELECT 1`; // Should succeed
```

### Migration Failures
```bash
# Use direct connection for migrations
export DIRECT_URL="postgresql://...direct-endpoint..."
npx prisma migrate deploy

# Check migration status
npx prisma migrate status

# Force reset (dev only)
npx prisma migrate reset
```

### Performance Issues
```typescript
// Enable query logging
import { drizzle } from "drizzle-orm/neon-http";
const db = drizzle(sql, { logger: true });

// Check slow queries in Neon console
// Monitoring → Query Performance

// Add indexes
await sql`CREATE INDEX idx_users_email ON users(email)`;

// Use connection pooling
// Ensure using -pooler endpoint
```

This skill provides comprehensive coverage of Neon serverless Postgres, including database branching, ORM integrations, serverless deployment patterns, and production best practices.