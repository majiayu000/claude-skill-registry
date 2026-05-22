---
name: prismadb
description: >-
  Configure and use Prisma 7 ORM with PostgreSQL driver adapters in the FTC Metrics project.
  Use when setting up database schemas, running migrations, troubleshooting Prisma configuration,
  or working with the packages/db package.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: database
---

# Prisma 7 Configuration Guide

Prisma 7 introduces breaking changes from v6. The main change is that database connection configuration has moved from `schema.prisma` to `prisma.config.ts`.

## Quick Start

### 1. Install Dependencies

```bash
bun add @prisma/client @prisma/adapter-pg pg dotenv
bun add -d prisma @types/pg
```

### 2. Create prisma.config.ts

Create `prisma.config.ts` in your Prisma package root (where `prisma/` folder is):

```typescript
import { config } from "dotenv";
import { defineConfig } from "prisma/config";
import path from "path";

// Load .env from appropriate location
config({ path: path.resolve(__dirname, "../../.env") });

export default defineConfig({
  earlyAccess: true,
  schema: "./prisma/schema.prisma",
  datasource: {
    url: process.env.DATABASE_URL!,
  },
  migrate: {
    adapter: async () => {
      const { Pool } = await import("pg");
      const { PrismaPg } = await import("@prisma/adapter-pg");
      const pool = new Pool({ connectionString: process.env.DATABASE_URL });
      return new PrismaPg(pool);
    },
  },
});
```

### 3. Update schema.prisma

Remove `url` from datasource block:

```prisma
datasource db {
  provider = "postgresql"
}

generator client {
  provider = "prisma-client-js"
}

// Your models here...
```

### 4. Create Prisma Client with Adapter

```typescript
import { config } from "dotenv";
import path from "path";

// Load .env from workspace root
config({ path: path.resolve(__dirname, "../../../.env") });

import { Pool } from "pg";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "@prisma/client";

// Create connection pool
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const adapter = new PrismaPg(pool);

// Prevent multiple instances during development
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient({ adapter });

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}

export * from "@prisma/client";
```

## Key Changes from Prisma 6

| Prisma 6 | Prisma 7 |
|----------|----------|
| `url = env("DATABASE_URL")` in schema.prisma | `datasource.url` in prisma.config.ts |
| `new PrismaClient()` | `new PrismaClient({ adapter })` |
| Built-in database driver | Explicit driver adapter required |
| `--schema` flag for CLI | Config file auto-detected |

## Commands

```bash
# Generate Prisma client
prisma generate

# Push schema to database (no migration)
prisma db push

# Create migration
prisma migrate dev --name <name>

# Open Prisma Studio
prisma studio
```

## Common Errors

### "The datasource property `url` is no longer supported"

Remove `url = env("DATABASE_URL")` from your `schema.prisma` datasource block and add it to `prisma.config.ts` instead.

### "The datasource.url property is required"

Ensure your `prisma.config.ts` has the `datasource.url` property set and that the .env file is being loaded correctly.

### Connection errors in monorepo

When using workspaces, ensure the dotenv path resolves to the correct .env location:

```typescript
config({ path: path.resolve(__dirname, "../../.env") }); // Adjust depth as needed
```

## References

- [Upgrade to Prisma 7 Guide](https://www.prisma.io/docs/orm/more/upgrade-guides/upgrading-versions/upgrading-to-prisma-7)
- [Prisma Config Reference](https://www.prisma.io/docs/orm/reference/prisma-config-reference)
- [Driver Adapters](https://www.prisma.io/docs/orm/overview/databases/database-drivers)
